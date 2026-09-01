from pathlib import Path
import argparse, hashlib, json, sys

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description='Verify immutable predecessor regression contract')
parser.add_argument('--strict-tree', action='store_true', help='Reject every file not present in the predecessor or explicit successor allow-list; intended for release ZIP/package verification')
args = parser.parse_args()

cpath = root / 'regression' / '0.39.14_to_0.39.15_contract.json'
c = json.loads(cpath.read_text(encoding='utf-8'))
b = json.loads((root / c['baselineManifest']).read_text(encoding='utf-8'))
bm = {x['path']: x for x in b['files']}
changed = set(c['allowedChanged'])
removed = set(c['allowedRemoved'])
new = set(c['allowedNew'])
self_excluded = set(c.get('selfHashExcluded', []))
generated = set(c.get('generatedSemanticPaths', []))
expected = c['successorSha256']
ignored_paths = set(c.get('ignoredLocalPaths', []))
ignored_dirs = set(c.get('ignoredLocalDirs', []))
errors = []

def ignored(rel: str) -> bool:
    pp = Path(rel)
    return rel in ignored_paths or any(part in ignored_dirs for part in pp.parts)

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def validate_generated(rel: str, p: Path) -> None:
    if rel != 'data/index.json':
        errors.append(f'no semantic validator registered for generated path: {rel}')
        return
    try:
        d = json.loads(p.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'generated {rel} is not valid UTF-8 JSON: {exc}')
        return
    required = {
        'schemaVersion': 1,
        'databaseVersion': '0.39.15',
        'normalizerVersion': 16,
        'publishedVulkanSpec': 'Vulkan 1.4.361 (2026-08-28)',
        'vulkanRegistryBaseline': 'VulkanScope producer/query baseline 1.4.361',
        'producerQueryBaseline': 'VulkanScope 0.41.40 · Vulkan 1.4.361',
        'compatibleProducer': 'VulkanScope 0.32.4+ · schema 2 / technical report 3',
    }
    for k, v in required.items():
        if d.get(k) != v:
            errors.append(f'generated {rel} semantic mismatch {k}: {d.get(k)!r} != {v!r}')
    if not isinstance(d.get('generatedAt'), str) or not d['generatedAt']:
        errors.append(f'generated {rel} missing generatedAt string')
    if not isinstance(d.get('reports'), list):
        errors.append(f'generated {rel} reports must be an array')

# Immutable predecessor-owned paths stay protected in both source-overlay and strict-package modes.
for rel, meta in bm.items():
    p = root / rel
    if rel in removed:
        if p.exists():
            errors.append(f'baseline file should be removed: {rel}')
        continue
    if not p.is_file():
        errors.append(f'baseline file missing unexpectedly: {rel}')
        continue
    if rel in generated:
        validate_generated(rel, p)
        continue
    actual = sha(p)
    if rel in changed:
        if expected.get(rel) != actual:
            errors.append(f'changed successor hash mismatch: {rel}')
    elif actual != meta['sha256']:
        errors.append(f'unallowlisted predecessor regression: {rel}')

# Explicit successor additions must always exist and match.
for rel in new:
    p = root / rel
    if not p.is_file():
        errors.append(f'allowed new file missing: {rel}')
    elif rel not in self_excluded and rel not in generated and expected.get(rel) != sha(p):
        errors.append(f'new successor hash mismatch: {rel}')

for rel in changed:
    if rel not in bm:
        errors.append(f'allowedChanged is not a baseline path: {rel}')

# A real Git checkout can legitimately contain history/source files that were not shipped in
# the predecessor release ZIP. Only strict release-package verification rejects such extras.
if args.strict_tree:
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if ignored(rel) or rel in bm or rel in new:
            continue
        errors.append(f'unallowlisted release-package file: {rel}')

if errors:
    print('\n'.join('FAIL ' + x for x in errors))
    raise SystemExit(1)
mode = 'strict-package' if args.strict_tree else 'source-overlay'
print(f"PASS regression contract mode={mode} baseline={c['baseline']} successor={c['successor']} baselineFiles={len(bm)} changed={len(changed)} removed={len(removed)} new={len(new)} generated={len(generated)}")
