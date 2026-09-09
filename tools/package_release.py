from __future__ import annotations
from pathlib import Path
import hashlib, json, subprocess, sys, zipfile

root = Path(__file__).resolve().parents[1]
out_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else (root / 'dist')
out_dir.mkdir(parents=True, exist_ok=True)

subprocess.run([sys.executable, str(root/'tools/repair_repository.py'), '--check'], cwd=root, check=True)
subprocess.run([sys.executable, str(root/'tools/verify_regression_contract.py'), '--strict-tree'], cwd=root, check=True)

contract = json.loads((root/'regression/1.0.6_to_1.0.7_contract.json').read_text(encoding='utf-8'))
manifest = json.loads((root/contract['baselineManifest']).read_text(encoding='utf-8'))
paths = {x['path'] for x in manifest['files']}
paths.difference_update(contract.get('allowedRemoved', []))
paths.update(contract.get('allowedNew', []))
# Local deployment workspace state is intentionally never part of a source release.
paths.discard('worker/package-lock.json')

missing = sorted(rel for rel in paths if not (root/rel).is_file())
if missing:
    raise SystemExit('release package missing files: ' + ', '.join(missing))

zip_path = out_dir / 'VulkanScope-Database-1.0.7.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for rel in sorted(paths):
        data = (root/rel).read_bytes()
        zi = zipfile.ZipInfo(rel, (1980, 1, 1, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = (0o100644 & 0xFFFF) << 16
        zi.create_system = 3
        zf.writestr(zi, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
sha_path = out_dir / (zip_path.name + '.sha256')
sha_path.write_text(f'{digest}  {zip_path.name}\n', encoding='ascii', newline='\n')
print(f'Built {zip_path} files={len(paths)} sha256={digest}')
