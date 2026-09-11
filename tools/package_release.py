from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, subprocess, sys, tempfile, zipfile

parser = argparse.ArgumentParser(description='Build a deterministic strict VulkanScope Database source release')
parser.add_argument('out_dir', nargs='?', default='dist')
parser.add_argument('--root', default=None, help='Source checkout root (test/fixture override)')
args = parser.parse_args()

root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
out_dir = Path(args.out_dir)
if not out_dir.is_absolute():
    out_dir = (Path.cwd() / out_dir).resolve()
out_dir.mkdir(parents=True, exist_ok=True)

# A long-lived/tagged Git checkout may contain legitimate historical tracked source files
# that were never part of the immutable predecessor release ZIP. Validate predecessor
# ownership in source-overlay mode here; strict-tree applies only to the actual package.
subprocess.run([sys.executable, str(root/'tools/repair_repository.py'), '--check'], cwd=root, check=True)
subprocess.run([sys.executable, str(root/'tools/verify_regression_contract.py')], cwd=root, check=True)

contract_path = root/'regression/1.0.12_to_1.0.13_contract.json'
contract = json.loads(contract_path.read_text(encoding='utf-8'))
manifest = json.loads((root/contract['baselineManifest']).read_text(encoding='utf-8'))
paths = {x['path'] for x in manifest['files']}
paths.difference_update(contract.get('allowedRemoved', []))
paths.update(contract.get('allowedNew', []))
paths.discard('worker/package-lock.json')
paths = set(sorted(paths))

missing = sorted(rel for rel in paths if not (root/rel).is_file())
if missing:
    raise SystemExit('release package missing files: ' + ', '.join(missing))

zip_path = out_dir / 'VulkanScope-Database-1.0.13.zip'
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for rel in sorted(paths):
        data = (root/rel).read_bytes()
        zi = zipfile.ZipInfo(rel, (1980, 1, 1, 0, 0, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = (0o100644 & 0xFFFF) << 16
        zi.create_system = 3
        zf.writestr(zi, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

# Strict-package verification happens against a clean extract, not the history-bearing
# tagged checkout. This is the key source-overlay/package boundary.
with tempfile.TemporaryDirectory(prefix='vulkanscope-db-release-1.0.13-') as td:
    extracted = Path(td) / 'release'
    extracted.mkdir()
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        if len(names) != len(set(names)):
            raise SystemExit('release ZIP contains duplicate path names')
        zf.extractall(extracted)

    actual = sorted(p.relative_to(extracted).as_posix() for p in extracted.rglob('*') if p.is_file())
    expected = sorted(paths)
    if actual != expected:
        extra = sorted(set(actual)-set(expected))
        lost = sorted(set(expected)-set(actual))
        raise SystemExit(f'clean-extract path mismatch extra={extra} missing={lost}')

    for rel in expected:
        if (extracted/rel).read_bytes() != (root/rel).read_bytes():
            raise SystemExit(f'clean-extract/source byte mismatch: {rel}')

    subprocess.run(
        [sys.executable, str(extracted/'tools/verify_regression_contract.py'), '--strict-tree'],
        cwd=extracted, check=True
    )
    subprocess.run(
        [sys.executable, str(extracted/'tools/verify_1_0_13_reports_disclosure_spray_ui.py')],
        cwd=extracted, check=True
    )
    subprocess.run(
        [sys.executable, str(extracted/'tools/test_1_0_13_reports_disclosure_spray_ui_negative_mutations.py')],
        cwd=extracted, check=True
    )

digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
sha_path = out_dir / (zip_path.name + '.sha256')
sha_path.write_text(f'{digest}  {zip_path.name}\n', encoding='ascii', newline='\n')
print(f'Built {zip_path} files={len(paths)} sha256={digest} clean-extract=strict-PASS')
