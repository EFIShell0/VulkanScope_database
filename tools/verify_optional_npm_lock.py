from pathlib import Path
import json, sys

root = Path(__file__).resolve().parents[1]
lock = root / 'worker' / 'package-lock.json'
if not lock.is_file():
    print('SKIP optional worker/package-lock.json not packaged; existing deployment workspace lock may be validated when present')
    raise SystemExit(0)

errors=[]
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
want='4.125.0'
root_wr=(rootpkg.get('devDependencies') or {}).get('wrangler')
if root_wr != want:
    errors.append(f'root wrangler pin {root_wr!r} != {want}')
wr=packages.get('node_modules/wrangler') or {}
if wr.get('version') != want:
    errors.append(f"resolved wrangler version {wr.get('version')!r} != {want}")
if not wr.get('integrity'):
    errors.append('resolved wrangler package missing integrity hash')
if errors:
    print('\n'.join('FAIL '+x for x in errors)); raise SystemExit(1)
print(f'PASS optional npm lock wrangler={want} lockfileVersion={data.get("lockfileVersion")}')
