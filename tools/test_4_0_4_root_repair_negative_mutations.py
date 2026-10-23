from pathlib import Path
import subprocess,sys,tempfile,shutil,json
root=Path(__file__).resolve().parents[1]
s=(root/'install_4_0_4.ps1').read_text(encoding='utf-8')
for key in ["$basename -eq 'VulkanScope_database'","'--strict-tree'","-NewName ([IO.Path]::GetFileName($backup))",'Rename-Item -LiteralPath $staging -NewName $basename',"'--cached','--check'", "'tools\\quality_gate.py'", "'tools\\package_release.py'", 'ORIGINAL_BACKUP=', 'ORIGINAL_BACKUP', '4.0.3_to_4.0.4_contract.json', 'Join-Path $unpacked', 'Set-Location -LiteralPath $parent']:
    if key not in s:raise SystemExit('FAIL missing protected canonical path installer operation: '+key)
if 'stash pop' in s or 'git reset --hard' in s or 'git clean -fd' in s or "Invoke-Checked git @('push'" in s:
    raise SystemExit('FAIL destructive or auto-publish operation in installer')
base=json.loads((root/'regression/4.0.3_to_4.0.4_contract.json').read_text(encoding='utf-8'))
retired={'install_4_0_0.ps1','install_4_0_2.ps1','install_4_0_3.ps1'}
assert retired <= set(base['allowedRemoved'])
for rel in retired:
    assert not (root/rel).exists()
assert (root/'install_4_0_4.ps1').is_file()
print('PASS 4.0.4 canonical-root installer: preserved original checkout, explicit obsolete installer removals, fail-closed staging gates')
