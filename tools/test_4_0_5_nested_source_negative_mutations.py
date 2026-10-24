from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_4_0_5_layout.py'
with tempfile.TemporaryDirectory(prefix='vsdb403-nested-test-') as td:
 t=Path(td)
 for rel in ['index.html','tools/repair_repository.py','tools/audit_database.py','rules/PROJECT_RULES.md','data/release.json','worker/package.json','.github/workflows/pages.yml']:
  dst=t/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/rel,dst)
 def test(expect):
  r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
  if (r.returncode==0)!=expect:raise SystemExit('nested layout guard incorrect: '+r.stdout+r.stderr)
 test(True)
 clone=t/'0cbbe'
 for rel in ['tools/repair_repository.py','tools/audit_database.py','rules/PROJECT_RULES.md','data/release.json']:
  dst=clone/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/rel,dst)
 (clone/'assets').mkdir(parents=True)
 test(False)
 shutil.rmtree(clone)
 test(True)
print('PASS 4.0.5 nested source detection: clean/rejected/recovered')
