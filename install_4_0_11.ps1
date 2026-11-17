#Requires -Version 5.1
<#
VulkanScope Database 4.0.11 - safe in-place source upgrade.
Source archive and checksum must both be in Downloads (or explicit -Archive).
- Verifies ZIP digest and entries before extraction.
- Requires clean main checkout; tests package before touching source.
- Backs up every overwritten/deleted file OUTSIDE the repository.
- On install failure, restores originals and removes new files.
- Does not commit, push, run D1 migration, or deploy Cloudflare.
#>
[CmdletBinding()]
param(
    [string]$Archive = (Join-Path $env:USERPROFILE 'Downloads\VulkanScope-Database-4.0.11.zip'),
    [string]$ProjectRoot = (Join-Path $env:USERPROFILE 'Desktop\VulkanScope_database')
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$Archive = [IO.Path]::GetFullPath($Archive)
$ProjectRoot = [IO.Path]::GetFullPath($ProjectRoot)
$repoName = [IO.Path]::GetFileName($ProjectRoot.TrimEnd([char[]]@('\','/')))
if ($repoName -cne 'VulkanScope_database') { throw 'Expected the existing VulkanScope_database repository.' }
if (-not (Test-Path -LiteralPath $Archive -PathType Leaf)) { throw "Missing ZIP: $Archive" }
$checksumPath = "$Archive.sha256"
if (-not (Test-Path -LiteralPath $checksumPath -PathType Leaf)) { throw "Missing SHA256 file: $checksumPath" }
$checksumText = [IO.File]::ReadAllText($checksumPath).Trim()
if ($checksumText -cnotmatch '^([A-Fa-f0-9]{64})\s+VulkanScope-Database-4\.0\.11\.zip$') { throw 'Invalid companion ZIP checksum format.' }
$expectedHash = $Matches[1]
$actualHash = (Get-FileHash -LiteralPath $Archive -Algorithm SHA256).Hash
if ($actualHash -ine $expectedHash) { throw 'SHA256 mismatch. No files have been changed.' }
if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot '.git') -PathType Container)) { throw 'Existing Git checkout not found.' }
if (((Get-Item -LiteralPath $ProjectRoot).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Symlinked repository root is forbidden.' }
$branch = @(& git -C $ProjectRoot branch --show-current)
if ($LASTEXITCODE -ne 0 -or ($branch -join '') -cne 'main') { throw 'Switch to the main branch before installation.' }
$origin = @(& git -C $ProjectRoot remote get-url origin)
if ($LASTEXITCODE -ne 0 -or ($origin -join '') -notmatch '^(https://github\.com/EFIShell0/VulkanScope_database(?:\.git)?/?|git@github\.com:EFIShell0/VulkanScope_database(?:\.git)?)$') {
    throw 'Unexpected Git origin. Verify the GitHub repository; nothing was installed.'
}
$dirty = @(& git -C $ProjectRoot status --porcelain)
if ($LASTEXITCODE -ne 0 -or $dirty.Count -gt 0) { throw 'Git checkout is not clean. Commit or manually back up local changes first.' }
# Strict archive inventory: no duplicate / traversal / drive / ADS / symlink entries.
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [IO.Compression.ZipFile]::OpenRead($Archive)
try {
    $names = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($entry in $zip.Entries) {
        $name = $entry.FullName
        if (-not $name -or $name.EndsWith('/') -or $name.Contains('\') -or $name.StartsWith('/') -or $name.Contains(':') -or $name -match '(^|/)\.{1,2}(/|$)') {
            throw "Unsupported ZIP entry: $name"
        }
        if (-not $names.Add($name)) { throw "Duplicate ZIP entry: $name" }
        $unixMode = ($entry.ExternalAttributes -shr 16) -band 61440
        if ($unixMode -eq 41060) { throw "ZIP symlink entry is forbidden: $name" }
    }
    foreach ($required in @('rules/PROJECT_RULES.md','tools/quality_gate.py','install_4_0_11.ps1','assets/app.v4011.js','assets/browser-compat.v4011.js')) {
        if (-not $names.Contains($required)) { throw "ZIP missing required release file: $required" }
    }
} finally { $zip.Dispose() }
# Deletions are explicit files in the audited predecessor and never wildcards.
$retire = @(
    'BUILD_AUDIT.md'
    'UPDATE_0.39.3.md'
    'UPDATE_0.39.4.md'
    'UPDATE_0.39.5.md'
    'UPDATE_0.39.6.md'
    'UPDATE_0.39.7.md'
    'UPDATE_0.39.8.md'
    'UPDATE_4.0.6.md'
    'UPDATE_4.0.7.md'
    'assets\app.v4005.js'
    'assets\app.v4006.js'
    'assets\browser-compat.v4005.js'
    'assets\browser-compat.v4006.js'
    'assets\encyclopedia.v1412.js'
    'assets\encyclopedia.v4001.js'
    'assets\encyclopedia.v4002.js'
    'assets\encyclopedia.v4003.js'
    'assets\encyclopedia.v4004.js'
    'assets\encyclopedia.v4005.js'
    'assets\encyclopedia.v4006.js'
    'assets\encyclopedia.v4008.js'
    'assets\jxl-probe.v4000.jxl'
    'assets\jxl-probe.v4001.jxl'
    'assets\jxl-probe.v4002.jxl'
    'assets\jxl-probe.v4003.jxl'
    'assets\jxl-probe.v4004.jxl'
    'assets\jxl-probe.v4005.jxl'
    'assets\jxl-probe.v4006.jxl'
    'assets\release-bootstrap.v4005.js'
    'assets\release-bootstrap.v4006.js'
    'assets\site.v0390.css'
    'assets\site.v1308.css'
    'assets\site.v1309.css'
    'assets\site.v1400.css'
    'assets\site.v1401.css'
    'assets\site.v1402.css'
    'assets\site.v1403.css'
    'assets\site.v1404.css'
    'assets\site.v1405.css'
    'assets\site.v1406.css'
    'assets\site.v1407.css'
    'assets\site.v1408.css'
    'assets\site.v1410.css'
    'assets\site.v1411.css'
    'assets\site.v1412.css'
    'assets\site.v1413.css'
    'assets\site.v4000.css'
    'assets\site.v4001.css'
    'assets\site.v4002.css'
    'assets\site.v4003.css'
    'assets\site.v4004.css'
    'assets\site.v4005.css'
    'assets\site.v4006.css'
    'install_4_0_5.ps1'
    'install_4_0_6.ps1'
    'install_4_0_7.ps1'
    'install_4_0_8.ps1'
    'install_4_0_9.ps1'
    'UPDATE_4.0.8.md'
    'UPDATE_4.0.9.md'
    'UPDATE_4.0.10.md'
    'install_4_0_10.ps1'
    'assets\app.v4009.js'
    'assets\browser-compat.v4009.js'
    'assets\release-bootstrap.v4009.js'
    'assets\site.v4009.css'
    'assets\jxl-probe.v4009.jxl'
    'assets\app.v4008.js'
    'assets\browser-compat.v4008.js'
    'assets\release-bootstrap.v4008.js'
    'assets\site.v4008.css'
    'assets\jxl-probe.v4008.jxl'
    'assets\app.v4007.js'
    'assets\browser-compat.v4007.js'
    'assets\release-bootstrap.v4007.js'
    'assets\site.v4007.css'
    'assets\jxl-probe.v4007.jxl'
)
$staging = Join-Path ([IO.Path]::GetTempPath()) ('VulkanScope_DB_411_'+[Guid]::NewGuid().ToString('N'))
$backupRoot = Join-Path (Split-Path -Parent $ProjectRoot) 'VulkanScope_database-backups'
$backup = Join-Path $backupRoot ((Get-Date -Format 'yyyyMMdd_HHmmss')+'_'+[Guid]::NewGuid().ToString('N').Substring(0,6))
$created = New-Object 'System.Collections.Generic.List[string]'
$existing = New-Object 'System.Collections.Generic.List[string]'
$changed = $false
New-Item -ItemType Directory -Path $staging -Force | Out-Null
try {
    Expand-Archive -LiteralPath $Archive -DestinationPath $staging -Force
    Push-Location -LiteralPath $staging
    try {
        & python -B tools\quality_gate.py
        if ($LASTEXITCODE -ne 0) { throw 'Extracted ZIP failed quality gate; no repository files modified.' }
    } finally { Pop-Location }
    $files = @(Get-ChildItem -LiteralPath $staging -Force -Recurse -File)
    $stagePrefix = $staging.TrimEnd([char[]]@('\','/')) + [IO.Path]::DirectorySeparatorChar
    $incoming = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($file in $files) {
        $relative = $file.FullName.Substring($stagePrefix.Length)
        if ($relative -match '(^|[\\/])(?:\.git|node_modules|dist|_site)([\\/]|$)') { throw "Forbidden path in package: $relative" }
        [void]$incoming.Add($relative)
    }
    foreach ($relative in $retire) {
        if ($incoming.Contains($relative)) { throw "Removal conflict inside ZIP: $relative" }
    }
    # Preflight all paths before touching working tree.
    $allTargets = @($files | ForEach-Object { $_.FullName.Substring($stagePrefix.Length) }) + @($retire)
    foreach ($relative in $allTargets) {
        $target = Join-Path $ProjectRoot $relative
        if (Test-Path -LiteralPath $target) {
            $item = Get-Item -LiteralPath $target -Force
            if ($item.PSIsContainer -or (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)) {
                throw "Unsafe destination path (directory/link): $relative"
            }
        }
    }
    New-Item -ItemType Directory -Path $backup -Force | Out-Null
    # Backup first, including retired files. Backups remain after successful install.
    foreach ($relative in $allTargets) {
        $target = Join-Path $ProjectRoot $relative
        if (Test-Path -LiteralPath $target -PathType Leaf) {
            $saved = Join-Path $backup $relative
            New-Item -ItemType Directory -Path (Split-Path -Parent $saved) -Force | Out-Null
            Copy-Item -LiteralPath $target -Destination $saved -Force
            $existing.Add($relative)
        } else { $created.Add($relative) }
    }
    $changed = $true
    foreach ($file in $files) {
        $relative = $file.FullName.Substring($stagePrefix.Length)
        $target = Join-Path $ProjectRoot $relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
        Copy-Item -LiteralPath $file.FullName -Destination $target -Force
    }
    foreach ($relative in $retire) {
        $target = Join-Path $ProjectRoot $relative
        if (Test-Path -LiteralPath $target -PathType Leaf) { Remove-Item -LiteralPath $target -Force }
    }
    Push-Location -LiteralPath $ProjectRoot
    try {
        & python -B tools\quality_gate.py
        if ($LASTEXITCODE -ne 0) { throw 'Post-install quality gate failed.' }
        & git diff --check
        if ($LASTEXITCODE -ne 0) { throw 'Git whitespace validation failed.' }
    } finally { Pop-Location }
    $changed = $false
    Write-Host 'PASS: VulkanScope Database 4.0.11 installed in the original checkout.' -ForegroundColor Green
    Write-Host "Originals backed up in: $backup"
    Write-Host 'Next: git add/commit/push; GitHub Actions; explicit Cloudflare Worker deployment.'
} catch {
    if ($changed) {
        Write-Warning "Installation failed. Restoring files from: $backup"
        foreach ($relative in $created) {
            $target = Join-Path $ProjectRoot $relative
            if (Test-Path -LiteralPath $target -PathType Leaf) { Remove-Item -LiteralPath $target -Force }
        }
        foreach ($relative in $existing) {
            $saved = Join-Path $backup $relative
            $target = Join-Path $ProjectRoot $relative
            if (Test-Path -LiteralPath $saved -PathType Leaf) {
                New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
                Copy-Item -LiteralPath $saved -Destination $target -Force
            }
        }
    }
    throw
} finally {
    if (Test-Path -LiteralPath $staging) { Remove-Item -LiteralPath $staging -Recurse -Force }
}
