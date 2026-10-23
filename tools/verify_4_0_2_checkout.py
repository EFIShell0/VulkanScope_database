from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, sys
parser=argparse.ArgumentParser(description='Fail-closed pre-repair Git checkout 4.0.2 coherency check')
parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
args=parser.parse_args();root=args.root.resolve()
contract=root/'regression/4.0.1_to_4.0.2_contract.json'
errors=[]
def fail(x):errors.append(x)
try:
 c=json.loads(contract.read_text(encoding='utf-8'))
except (OSError,ValueError) as e:
 raise SystemExit('FAIL missing/invalid 4.0.2 source contract: '+str(e))
if c.get('successor')!='4.0.2' or c.get('baseline')!='4.0.1':fail('contract identity mismatch')
sha=c.get('successorSha256',{})
critical=['tools/repair_repository.py','tools/quality_gate.py','tools/build_pages_artifact.py','tools/pages.workflow.yml','.github/workflows/pages.yml','tools/package_release.py','tools/verify_4_0_2_regression_contract.py','assets/app.v4002.js','assets/browser-compat.v4002.js','assets/release-bootstrap.v4002.js','assets/encyclopedia.v4002.js','assets/site.v4002.css','index.html','data/release.json']
for rel in critical:
 p=root/rel
 if not p.is_file():fail('required current release file missing: '+rel);continue
 if rel not in sha or hashlib.sha256(p.read_bytes()).hexdigest()!=sha[rel]:fail('wrong version / bad hash: '+rel)
for rel in ['assets/app.v4001.js','assets/browser-compat.v4001.js','assets/release-bootstrap.v4001.js']:
 p=root/rel
 if not p.is_file():fail('missing immediate predecessor bridge: '+rel)
try:
 s=(root/'tools/repair_repository.py').read_text(encoding='utf-8')
 if "CURRENT_APP = 'app.v4002.js'" not in s or "PREDECESSOR_BRIDGE = {'app.v4001.js','browser-compat.v4001.js','release-bootstrap.v4001.js'}" not in s:fail('repair script bridge/current mismatch')
except OSError:pass
for rel in ['assets/app.v4000.js','assets/browser-compat.v4000.js','assets/release-bootstrap.v4000.js']:
 if (root/rel).exists():fail('stale two-generation-old bridge in checkout: '+rel)
if errors:
 print('\n'.join('FAIL '+e for e in errors));raise SystemExit(1)
print('PASS 4.0.2 checkout preflight: tool hashes, predecessor bridge, current JS and release identity agree')
