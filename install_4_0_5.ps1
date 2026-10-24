#Requires -Version 5.1
<# Safe in-place VulkanScope Database 4.0.5 installer.
    Updates ONLY the established VulkanScope_database directory by a validated
    local Git fast-forward. It never renames the folder or runs reset/clean.
    Old stashes and local edits are preserved. No automatic remote push.
#>
[CmdletBinding()]
param(
    [string]$Repository = (Join-Path $env:USERPROFILE 'Desktop\VulkanScope_database'),
    [string]$Zip = (Join-Path $env:USERPROFILE 'Downloads\VulkanScope-Database-4.0.5.zip')
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
function Require([bool]$OK,[string]$Message) { if (-not $OK) { throw $Message } }
function Git([string]$Dir,[string[]]$Arguments) {
    & git -C $Dir @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Git failed: git $($Arguments -join ' ')" }
}
function GitRead([string]$Dir,[string[]]$Arguments) {
    $output=@(& git -C $Dir @Arguments)
    if ($LASTEXITCODE -ne 0) { throw "Git read failed: git $($Arguments -join ' ')" }
    return ($output -join "`n").Trim()
}
function Py([string]$Dir,[string[]]$Arguments) {
    Push-Location -LiteralPath $Dir
    try { & python -B @Arguments; if ($LASTEXITCODE -ne 0) { throw "Validation failed: $($Arguments -join ' ')" } }
    finally { Pop-Location }
}
$Repository=[IO.Path]::GetFullPath($Repository).TrimEnd('\','/')
$Zip=[IO.Path]::GetFullPath($Zip)
Require ([IO.Path]::GetFileName($Repository) -ceq 'VulkanScope_database') 'Target must be the existing VulkanScope_database root'
Require ([IO.Directory]::Exists((Join-Path $Repository '.git'))) 'Existing Git checkout not found'
Require (-not (([IO.File]::GetAttributes($Repository) -band [IO.FileAttributes]::ReparsePoint) -ne 0)) 'Repository symlink forbidden'
Require ([IO.File]::Exists($Zip)) "ZIP missing: $Zip"
$shaFile="$Zip.sha256"
Require ([IO.File]::Exists($shaFile)) "SHA-256 companion missing: $shaFile"
$line=[IO.File]::ReadAllText($shaFile).Trim()
Require ($line -match '^([A-Fa-f0-9]{64})\s+VulkanScope-Database-4\.0\.5\.zip$') 'Invalid 4.0.5 SHA-256 companion'
$expectedHash=$Matches[1].ToLowerInvariant()
Require ((Get-FileHash -LiteralPath $Zip -Algorithm SHA256).Hash.ToLowerInvariant() -eq $expectedHash) 'ZIP SHA-256 mismatch'
Require ((GitRead $Repository @('remote','get-url','origin')) -match '^https://github\.com/EFIShell0/VulkanScope_database(?:\.git)?$') 'Wrong GitHub origin'
Require ((GitRead $Repository @('branch','--show-current')) -ceq 'main') 'Expected original branch main'
$sourceHead=GitRead $Repository @('rev-parse','HEAD')
Git $Repository @('fetch','--quiet','origin','main')
Require ((GitRead $Repository @('rev-parse','refs/remotes/origin/main')) -ceq $sourceHead) 'Original main differs from remote main. Stop and reconcile first.'

$base=Join-Path $env:TEMP ('vsdb405-install-'+[guid]::NewGuid().ToString('N'))
$extracted=Join-Path $base 'release'
$staging=Join-Path $base 'staging'
[IO.Directory]::CreateDirectory($extracted) | Out-Null
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zipFile=[IO.Compression.ZipFile]::OpenRead($Zip)
try {
    $seen=New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
    $count=0
    foreach($entry in $zipFile.Entries) {
        $name=$entry.FullName.Replace('\','/')
        Require ($name -notmatch '(^/|//|[\\:]|[<>|?*]|[\x00-\x1f])') "Invalid ZIP path: $name"
        if ($name.EndsWith('/')) { throw "ZIP directory entries forbidden: $name" }
        $parts=@($name.Split('/'))
        foreach($part in $parts) {
            Require ($part -ne '' -and $part -ne '.' -and $part -ne '..') "ZIP traversal: $name"
            Require (-not $part.EndsWith('.') -and -not $part.EndsWith(' ')) "Invalid Windows path: $name"
            Require ($part -notmatch '^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)') "Device path: $name"
        }
        Require ($seen.Add($name)) "Duplicate ZIP path: $name"
        $unixType=($entry.ExternalAttributes -shr 16) -band 0xF000
        Require ($unixType -ne 0xA000) "Symlink refused: $name"
        $target=$extracted
        foreach($part in $parts) { $target=[IO.Path]::Combine($target,$part) }
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($target)) | Out-Null
        $inputStream=$entry.Open()
        try {
            $outputStream=[IO.File]::Open($target,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
            try { $inputStream.CopyTo($outputStream) } finally { $outputStream.Dispose() }
        } finally { $inputStream.Dispose() }
        $count++
    }
} finally { $zipFile.Dispose() }
Require ($count -ge 850) "Incomplete ZIP: $count"
Require ($seen.Contains('regression/4.0.4_to_4.0.5_contract.json')) 'Release contract missing from ZIP'
Py $extracted @('tools\verify_4_0_5_layout.py')
Py $extracted @('tools\verify_4_0_5_checkout.py')
Py $extracted @('tools\verify_4_0_5_regression_contract.py','--strict-tree')
Write-Host "PASS ZIP hash, canonical layout, $count source files and immutable regression contract" -ForegroundColor Green

# Clone ORIGINAL HEAD into a temporary repo; original folder remains untouched until all gates pass.
& git clone --quiet --branch main --no-single-branch $Repository $staging
if ($LASTEXITCODE -ne 0) { throw 'Local staging clone failed' }
Require ((GitRead $staging @('rev-parse','HEAD')) -ceq $sourceHead) 'Staging source HEAD changed'
$contract=Get-Content -LiteralPath (Join-Path $extracted 'regression\4.0.4_to_4.0.5_contract.json') -Raw | ConvertFrom-Json
foreach($rel in @($contract.allowedRemoved)) {
    $f=Join-Path $staging $rel
    if ([IO.File]::Exists($f)) { Git $staging @('rm','-f','--',$rel) }
}
foreach($name in $seen) {
    $src=Join-Path $extracted $name
    $dst=Join-Path $staging $name
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($dst)) | Out-Null
    Copy-Item -LiteralPath $src -Destination $dst -Force
    Require ((Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash -eq (Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash) "Copy hash mismatch: $name"
}
Py $staging @('tools\verify_4_0_5_layout.py')
Py $staging @('tools\verify_4_0_5_checkout.py')
Py $staging @('tools\quality_gate.py')
$releaseDir=Join-Path $base 'verified-release-output'
Py $staging @('tools\package_release.py',$releaseDir)
Git $staging @('add','-A')
Git $staging @('diff','--cached','--check')
Require ((@(& git -C $staging diff --cached --name-only)).Count -gt 0) 'Staging release has no changes'
$sourceAfter=GitRead $Repository @('rev-parse','HEAD')
Require ($sourceAfter -eq $sourceHead) 'Original repository HEAD changed during validation'
$author=GitRead $Repository @('config','user.name')
$email=GitRead $Repository @('config','user.email')
Require ($author.Length -gt 0 -and $email.Length -gt 0) 'Configure git user.name and user.email before release'
Git $staging @('-c',"user.name=$author",'-c',"user.email=$email",'commit','-m','Release VulkanScope Database 4.0.5')
$targetCommit=GitRead $staging @('rev-parse','HEAD')
Write-Host 'PASS staging quality gate, strict release package and staged Git commit' -ForegroundColor Green

# Backup BEFORE applying any changes to original. Never replace/rename target folder.
$backupRoot=Join-Path $env:USERPROFILE 'Downloads\VulkanScope_database_git_backups'
[IO.Directory]::CreateDirectory($backupRoot) | Out-Null
$bundle=Join-Path $backupRoot ('before_405_'+(Get-Date -Format 'yyyyMMdd-HHmmss')+'.bundle')
Git $Repository @('bundle','create',$bundle,'--all')
Require ([IO.File]::Exists($bundle)) 'Git history bundle missing'
$dirty=@(& git -C $Repository status --porcelain)
Require ($LASTEXITCODE -eq 0) 'Could not inspect working copy'
if ($dirty.Count -gt 0) {
    $label='Before-VulkanScope-Database-4.0.5-'+(Get-Date -Format 'yyyyMMdd-HHmmss')
    Git $Repository @('stash','push','--include-untracked','-m',$label)
    Write-Host "PASS local modifications preserved in stash: $label" -ForegroundColor Yellow
}
Require ((@(& git -C $Repository status --porcelain)).Count -eq 0) 'Original working copy is still dirty; aborting before Git update'
Git $Repository @('fetch','--quiet','--no-tags',$staging,'main')
Require ((GitRead $Repository @('rev-parse','FETCH_HEAD')) -ceq $targetCommit) 'Wrong locally fetched commit'
Git $Repository @('merge','--ff-only',$targetCommit)
Require ((GitRead $Repository @('rev-parse','HEAD')) -ceq $targetCommit) 'Fast-forward did not land on approved commit'
Py $Repository @('tools\verify_4_0_5_checkout.py')
Py $Repository @('tools\quality_gate.py')
Write-Host 'PASS: VulkanScope Database 4.0.5 installed IN PLACE; permanent folder was never renamed.' -ForegroundColor Green
Write-Host "REPOSITORY=$Repository"
Write-Host "HISTORY_BACKUP=$bundle"
Write-Host 'No GitHub push, D1 migration or Cloudflare deploy was performed.'
