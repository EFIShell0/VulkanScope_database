from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]; verifier=root/'tools/verify_1_0_1_full_audit.py'
mutations=[
 ('worker/src/index.js',"if(v.major===1&&v.minor===0)return p.application.versionCode===1000+v.patch","if(v.major===1&&v.minor===0)return true",'producer-identity'),
 ('worker/src/index.js',"if(a){surface.available=a[1].toLowerCase()==='true';surface.presentationSupported=a[2].toLowerCase()==='true';continue}","if(a){surface.available=a[1].toLowerCase()==='true';surface.presentationSupported=a[2].toLowerCase()==='true';push(out,'SURFACE','Available',a[1],surfaceAvailableState(surface));continue}",'line-order'),
 ('worker/src/index.js',"q==='available'?'unsupported'","q==='unavailable'?'unsupported'",'unsupported-evidence'),
 ('assets/app.v1006.js',"const av=surfaceAvailableState(s),pr=surfacePresentationState(s),diag=","const av=s.available?'available':'unavailable',pr=s.presentationSupported?'supported':'unsupported',diag=",'frontend-bool-state'),
]
def run(tree):
 return subprocess.run([sys.executable,str(verifier),'--root',str(tree),'--skip-version'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True).returncode
for rel,a,b,label in mutations:
 with tempfile.TemporaryDirectory(prefix='vsdb1001-neg-') as td:
  d=Path(td); shutil.copytree(root,d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.git','node_modules','.wrangler','__pycache__'))
  p=d/rel; s=p.read_text(encoding='utf-8')
  if a not in s: raise SystemExit(f'mutation anchor missing {label}')
  p.write_text(s.replace(a,b,1),encoding='utf-8')
  if run(d)==0: raise SystemExit(f'negative mutation accepted: {label}')
# false-positive wording only
with tempfile.TemporaryDirectory(prefix='vsdb1001-fp-') as td:
 d=Path(td); shutil.copytree(root,d,dirs_exist_ok=True,ignore=shutil.ignore_patterns('.git','node_modules','.wrangler','__pycache__'))
 p=d/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\nHarmless audit wording.\n',encoding='utf-8')
 if run(d)!=0: raise SystemExit('false-positive control rejected')
print('PASS Database 1.0.1 negative mutations and false-positive control')
