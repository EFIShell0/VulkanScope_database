from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_0_5_optional_lock_overlay.py'

mutations=[
 ('repair-unlink','tools/repair_repository.py','optional_lock.unlink()','pass  # cleanup removed'),
 ('overlay-fixture','tools/test_existing_repo_overlay.py','real 1.0.4 failure','stale lock fixture removed'),
 ('workflow-order','tools/pages.workflow.yml','python tools/verify_optional_npm_lock.py','python tools/verify_optional_npm_lock_REMOVED.py'),
 ('lock-pin','tools/verify_optional_npm_lock.py',"want = '4.130.0'","want = '4.125.0'"),
]
for name,rel,a,b in mutations:
    with tempfile.TemporaryDirectory(prefix='vsdb105-neg-') as td:
        d=Path(td)/'tree'
        shutil.copytree(root,d,ignore=shutil.ignore_patterns('.git','node_modules','.wrangler','_site','__pycache__'))
        p=d/rel; s=p.read_text(encoding='utf-8')
        if a not in s: raise SystemExit(f'{name}: mutation source missing')
        p.write_text(s.replace(a,b,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(d/'tools/verify_1_0_5_optional_lock_overlay.py'),'--root',str(d)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode==0:
            print(r.stdout)
            raise SystemExit(f'{name}: negative mutation was accepted')
print('PASS VulkanScope Database 1.0.8 optional-lock overlay negative mutations')
