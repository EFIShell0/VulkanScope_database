param(
    [Parameter(Mandatory=$false)][string]$Repo = "."
)
$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $Repo
$python = Get-Command py -ErrorAction SilentlyContinue
if ($python) {
    & py -3 tools\repair_repository.py --apply
    & py -3 tools\audit_database.py --source-tree .
} else {
    $python = Get-Command python -ErrorAction Stop
    & python tools\repair_repository.py --apply
    & python tools\audit_database.py --source-tree .
}
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "VulkanScope Database 0.39.4 repository repair finished."
