# VulkanScope Database 4.0.6: non-recursive, in-place source overlay preserving .git.
[CmdletBinding()]
param(
    [string]$Archive = (Join-Path $env:USERPROFILE 'Downloads\VulkanScope-Database-4.0.6.zip'),
    [string]$ProjectRoot = (Join-Path $env:USERPROFILE 'Desktop\VulkanScope_database'),
    [switch]$AllowDirty
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Archive -PathType Leaf)) { throw "Missing archive: $Archive" }
if (-not (Test-Path -LiteralPath (Join-Path $ProjectRoot '.git'))) { throw "Not a Git working tree: $ProjectRoot" }
$changes = @(git -C $ProjectRoot status --porcelain --untracked-files=no 2>$null)
if ($LASTEXITCODE -ne 0) { throw 'Could not inspect existing Git working tree.' }
if ($changes.Count -gt 0 -and -not $AllowDirty) {
    throw 'Tracked local changes detected; use -AllowDirty only if you intend to overwrite project files. Existing overwritten files are backed up first.'
}
$stage = Join-Path ([System.IO.Path]::GetTempPath()) ('VulkanScope_DB_406_' + [guid]::NewGuid().ToString('N'))
$backup = Join-Path (Join-Path $env:USERPROFILE 'Downloads') ('VulkanScope_DB_backup_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
New-Item -ItemType Directory -Path $stage,$backup -Force | Out-Null
try {
    Expand-Archive -LiteralPath $Archive -DestinationPath $stage -Force
    if (-not (Test-Path -LiteralPath (Join-Path $stage 'tools\verify_4_0_6_release.py'))) { throw 'Archive layout is not the expected flat Database source root.' }
    $sourceRoot = (Resolve-Path -LiteralPath $stage).Path.TrimEnd('\','/')
    $files = @(Get-ChildItem -LiteralPath $sourceRoot -Recurse -Force -File)
    foreach ($file in $files) {
        $rel = $file.FullName.Substring($sourceRoot.Length).TrimStart('\','/')
        if ($rel -match '(^|[\\/])\.git([\\/]|$)') { throw 'Archive unexpectedly contains .git content.' }
        $dest = Join-Path $ProjectRoot $rel
        if (Test-Path -LiteralPath $dest -PathType Leaf) {
            $old = Join-Path $backup $rel
            New-Item -ItemType Directory -Path (Split-Path $old -Parent) -Force | Out-Null
            Copy-Item -LiteralPath $dest -Destination $old -Force
        }
        New-Item -ItemType Directory -Path (Split-Path $dest -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $file.FullName -Destination $dest -Force
    }
    # Obsolete frontend generations are no longer release assets.
    foreach ($name in @('app.v4004.js','browser-compat.v4004.js','release-bootstrap.v4004.js')) {
        $obsolete = Join-Path (Join-Path $ProjectRoot 'assets') $name
        if (Test-Path -LiteralPath $obsolete -PathType Leaf) { Remove-Item -LiteralPath $obsolete -Force }
    }
    Push-Location $ProjectRoot
    try {
        python -B tools\quality_gate.py
        if ($LASTEXITCODE -ne 0) { throw '4.0.6 source quality gate failed. Backup is preserved.' }
    } finally { Pop-Location }
    Write-Host "Database 4.0.6 sources installed and verified in: $ProjectRoot"
    Write-Host "Backup of overwritten source files: $backup"
    Write-Host 'Deployment is separate: commit/push Pages source and deploy Worker with Wrangler.'
}
finally { if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force } }
