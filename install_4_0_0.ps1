#Requires -Version 5.1
[CmdletBinding()]
param(
  [string]$Zip = (Join-Path $env:USERPROFILE 'Downloads\VulkanScope-Database-4.0.0.zip'),
  [string]$Repository = (Join-Path $env:USERPROFILE 'Desktop\VulkanScope_database')
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Invoke-Checked {
  param([string]$Exe, [string[]]$Arguments)
  & $Exe @Arguments
  if ($LASTEXITCODE -ne 0) { throw "Command failed (exit $LASTEXITCODE): $Exe $($Arguments -join ' ')" }
}

$Repository = [IO.Path]::GetFullPath($Repository)
$Zip = [IO.Path]::GetFullPath($Zip)
if (-not (Test-Path -LiteralPath $Zip -PathType Leaf)) { throw "Missing ZIP: $Zip" }
if (-not (Test-Path -LiteralPath (Join-Path $Repository '.git'))) { throw "Not a Git checkout: $Repository" }

$hashFile = "$Zip.sha256"
if (-not (Test-Path -LiteralPath $hashFile)) { throw "Missing SHA-256 companion file: $hashFile" }
$line = (Get-Content -LiteralPath $hashFile -TotalCount 1)
if ($line -notmatch '^([0-9a-fA-F]{64})\s+VulkanScope-Database-4\.0\.0\.zip$') { throw 'Unexpected checksum file content' }
$expected = $Matches[1].ToLowerInvariant()
$actual = (Get-FileHash -LiteralPath $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw 'ZIP SHA-256 verification failed' }

# Stop on every failure. In interactive PowerShell a `throw` in an earlier pasted
# block does NOT prevent users from running subsequent blocks; this single script does.
Invoke-Checked 'git' @('-C',$Repository,'status','--short')
$branch = (& git -C $Repository branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne 'main') { throw 'Repository must be on main' }
$status = @(& git -C $Repository status --porcelain)
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect working tree' }
if ($status.Count -gt 0) {
  $message = 'Before-VulkanScope-Database-4.0.0-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
  Invoke-Checked 'git' @('-C',$Repository,'stash','push','--include-untracked','-m',$message)
  Write-Host 'Local changes were preserved in Git stash (not re-applied automatically):' $message
  Invoke-Checked 'git' @('-C',$Repository,'stash','list','-1')
}
Invoke-Checked 'git' @('-C',$Repository,'pull','--ff-only','origin','main')

$stage = Join-Path $env:TEMP ('VulkanScope-Database-4.0.0-install-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stage -Force | Out-Null
try {
  Expand-Archive -LiteralPath $Zip -DestinationPath $stage -Force
  $contracts = @(
     (Join-Path $stage 'regression\1.4.12_to_1.4.13_contract.json'),
     (Join-Path $stage 'regression\1.4.13_to_4.0.0_contract.json')
  )
  # These are the only source files the two updates explicitly retire.
  foreach ($contractPath in $contracts) {
    if (-not (Test-Path -LiteralPath $contractPath)) { throw "Missing contract: $contractPath" }
    $contract = Get-Content -LiteralPath $contractPath -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($relative in $contract.allowedRemoved) {
      if ($relative -match '(^|/|\\)\.git($|/|\\)' -or $relative -match '(^|/|\\)\.\.(?:/|\\|$)') { throw "Unsafe contract path: $relative" }
      $target = [IO.Path]::GetFullPath((Join-Path $Repository $relative.Replace('/','\')))
      if (-not $target.StartsWith(($Repository.TrimEnd('\') + '\'),[StringComparison]::OrdinalIgnoreCase)) { throw "Path outside repository: $relative" }
      if (Test-Path -LiteralPath $target -PathType Leaf) { Remove-Item -LiteralPath $target -Force }
    }
  }
  Get-ChildItem -LiteralPath $stage -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $Repository -Recurse -Force
  }
  Push-Location $Repository
  try {
    Invoke-Checked 'python' @('-B','tools\quality_gate.py')
    Invoke-Checked 'python' @('-B','tools\verify_regression_contract.py')
    Write-Host 'PASS: VulkanScope Database 4.0.0 sources installed and verified.'
    Write-Host 'Review git diff and deploy intentionally; no Git push or production migration was run.'
    Invoke-Checked 'git' @('status','--short')
  } finally { Pop-Location }
} finally {
  if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Force -Recurse }
}
