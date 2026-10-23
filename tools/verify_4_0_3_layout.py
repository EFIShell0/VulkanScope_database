from __future__ import annotations
from pathlib import Path
import argparse, re, sys
parser=argparse.ArgumentParser(description='Prevent committed or local nested source-root clones')
parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
a=parser.parse_args()
def find_nested(root:Path):
    result=[]
    for p in sorted(root.iterdir()):
        if not p.is_dir() or p.name in {'.git','assets','tools','worker','rules','licenses','data','compat','regression','registry','.github'}:
            continue
        # Root copies from buggy ZIP installations have a complete set of markers.
        markers=['tools/repair_repository.py','tools/audit_database.py','assets','data/release.json','rules/PROJECT_RULES.md']
        if all((p / rel).exists() for rel in markers):
            result.append(p.name)
    return result
root=a.root.resolve()
errors=[]
required=['index.html','tools/repair_repository.py','tools/audit_database.py','rules/PROJECT_RULES.md','data/release.json','worker/package.json','.github/workflows/pages.yml']
for rel in required:
    if not (root/rel).is_file():errors.append('source root missing '+rel)
for rel in find_nested(root):errors.append('nested full source tree forbidden: '+rel)
if errors:
    print('\n'.join('FAIL '+x for x in errors));sys.exit(1)
print('PASS VulkanScope Database 4.0.3 canonical root, no nested source clone')
