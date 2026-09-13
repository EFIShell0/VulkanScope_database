from __future__ import annotations
from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_0_25_connectivity_surface_encyclopedia.py'
required=['assets/app.v1025.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md']
flag_files=list((root/'assets/country-flags').glob('*.png'))

def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-1025-negative-') as td:
        d=Path(td)
        for r in required:
            dst=d/r; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/r,dst)
        fd=d/'assets/country-flags'; fd.mkdir(parents=True,exist_ok=True)
        for f in flag_files: shutil.copy2(f,fd/f.name)
        p=d/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'{name}: mutation token absent')
        p.write_text(s.replace(old,new),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(d)],text=True,capture_output=True)
        if r.returncode==0: raise SystemExit(f'{name}: verifier accepted mutation')
        print('PASS negative',name)

fixture('restored-duration','assets/app.v1025.js','},5000);renderNetworkInfo()','},3000);renderNetworkInfo()')
fixture('failure-debounce','assets/app.v1025.js','liveSyncFailures++;markNetworkFailure(true)','liveSyncFailures++;markNetworkFailure(liveSyncFailures>=2)')
fixture('manual-refresh','index.html','<div id="networkInfo"></div>','<button id="networkInfoRefresh">Refresh</button><div id="networkInfo"></div>')
fixture('scrollbar-design','assets/site.v0390.css','scrollbar-color:#684047 #100c0d','scrollbar-color:auto')
fixture('encyclopedia-workspace','assets/app.v1025.js','encyclopedia-workspace','encyclopedia-panel')
fixture('surface-semantics','assets/app.v1025.js','Unavailable, unsupported, not applicable and unknown are not interchangeable.','All states are equivalent.')
# Missing local flag asset must fail.
with tempfile.TemporaryDirectory(prefix='vsdb-1025-negative-flag-') as td:
    d=Path(td)
    for r in required:
        dst=d/r; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/r,dst)
    fd=d/'assets/country-flags'; fd.mkdir(parents=True,exist_ok=True)
    for f in flag_files: shutil.copy2(f,fd/f.name)
    (fd/'tr.png').unlink()
    r=subprocess.run([sys.executable,str(verifier),'--root',str(d)],text=True,capture_output=True)
    if r.returncode==0: raise SystemExit('missing-flag: verifier accepted mutation')
    print('PASS negative missing-flag')
print('PASS 1.0.25 negative mutation suite')
