from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parents[1]
for target in [R/'dist',R/'_site'/'unsafe-output']:
    if target.exists(): raise SystemExit('FAIL test would modify existing build output: '+str(target))
    p=subprocess.run([sys.executable,'-B','tools/package_release.py',str(target)],cwd=R,capture_output=True,text=True)
    if p.returncode==0 or target.exists():raise SystemExit('FAIL in-checkout package output was not rejected safely')
print('PASS 4.0.10 package build safety: in-checkout output rejected before creation')
