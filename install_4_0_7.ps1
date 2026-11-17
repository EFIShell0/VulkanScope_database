#Requires -Version 5.1
<# VulkanScope Database 4.0.7 source overlay installer.
    Never renames or removes the existing repository, changes Git history,
    pushes to a remote, deploys Cloudflare, or changes stored report data.
    Local project must be clean; original overwritten files are backed up.
#>
[CmdletBinding()]
param(
    [string]$Archive = (Join-Path $env:USERPROFILE 'Downloads\VulkanScope-Database-4.0.7.zip'),
    [string]$ProjectRoot = (Join-Path $env:USERPROFILE 'Desktop\VulkanScope_database')
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$ProjectRoot=[IO.Path]::GetFullPath($ProjectRoot)
$Archive=[IO.Path]::GetFullPath($Archive)
if ([IO.Path]::GetFileName($ProjectRoot.TrimEnd('\','/')) -cne 'VulkanScope_database') {throw 'Wrong project directory name; expected VulkanScope_database.'}
if (-not (Test-Path -LiteralPath $Archive -PathType Leaf)) {throw "Missing package: $Archive"}
if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot '.git') -PathType Container)) {throw "Existing Git checkout not found: $ProjectRoot"}
if ((Get-Item -LiteralPath $ProjectRoot).Attributes -band [IO.FileAttributes]::ReparsePoint) {throw 'Repository symlink is not supported.'}
$hashFile="$Archive.sha256"
if (-not (Test-Path -LiteralPath $hashFile -PathType Leaf)) {throw "Missing ZIP checksum: $hashFile"}
$checksum=([IO.File]::ReadAllText($hashFile)).Trim()
if ($checksum -cnotmatch '^([a-fA-F0-9]{64})\s+VulkanScope-Database-4\.0\.7\.zip$') {throw 'Invalid 4.0.7 checksum companion.'}
$expected=$Matches[1]
$actual=(Get-FileHash -LiteralPath $Archive -Algorithm SHA256).Hash
if ($expected -ine $actual) {throw 'Package SHA256 mismatch. Nothing was installed.'}
$changes=@(& git -C $ProjectRoot status --porcelain 2>$null)
if ($LASTEXITCODE -ne 0) {throw 'Git status check failed.'}
if ($changes.Count -gt 0) {throw 'Project has local changes or untracked files. Back them up or commit them manually before installing.'}
$stage=Join-Path ([IO.Path]::GetTempPath()) ('VulkanScope_DB_407_'+[guid]::NewGuid().ToString('N'))
$backup=Join-Path (Join-Path $env:USERPROFILE 'Downloads') ('VulkanScope_DB_backup_'+(Get-Date -Format 'yyyyMMdd_HHmmss')+'_'+[guid]::NewGuid().ToString('N').Substring(0,6))
[IO.Directory]::CreateDirectory($stage) | Out-Null
try {
    Expand-Archive -LiteralPath $Archive -DestinationPath $stage -Force
    if (-not (Test-Path -LiteralPath (Join-Path $stage 'tools\verify_4_0_7_release.py'))) {throw 'Not a flat 4.0.7 source archive.'}
    if (Test-Path -LiteralPath (Join-Path $stage '.git')) {throw 'Archive must not contain Git metadata.'}
    Push-Location -LiteralPath $stage
    try {
        & python -B tools\quality_gate.py
        if ($LASTEXITCODE -ne 0) {throw 'Release quality gate rejected the extracted ZIP.'}
    } finally {Pop-Location}
    $sourceRoot=(Resolve-Path -LiteralPath $stage).Path.TrimEnd('\','/')
    $files=@(Get-ChildItem -LiteralPath $stage -Recurse -Force -File)
    [IO.Directory]::CreateDirectory($backup) | Out-Null
    foreach ($file in $files) {
        $rel=$file.FullName.Substring($sourceRoot.Length).TrimStart('\','/')
        if ($rel -match '(^|[\\/])(?:\.git|node_modules|dist|_site)([\\/]|$)') {throw "Unexpected archive file: $rel"}
        $target=Join-Path $ProjectRoot $rel
        if (Test-Path -LiteralPath $target -PathType Leaf) {
            $saved=Join-Path $backup $rel
            [IO.Directory]::CreateDirectory((Split-Path -Parent $saved)) | Out-Null
            Copy-Item -LiteralPath $target -Destination $saved -Force
        }
        [IO.Directory]::CreateDirectory((Split-Path -Parent $target)) | Out-Null
        Copy-Item -LiteralPath $file.FullName -Destination $target -Force
    }
    foreach($obsolete in @('app.v4005.js','browser-compat.v4005.js','release-bootstrap.v4005.js')) {
        $target=Join-Path (Join-Path $ProjectRoot 'assets') $obsolete
        if (Test-Path -LiteralPath $target -PathType Leaf) {
            $saved=Join-Path (Join-Path $backup 'assets') $obsolete
            [IO.Directory]::CreateDirectory((Split-Path -Parent $saved)) | Out-Null
            Move-Item -LiteralPath $target -Destination $saved -Force
        }
    }
    Push-Location -LiteralPath $ProjectRoot
    try {
        & python -B tools\quality_gate.py
        if ($LASTEXITCODE -ne 0) {throw "Post-install quality gate failed; overwritten files backed up in: $backup"}
    } finally {Pop-Location}
    Write-Host "PASS installed VulkanScope Database 4.0.7 at $ProjectRoot"
    Write-Host "Backups: $backup"
    Write-Host 'Git commit/push and Cloudflare Worker deployment are separate manual operations.'
} finally {
    if (Test-Path -LiteralPath $stage) {Remove-Item -LiteralPath $stage -Recurse -Force}
}
