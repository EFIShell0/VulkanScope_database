#Requires -Version 5.1
[CmdletBinding()]
param(
 [string]$Zip = (Join-Path $env:USERPROFILE 'Downloads\VulkanScope-Database-4.0.3.zip'),
 [string]$Destination = '',
 [string]$Sha256 = ''
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
function Invoke-Checked([string]$Exe,[string[]]$CmdArgs) {
 & $Exe @CmdArgs
 if ($LASTEXITCODE -ne 0) { throw "FAIL $Exe $($CmdArgs -join ' ') (exit $LASTEXITCODE)" }
}
function Hash([string]$File) { (Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant() }
# NEVER read or mutate the old repository; it contains user stashes/edits.
$Zip = [IO.Path]::GetFullPath($Zip)
if (-not [IO.File]::Exists($Zip)) { throw "Missing ZIP: $Zip" }
if (-not $Sha256) {
 $sf="$Zip.sha256"
 if (-not [IO.File]::Exists($sf)) { throw "Provide -Sha256 or download companion .sha256: $sf" }
 $line=[IO.File]::ReadAllText($sf).Trim()
 if ($line -match '^([0-9a-fA-F]{64})\s+VulkanScope-Database-4\.0\.3\.zip$') { $Sha256=$Matches[1] }
 else { throw 'Invalid checksum manifest' }
}
if ((Hash $Zip) -ne $Sha256.ToLowerInvariant()) { throw 'ZIP checksum mismatch' }
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive=[IO.Compression.ZipFile]::OpenRead($Zip)
try {
 $entries=@($archive.Entries | Where-Object { -not $_.FullName.EndsWith('/') })
 $seen=[System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
 foreach($e in $entries) {
   $rel=$e.FullName.Replace('\','/')
   if (-not $rel -or $rel.StartsWith('/') -or $rel.Contains(':') -or $rel -match '(^|/)\.\.?(/|$)' -or -not $seen.Add($rel)) { throw "Unsafe entry: $rel" }
 }
 if ($entries.Count -lt 850) {throw "Unexpectedly incomplete ZIP: $($entries.Count) files"}
 # Detect schema markers in ARCHIVE, not by trusting extracted working directories.
 foreach($must in @('tools/verify_4_0_3_checkout.py','tools/verify_4_0_3_layout.py','index.html','rules/PROJECT_RULES.md','.github/workflows/pages.yml')) {
   if (-not $seen.Contains($must)) { throw "Missing canonical source: $must" }
 }
 if ($Destination) { $dest=[IO.Path]::GetFullPath($Destination) }
 else {
   $tag=Get-Date -Format 'yyyyMMdd-HHmmss'
   $dest=Join-Path (Join-Path $env:USERPROFILE 'Desktop') ("VulkanScope_database_clean_403_"+$tag)
 }
 if ([IO.Directory]::Exists($dest) -or [IO.File]::Exists($dest)) {throw "Destination already exists: $dest"}
 $parent=Split-Path -Parent $dest
 if (-not [IO.Directory]::Exists($parent)) { [IO.Directory]::CreateDirectory($parent) | Out-Null }
 # Git repository clone from confirmed user-reported origin; old checkout is not touched.
 Invoke-Checked git @('clone','--branch','main','--single-branch','https://github.com/EFIShell0/VulkanScope_database.git',$dest)
 $origin=(& git -C $dest remote get-url origin).Trim()
 if ($LASTEXITCODE -ne 0 -or $origin -notmatch '^https://github\.com/EFIShell0/VulkanScope_database(?:\.git)?$') {throw 'Unexpected origin'}
 # Remove only fully duplicated source roots in FRESH CLONE. Never touch old checkout or its stash.
 $polluted=@()
 foreach($dir in @(Get-ChildItem -LiteralPath $dest -Directory -Force)) {
   $n=$dir.Name
   if ($n -in @('.git','assets','tools','worker','data','registry','rules','regression','licenses','compat','.github')) {continue}
   $markers=@('tools/repair_repository.py','tools/audit_database.py','data/release.json','rules/PROJECT_RULES.md')
   $found=0
   foreach($m in $markers) {if ([IO.File]::Exists((Join-Path $dir.FullName $m))) {$found++}}
   if ($found -eq $markers.Count) {
       if ($n -notmatch '^[0-9a-fA-F]{5,40}$') {throw "Unexpected nested source directory name, manual review required: $n"}
       # Git checkout was just freshly cloned. Confirm all files tracked before safely removing clone-only subtree.
       $all=@(Get-ChildItem -LiteralPath $dir.FullName -File -Recurse -Force)
       $tracked=@(& git -C $dest ls-files -- $n)
       if ($LASTEXITCODE -ne 0 -or $tracked.Count -ne $all.Count) {throw "Nested clone contains untracked/unknown files: $n"}
       $polluted += $n
   }
 }
 foreach($n in $polluted) { Invoke-Checked git @('-C',$dest,'rm','-r','--',$n) }
 # Remove exclusively declared old files, never tracked unknown files.
 $remove=@('assets/app.v4001.js','assets/browser-compat.v4001.js','assets/release-bootstrap.v4001.js')
 foreach($rel in $remove) {
   $p=Join-Path $dest $rel
   if ([IO.File]::Exists($p)) { Invoke-Checked git @('-C',$dest,'rm','-f','--',$rel) }
 }
 # Decode ZIP entries directly to destination/$ENTRY.FullName. No temp folder substring logic.
 $canonical=$dest.TrimEnd('\','/')+[IO.Path]::DirectorySeparatorChar
 $count=0
 foreach($e in $entries) {
   $rel=$e.FullName.Replace('/',[IO.Path]::DirectorySeparatorChar)
   $file=[IO.Path]::GetFullPath((Join-Path $dest $rel))
   if (-not $file.StartsWith($canonical,[StringComparison]::OrdinalIgnoreCase)) {throw "Path escaped clone root: $rel"}
   $dir=[IO.Path]::GetDirectoryName($file)
   [IO.Directory]::CreateDirectory($dir) | Out-Null
   $source=$e.Open()
   try {
     $output=[IO.File]::Open($file,[IO.FileMode]::Create,[IO.FileAccess]::Write,[IO.FileShare]::None)
     try { $source.CopyTo($output) } finally { $output.Dispose() }
   } finally { $source.Dispose() }
   $count++
 }
 Write-Host "PASS wrote $count ZIP entries at canonical root $dest" -ForegroundColor Green
} finally { $archive.Dispose() }
# These checks run before any other mutating repair. The layout failure now fails closed.
foreach($p in @('tools\verify_4_0_3_checkout.py','tools\verify_4_0_3_layout.py','.github\workflows\pages.yml')) {
 if (-not [IO.File]::Exists((Join-Path $dest $p))) {throw "Canonical-root file absent: $p"}
}
Push-Location $dest
try {
 Invoke-Checked python @('-B','tools\verify_4_0_3_layout.py')
 Invoke-Checked python @('-B','tools\verify_4_0_3_checkout.py')
 Invoke-Checked python @('-B','tools\repair_repository.py','--apply')
 Invoke-Checked python @('-B','tools\quality_gate.py')
 Invoke-Checked python @('-B','tools\package_release.py',(Join-Path $env:TEMP 'vsdb403-release-check') )
 Invoke-Checked git @('add','-A')
 Invoke-Checked git @('diff','--cached','--check')
 Write-Host 'PASS: CLEAN 4.0.3 checkout staged; no commit/push performed.' -ForegroundColor Green
 Write-Host "CLEAN_REPOSITORY=$dest"
 Invoke-Checked git @('status','--short')
} finally {Pop-Location}
