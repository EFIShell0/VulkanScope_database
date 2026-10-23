from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]; verifier=root/'tools/verify_1_0_2_producer_baseline.py'
mutations=[
 ('worker/src/index.js',"if(v.major===1&&v.minor===0)return p.application.versionCode===1000+v.patch","if(v.major===1&&v.minor===0)return true",'producer-identity'),
 ('data/index.json','"normalizerVersion": 16','"normalizerVersion": 17','normalizer-drift'),
 ('worker/tests/contract.mjs','bad1002Identity.application.versionCode=1001','bad1002Identity.application.versionCode=1002','identity-negative-fixture'),
]
def run(tree):
 return subprocess.run([sys.executable,str(verifier),'--root',str(tree),'--skip-version'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True).returncode
for rel,a,b,label in mutations:
 with tempfile.TemporaryDirectory(prefix='vsdb1002-neg-') as td:
  d=Path(td); shutil.copytree(root,d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.git','node_modules','.wrangler','__pycache__'))
  p=d/rel; s=p.read_text(encoding='utf-8')
  if a not in s: raise SystemExit(f'mutation anchor missing {label}')
  p.write_text(s.replace(a,b,1),encoding='utf-8')
  if run(d)==0: raise SystemExit(f'negative mutation accepted: {label}')
with tempfile.TemporaryDirectory(prefix='vsdb1002-fp-') as td:
 d=Path(td); shutil.copytree(root,d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.git','node_modules','.wrangler','__pycache__'))
 p=d/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\nHarmless producer-audit wording.\n',encoding='utf-8')
 if run(d)!=0: raise SystemExit('false-positive control rejected')
print('PASS Database 1.0.2 negative mutations and false-positive control')
