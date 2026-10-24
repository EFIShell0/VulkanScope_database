from __future__ import annotations
from pathlib import Path
import argparse,hashlib,json
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description='Verify immutable VulkanScope Database 4.0.4 predecessor ownership and 4.0.5 successor allow-list')
p.add_argument('--strict-tree',action='store_true')
a=p.parse_args()
c=json.loads((root/'regression/4.0.4_to_4.0.5_contract.json').read_text(encoding='utf-8'))
b=json.loads((root/c['baselineManifest']).read_text(encoding='utf-8'))
baseline={f['path']:f for f in b['files']};changed=set(c['allowedChanged']);removed=set(c['allowedRemoved']);added=set(c['allowedNew']);hashes=c['successorSha256'];self_excluded=set(c.get('selfHashExcluded',[]));generated=set(c.get('generatedSemanticPaths',[]));errors=[]
def fail(message):errors.append(message)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
if changed&removed or changed&added or removed&added:fail('overlapping change/remove/add categories')
if any(x not in baseline for x in changed|removed):fail('changed/removed path missing from predecessor')
if any(x in baseline for x in added):fail('new path already belonged to predecessor')
for rel,previous in baseline.items():
    path=root/rel
    if rel in removed:
        if path.exists():fail('removed predecessor file still exists: '+rel)
    elif not path.is_file():fail('protected predecessor file missing: '+rel)
    elif rel in generated:
        try:
            document=json.loads(path.read_text(encoding='utf-8'))
            if rel=='data/index.json':
                required={'schemaVersion':1,'databaseVersion':'4.0.5','normalizerVersion':16,'publishedVulkanSpec':'Vulkan 1.4.364 (2026-09-25)','producerQueryBaseline':'VulkanScope 3.0.12 · Vulkan 1.4.364'}
                if not all(document.get(k)==v for k,v in required.items()) or not isinstance(document.get('reports'),list) or not document.get('generatedAt'):fail('generated index metadata drift')
            else:fail('unregistered generated semantic validator: '+rel)
        except Exception as error:fail('generated index failed validation: '+str(error))
    elif digest(path)!=(hashes.get(rel) if rel in changed else previous['sha256']):fail('protected file hash mismatch: '+rel)
for rel in added:
    path=root/rel
    if not path.is_file():fail('successor source file missing: '+rel)
    elif rel not in self_excluded and digest(path)!=hashes.get(rel):fail('successor new file hash mismatch: '+rel)
if set(hashes)!=(changed|added)-self_excluded-generated:fail('successor hash map does not exactly cover pinned source modifications')
if a.strict_tree:
    allowed=(set(baseline)-removed)|added
    for f in root.rglob('*'):
        if f.is_file() and f.relative_to(root).as_posix() not in allowed:
            fail('unallowlisted file in release tree: '+f.relative_to(root).as_posix())
if errors:
    print('\n'.join('FAIL '+x for x in errors));raise SystemExit(1)
print(f'PASS regression contract 4.0.4 → 4.0.5 mode={"strict-tree" if a.strict_tree else "source-overlay"} baseline={len(baseline)} changed={len(changed)} removed={len(removed)} added={len(added)}')
