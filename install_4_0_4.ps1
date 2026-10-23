#Requires -Version 5.1
[CmdletBinding()]
param(
    [string]$Zip = (Join-Path $env:USERPROFILE 'Downloads\VulkanScope-Database-4.0.4.zip'),
    [string]$Repository = (Join-Path $env:USERPROFILE 'Desktop\VulkanScope_database'),
    [string]$Sha256 = ''
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
function Invoke-Checked([string]$Exe,[string[]]$Arguments) {
    & $Exe @Arguments
    if ($LASTEXITCODE -ne 0) { throw "FAIL: $Exe $($Arguments -join ' ') exit=$LASTEXITCODE" }
}
function FileHash([string]$Path) { return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Ensure([bool]$Condition,[string]$Message) { if (-not $Condition) { throw $Message } }

$Zip = [IO.Path]::GetFullPath($Zip)
$Repository = [IO.Path]::GetFullPath($Repository).TrimEnd('\','/')
$parent = [IO.Path]::GetDirectoryName($Repository)
$basename = [IO.Path]::GetFileName($Repository)
Ensure ($basename -eq 'VulkanScope_database') 'The permanent repository must be named VulkanScope_database'
Ensure ([IO.File]::Exists($Zip)) "Missing release ZIP: $Zip"
$shaFile = "$Zip.sha256"
if ([string]::IsNullOrEmpty($Sha256)) {
    Ensure ([IO.File]::Exists($shaFile)) "Missing companion SHA-256 file: $shaFile"
    $line = [IO.File]::ReadAllText($shaFile).Trim()
    Ensure ($line -match '^([A-Fa-f0-9]{64})\s+VulkanScope-Database-4\.0\.4\.zip$') 'Invalid SHA-256 companion'
    $Sha256 = $Matches[1]
}
Ensure ($Sha256 -match '^[a-fA-F0-9]{64}$') 'Invalid expected SHA-256'
Ensure ((FileHash $Zip) -eq $Sha256.ToLowerInvariant()) 'ZIP SHA-256 mismatch'
Ensure ([IO.Directory]::Exists($Repository)) "Original repository not found: $Repository"
Ensure ([IO.Directory]::Exists((Join-Path $Repository '.git'))) 'Original path is not a Git checkout'
$origin = (& git -C $Repository remote get-url origin).Trim()
Ensure ($LASTEXITCODE -eq 0 -and $origin -match '^https://github\.com/EFIShell0/VulkanScope_database(?:\.git)?$') 'Unexpected original Git origin'
Ensure ([IO.Directory]::Exists($parent)) "Parent directory not found: $parent"
# Do not hold the directory being renamed as this PowerShell process's current location.
Set-Location -LiteralPath $parent

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$guid = [guid]::NewGuid().ToString('N').Substring(0,10)
$staging = Join-Path $parent "VulkanScope_database_staging_404_$stamp`_$guid"
$backup = Join-Path $parent "VulkanScope_database_backup_before_404_$stamp`_$guid"
$unpacked = Join-Path $env:TEMP "VulkanScope_database_404_source_$guid"
Ensure (-not ([IO.Directory]::Exists($staging) -or [IO.Directory]::Exists($backup) -or [IO.Directory]::Exists($unpacked))) 'Unexpected staging directory collision'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive = [IO.Compression.ZipFile]::OpenRead($Zip)
try {
    $seen = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
    $entries = @($archive.Entries | Where-Object { -not $_.FullName.EndsWith('/') })
    Ensure ($entries.Count -ge 850) "Incomplete ZIP: $($entries.Count) files"
    foreach($entry in $entries) {
        $rel = $entry.FullName.Replace('\','/')
        Ensure (-not [string]::IsNullOrWhiteSpace($rel)) 'Empty ZIP entry'
        Ensure (-not ($rel.StartsWith('/') -or $rel.Contains(':') -or $rel -match '(^|/)(\.\.?)(/|$)' -or -not $seen.Add($rel))) "Unsafe ZIP path: $rel"
        $unixMode = ($entry.ExternalAttributes -shr 16) -band 0xF000
        Ensure ($unixMode -ne 0xA000) "ZIP symbolic link is forbidden: $rel"
    }
    foreach($required in @('tools/verify_4_0_4_checkout.py','tools/verify_4_0_4_layout.py','tools/quality_gate.py','index.html','rules/PROJECT_RULES.md','regression/4.0.3_to_4.0.4_contract.json','install_4_0_4.ps1')) {
        Ensure ($seen.Contains($required)) "Missing canonical release path: $required"
    }
    [IO.Directory]::CreateDirectory($unpacked) | Out-Null
    $sourcePrefix = $unpacked.TrimEnd('\','/') + [IO.Path]::DirectorySeparatorChar
    foreach($entry in $entries) {
        $relative = $entry.FullName.Replace('/',[IO.Path]::DirectorySeparatorChar)
        $file = [IO.Path]::GetFullPath((Join-Path $unpacked $relative))
        Ensure ($file.StartsWith($sourcePrefix,[StringComparison]::OrdinalIgnoreCase)) "ZIP path escapes source: $relative"
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($file)) | Out-Null
        $inStream = $entry.Open()
        try {
            $outStream = [IO.File]::Open($file,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
            try { $inStream.CopyTo($outStream) } finally { $outStream.Dispose() }
        } finally { $inStream.Dispose() }
    }
} finally { $archive.Dispose() }
Write-Host "PASS: verified ZIP and extracted $($entries.Count) files" -ForegroundColor Green
# Fail fast while ORIGINAL root and stash are completely untouched.
Push-Location $unpacked
try {
    Invoke-Checked python @('-B','tools\verify_4_0_4_layout.py')
    Invoke-Checked python @('-B','tools\verify_4_0_4_checkout.py')
    Invoke-Checked python @('-B','tools\verify_4_0_4_regression_contract.py','--strict-tree')
    Invoke-Checked python @('-B','tools\verify_4_0_4_snapshot_jxl.py')
} finally { Pop-Location }
# Always use a temporary fresh clone, then promote into the SAME established repository path.
Invoke-Checked git @('clone','--branch','main','--single-branch','https://github.com/EFIShell0/VulkanScope_database.git',$staging)
$cloneOrigin = (& git -C $staging remote get-url origin).Trim()
Ensure ($LASTEXITCODE -eq 0 -and $cloneOrigin -match '^https://github\.com/EFIShell0/VulkanScope_database(?:\.git)?$') 'Unexpected staging Git origin'
# Remove only fully recognized and entirely tracked nested project copies, never the original root.
$fixedNames=@('.git','assets','tools','worker','data','registry','rules','regression','licenses','compat','.github')
foreach($dir in @(Get-ChildItem -LiteralPath $staging -Directory -Force)) {
    if ($dir.Name -in $fixedNames) { continue }
    $markers=@('tools/repair_repository.py','tools/audit_database.py','rules/PROJECT_RULES.md','data/release.json')
    $complete=$true
    foreach($marker in $markers) { if (-not [IO.File]::Exists((Join-Path $dir.FullName $marker))) { $complete=$false; break } }
    if (-not $complete) { continue }
    Ensure ($dir.Name -match '^[a-fA-F0-9]{5,40}$') "Unknown nested project location: $($dir.Name)"
    $tracked=@(& git -C $staging ls-files -- $dir.Name)
    Ensure ($LASTEXITCODE -eq 0 -and $tracked.Count -gt 100) "Unexpected nested tracked files: $($dir.Name)"
    $unknown=@(& git -C $staging ls-files --others --exclude-standard -- $dir.Name)
    Ensure ($LASTEXITCODE -eq 0 -and $unknown.Count -eq 0) "Unknown files in nested clone: $($dir.Name)"
    Invoke-Checked git @('-C',$staging,'rm','-rq','--',$dir.Name)
    Write-Host "Removed nested tracked clone from STAGING only: $($dir.Name)"
}
# Remove exactly the predecessor-contract-declared obsolete tracked paths.
$contract = Get-Content -LiteralPath (Join-Path $unpacked 'regression\4.0.3_to_4.0.4_contract.json') -Raw | ConvertFrom-Json
foreach($rel in @($contract.allowedRemoved)) {
    $oldFile = Join-Path $staging ($rel.Replace('/',[IO.Path]::DirectorySeparatorChar))
    if ([IO.File]::Exists($oldFile)) {
        Invoke-Checked git @('-C',$staging,'rm','-f','--',$rel)
    }
}
$targetPrefix=$staging.TrimEnd('\','/')+[IO.Path]::DirectorySeparatorChar
foreach($entry in $entries) {
    $relative=$entry.FullName.Replace('/',[IO.Path]::DirectorySeparatorChar)
    $inputPath=Join-Path $unpacked $relative
    $outputPath=[IO.Path]::GetFullPath((Join-Path $staging $relative))
    Ensure ($outputPath.StartsWith($targetPrefix,[StringComparison]::OrdinalIgnoreCase)) "Overlay path escaped staging: $relative"
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($outputPath)) | Out-Null
    Copy-Item -LiteralPath $inputPath -Destination $outputPath -Force
    Ensure ((FileHash $inputPath) -eq (FileHash $outputPath)) "Overlay content mismatch: $relative"
}
Write-Host 'PASS: canonical-root source overlay; original checkout untouched' -ForegroundColor Green
Push-Location $staging
try {
    Invoke-Checked python @('-B','tools\verify_4_0_4_layout.py')
    Invoke-Checked python @('-B','tools\verify_4_0_4_checkout.py')
    Invoke-Checked python @('-B','tools\repair_repository.py','--apply')
    Invoke-Checked python @('-B','tools\quality_gate.py')
    $releaseCheck=Join-Path $env:TEMP "vsdb404-release-$guid"
    Invoke-Checked python @('-B','tools\package_release.py',$releaseCheck)
    Invoke-Checked git @('add','-A')
    Invoke-Checked git @('diff','--cached','--check')
    $stat = @(& git diff --cached --name-only)
    Ensure ($LASTEXITCODE -eq 0 -and $stat.Count -gt 0) 'No changes staged for 4.0.4 release'
} finally { Pop-Location }
# Only after the ENTIRE validation can the permanent path be swapped.
$originalMoved=$false
$promoted=$false
try {
    Rename-Item -LiteralPath $Repository -NewName ([IO.Path]::GetFileName($backup)) -ErrorAction Stop
    $originalMoved=$true
    Rename-Item -LiteralPath $staging -NewName $basename -ErrorAction Stop
    $promoted=$true
} catch {
    if ($originalMoved -and -not $promoted -and -not [IO.Directory]::Exists($Repository)) {
        Rename-Item -LiteralPath $backup -NewName $basename -ErrorAction Stop
    }
    throw
}
Ensure ([IO.File]::Exists((Join-Path $Repository 'tools\verify_4_0_4_checkout.py'))) 'Promoted repository missing verifier'
Write-Host ''
Write-Host 'PASS: VulkanScope Database 4.0.4 installed to permanent original path' -ForegroundColor Green
Write-Host "REPOSITORY=$Repository"
Write-Host "ORIGINAL_BACKUP=$backup"
Write-Host 'Staged changes are ready. Commit and push manually only after reviewing them.'
Write-Host 'No existing stashes, local user files, D1 data, Cloudflare resources or GitHub releases were deleted.'
Invoke-Checked git @('-C',$Repository,'status','--short')
