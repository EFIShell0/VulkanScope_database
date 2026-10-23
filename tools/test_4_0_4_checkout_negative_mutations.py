from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
verify=root/'tools/verify_4_0_4_checkout.py'
needed=['tools/verify_4_0_4_layout.py','tools/audit_database.py','rules/PROJECT_RULES.md','worker/package.json','regression/4.0.3_to_4.0.4_contract.json','tools/repair_repository.py','tools/quality_gate.py','tools/build_pages_artifact.py','tools/pages.workflow.yml','.github/workflows/pages.yml','tools/package_release.py','tools/verify_4_0_4_regression_contract.py','assets/app.v4004.js','assets/browser-compat.v4004.js','assets/release-bootstrap.v4004.js','assets/encyclopedia.v4004.js','assets/site.v4004.css','assets/app.v4003.js','assets/browser-compat.v4003.js','assets/release-bootstrap.v4003.js','index.html','data/release.json']
with tempfile.TemporaryDirectory(prefix='vsdb402-checkout-negative-') as t:
 dest=Path(t)
 for rel in needed:
  x=dest/rel;x.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/rel,x)
 def check(expect=True):
  p=subprocess.run([sys.executable,str(verify),'--root',str(dest)],capture_output=True,text=True)
  if (p.returncode==0)!=expect:raise SystemExit(f'Unexpected checkout verification expect={expect}: '+p.stdout+p.stderr)
 check()
 for rel in ['tools/repair_repository.py','tools/pages.workflow.yml','tools/quality_gate.py','assets/app.v4004.js']:
  p=dest/rel;old=p.read_bytes();p.write_bytes(old+b'\n# stale version\n');check(False);p.write_bytes(old)
 for rel in ['assets/app.v4003.js','assets/browser-compat.v4003.js','assets/release-bootstrap.v4003.js']:
  p=dest/rel;old=p.read_bytes();p.unlink();check(False);p.write_bytes(old)
 p=dest/'assets/app.v4002.js';p.write_text('obsolete',encoding='utf-8');check(False);p.unlink();check()
print('PASS 4.0.4 checkout preflight: 8 corruption/missing/obsolete negatives rejected')
