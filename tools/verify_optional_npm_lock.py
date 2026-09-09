from pathlib import Path
import json, sys

root = Path(__file__).resolve().parents[1]
pkg_path = root / 'worker' / 'package.json'
lock = root / 'worker' / 'package-lock.json'
want = '4.130.0'
want_sharp = '0.35.4'
errors=[]

try:
    pkg=json.loads(pkg_path.read_text(encoding='utf-8'))
except Exception as exc:
    print(f'FAIL worker/package.json is not valid UTF-8 JSON: {exc}')
    raise SystemExit(1)
root_pin=(pkg.get('devDependencies') or {}).get('wrangler')
if root_pin != want:
    errors.append(f'worker/package.json wrangler pin {root_pin!r} != {want}')
if (pkg.get('overrides') or {}).get('sharp') != want_sharp:
    errors.append(f"worker/package.json sharp override {(pkg.get('overrides') or {}).get('sharp')!r} != {want_sharp}")

if not lock.is_file():
    if errors:
        print('\n'.join('FAIL '+x for x in errors)); raise SystemExit(1)
    print(f'PASS optional npm lock absent; canonical worker/package.json wrangler={want} sharpOverride={want_sharp}')
    raise SystemExit(0)

try:
    data=json.loads(lock.read_text(encoding='utf-8'))
except Exception as exc:
    print(f'FAIL worker/package-lock.json is not valid UTF-8 JSON: {exc}')
    raise SystemExit(1)
if int(data.get('lockfileVersion',0) or 0) < 2:
    errors.append('lockfileVersion must be >= 2')
packages=data.get('packages') or {}
rootpkg=packages.get('') or {}
if rootpkg.get('name') not in (None,'vulkanscope-database-worker'):
    errors.append(f"unexpected root package name {rootpkg.get('name')!r}")
root_wr=(rootpkg.get('devDependencies') or {}).get('wrangler')
if root_wr != want:
    errors.append(f'lock root wrangler pin {root_wr!r} != {want}')
wr=packages.get('node_modules/wrangler') or {}
if wr.get('version') != want:
    errors.append(f"resolved wrangler version {wr.get('version')!r} != {want}")
if not wr.get('integrity'):
    errors.append('resolved wrangler package missing integrity hash')
sharp=packages.get('node_modules/sharp') or {}
if sharp.get('version') != want_sharp:
    errors.append(f"resolved sharp version {sharp.get('version')!r} != {want_sharp}")
if not sharp.get('integrity'):
    errors.append('resolved sharp package missing integrity hash')
if errors:
    print('\n'.join('FAIL '+x for x in errors))
    print('FAIL stale optional lock: run `python tools/repair_repository.py --apply` before the release quality gate, then run `npm install` in worker to create a fresh audited workspace lock.')
    raise SystemExit(1)
print(f'PASS optional npm lock wrangler={want} sharp={want_sharp} lockfileVersion={data.get("lockfileVersion")}')
