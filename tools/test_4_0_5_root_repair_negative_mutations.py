from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
script=(root/'install_4_0_5.ps1').read_text(encoding='utf-8')
for token in ('VulkanScope_database', 'Get-FileHash', 'git', 'stash', 'bundle', 'fetch', 'merge', '--ff-only', 'verify_4_0_5_checkout.py', 'quality_gate.py', 'regression/4.0.4_to_4.0.5_contract.json'):
    if token not in script:raise SystemExit('FAIL missing in-place installer guard: '+token)
for token in ('git reset --hard', 'git clean -fd', 'stash pop', 'Rename-Item -LiteralPath $Repository', 'push origin main'):
    if token in script:raise SystemExit('FAIL unsafe installer operation: '+token)
contract=json.loads((root/'regression/4.0.4_to_4.0.5_contract.json').read_text(encoding='utf-8'))
assert 'install_4_0_4.ps1' in contract['allowedRemoved']
assert not (root/'install_4_0_4.ps1').exists()
assert (root/'install_4_0_5.ps1').is_file()
print('PASS 4.0.5 safe original-root in-place Git installer: no rename/reset/clean/auto-push')
