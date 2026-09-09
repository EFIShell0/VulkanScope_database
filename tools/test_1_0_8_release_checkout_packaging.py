#!/usr/bin/env python3
from pathlib import Path
import shutil, subprocess, sys, tempfile, zipfile

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='vsdb108-overlay-') as td:
    td=Path(td)
    src=td/'repo'
    shutil.copytree(root,src,ignore=shutil.ignore_patterns('.git','node_modules','.wrangler','_site','dist','__pycache__'))
    # Reproduce the real long-lived tagged-checkout failure class: historical tracked
    # frontend assets are source-history extras, not release-package members.
    extras={
        'assets/site.v0380.css':'/* historical css */\n',
        'assets/site.v0357.css':'/* historical css */\n',
        'assets/app.js':'// historical unversioned frontend\n',
    }
    for rel,data in extras.items():
        p=src/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(data,encoding='utf-8',newline='\n')

    r=subprocess.run([sys.executable,str(src/'tools/verify_regression_contract.py')],cwd=src,capture_output=True,text=True)
    if r.returncode!=0:
        raise SystemExit('FAIL source-overlay rejected legitimate tagged-checkout history extras\n'+r.stdout+r.stderr)

    dist=td/'dist'
    r=subprocess.run([sys.executable,str(src/'tools/package_release.py'),str(dist),'--root',str(src)],cwd=src,capture_output=True,text=True)
    if r.returncode!=0:
        raise SystemExit('FAIL package_release rejected history-bearing tagged checkout\n'+r.stdout+r.stderr)

    zp=dist/'VulkanScope-Database-1.0.8.zip'
    if not zp.is_file(): raise SystemExit('FAIL deterministic release ZIP missing')
    with zipfile.ZipFile(zp) as zf:
        names=set(zf.namelist())
        leaked=sorted(set(extras) & names)
        if leaked: raise SystemExit('FAIL historical checkout extras leaked into release ZIP: '+', '.join(leaked))
        extract=td/'extract'; zf.extractall(extract)

    r=subprocess.run([sys.executable,str(extract/'tools/verify_regression_contract.py'),'--strict-tree'],
                     cwd=extract,capture_output=True,text=True)
    if r.returncode!=0:
        raise SystemExit('FAIL clean release extract did not pass strict-tree\n'+r.stdout+r.stderr)

    rogue=extract/'assets/site.v0999.css'
    rogue.write_text('/* injected */\n',encoding='utf-8',newline='\n')
    r=subprocess.run([sys.executable,str(extract/'tools/verify_regression_contract.py'),'--strict-tree'],
                     cwd=extract,capture_output=True,text=True)
    if r.returncode==0:
        raise SystemExit('FAIL strict-tree accepted an injected unallowlisted release-package file')

print('PASS Database 1.0.8 tagged-checkout source-overlay -> deterministic strict-package state machine')
