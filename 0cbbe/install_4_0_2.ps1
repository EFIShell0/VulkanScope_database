#Requires -Version 5.1
[CmdletBinding()]
param(
  [string]$Zip = (Join-Path $env:USERPROFILE 'Downloads\VulkanScope-Database-4.0.2.zip'),
  [string]$Repository = (Join-Path $env:USERPROFILE 'Desktop\VulkanScope_database')
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
function Invoke-Checked {
  param([string]$Exe, [string[]]$ArgList)
  & $Exe @ArgList
  if ($LASTEXITCODE -ne 0) { throw "Command failed ($LASTEXITCODE): $Exe $($ArgList -join ' ')" }
}
$Repository = [IO.Path]::GetFullPath($Repository)
$Zip = [IO.Path]::GetFullPath($Zip)
if (-not (Test-Path -LiteralPath $Zip -PathType Leaf)) { throw "Missing release ZIP: $Zip" }
if (-not (Test-Path -LiteralPath (Join-Path $Repository '.git'))) { throw "Not a Git checkout: $Repository" }
$checksum = "$Zip.sha256"
if (-not (Test-Path -LiteralPath $checksum -PathType Leaf)) { throw "Missing SHA-256 file: $checksum" }
$line = (Get-Content -LiteralPath $checksum -TotalCount 1)
if ($line -match '^([0-9a-fA-F]{64})\s+VulkanScope-Database-4\.0\.2\.zip$') {
  $expected = $Matches[1].ToLowerInvariant()
} else {
  throw 'Malformed 4.0.2 checksum file'
}
$actual = (Get-FileHash -LiteralPath $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $expected) { throw "ZIP integrity mismatch expected=$expected got=$actual" }
# Verify every archive filename before extraction, not merely ZIP integrity.
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [IO.Compression.ZipFile]::OpenRead($Zip)
try {
  $names = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
  foreach ($entry in $archive.Entries) {
    $name = $entry.FullName.Replace('\','/')
    if (!$name -or $name.StartsWith('/') -or $name.Contains(':') -or $name -match '(^|/)\.\.(/|$)') { throw "Unsafe ZIP path: $name" }
    if (-not $names.Add($name)) { throw "Duplicate ZIP path: $name" }
  }
} finally { $archive.Dispose() }

$branch = (& git -C $Repository branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $branch -ne 'main') { throw 'Checkout must be on main' }
$status = @(& git -C $Repository status --porcelain)
if ($LASTEXITCODE -ne 0) { throw 'Unable to inspect Git status' }
if ($status.Count -gt 0) {
  $label = 'Before-VulkanScope-Database-4.0.2-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
  Invoke-Checked git @('-C',$Repository,'stash','push','--include-untracked','-m',$label)
  Write-Host "Local changes preserved as stash: $label"
}
Invoke-Checked git @('-C',$Repository,'pull','--ff-only','origin','main')
$stage = Join-Path $env:TEMP ('VulkanScope-4.0.2-stage-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stage -Force | Out-Null
try {
  Expand-Archive -LiteralPath $Zip -DestinationPath $stage
  $paths = @(
    'regression\1.4.12_to_1.4.13_contract.json',
    'regression\1.4.13_to_4.0.0_contract.json',
    'regression\4.0.0_to_4.0.1_contract.json',
    'regression\4.0.1_to_4.0.2_contract.json'
  )
  foreach ($file in $paths) {
    $source = Join-Path $stage $file
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Missing update contract: $file" }
    $c = Get-Content -LiteralPath $source -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($relative in $c.allowedRemoved) {
      if ($relative -notmatch '^[A-Za-z0-9_./-]+$' -or $relative -match '(^|/)\.\.(/|$)') { throw "Unsafe removal path: $relative" }
      $dest = [IO.Path]::GetFullPath((Join-Path $Repository $relative.Replace('/','\')))
      if (-not $dest.StartsWith(($Repository.TrimEnd('\')+'\'),[StringComparison]::OrdinalIgnoreCase)) { throw "Removal outside checkout: $relative" }
      if (Test-Path -LiteralPath $dest -PathType Leaf) { Remove-Item -LiteralPath $dest -Force }
    }
  }
  # Copy each file explicitly; never rely on recursive directory overlay semantics.
  $sourceFiles = @(Get-ChildItem -LiteralPath $stage -Recurse -File -Force)
  foreach ($source in $sourceFiles) {
    $relative = $source.FullName.Substring($stage.Length).TrimStart('\','/')
    $target = [IO.Path]::GetFullPath((Join-Path $Repository $relative))
    if (-not $target.StartsWith(($Repository.TrimEnd('\')+'\'),[StringComparison]::OrdinalIgnoreCase)) { throw "Copy outside checkout: $relative" }
    $parent = Split-Path -Parent $target
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    Copy-Item -LiteralPath $source.FullName -Destination $target -Force
    $srcHash = (Get-FileHash -LiteralPath $source.FullName -Algorithm SHA256).Hash
    $dstHash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
    if ($srcHash -ne $dstHash) { throw "Post-copy file mismatch: $relative" }
  }
  Push-Location $Repository
  try {
    # This must run BEFORE repair. The mixed 4.0.0/4.0.1 problem must not be concealed.
    Invoke-Checked python @('-B','tools\verify_4_0_2_checkout.py')
    Invoke-Checked python @('-B','tools\test_4_0_2_checkout_negative_mutations.py')
    Invoke-Checked python @('-B','tools\repair_repository.py','--apply')
    Invoke-Checked python @('-B','tools\quality_gate.py')
    Invoke-Checked python @('-B','tools\verify_4_0_2_regression_contract.py')
    Write-Host 'PASS: 4.0.2 checkout and local quality gates. Review changes before committing.' -ForegroundColor Green
    Invoke-Checked git @('status','--short')
  } finally { Pop-Location }
} finally {
  if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
}
