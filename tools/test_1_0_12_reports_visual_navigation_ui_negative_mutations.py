from __future__ import annotations
from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_0_12_reports_visual_navigation_ui.py'

def run_fixture(name, rel, old, new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1012-{name}-') as td:
        dst=Path(td)/'repo'
        shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
        p=dst/rel
        s=p.read_text(encoding='utf-8')
        if old not in s:
            raise SystemExit(f'fixture token missing for {name}: {old!r}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],capture_output=True,text=True)
        if r.returncode==0:
            raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print(f'PASS negative mutation rejected: {name}')

run_fixture('white-hatch','assets/site.v0390.css','rgba(0,0,0,.9) 0 3px','rgba(255,255,255,.9) 0 3px')
run_fixture('missing-high-shine','assets/site.v0390.css','animation:coverageHighShine 2.6s','animation:none')
run_fixture('timestamps-expanded-by-default','assets/app.v1012.js','reportSubmittedExpanded:false','reportSubmittedExpanded:true')
run_fixture('lost-scroll-store','assets/app.v1012.js','const routeScrollPositions=new Map()','const routeScrollPositions=new Set()')
run_fixture('generic-android-filter','assets/app.v1012.js',"key==='android'?ANDROID_APP_FILTER_ICON:","key==='android'?`<svg class=\\\"filter-option-icon\\\"></svg>`:")

# Harmless documentation-only mutation must not trigger the UI verifier.
with tempfile.TemporaryDirectory(prefix='vsdb-1012-false-positive-') as td:
    dst=Path(td)/'repo'
    shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
    p=dst/'changelog.md'
    p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless verifier control -->\n',encoding='utf-8',newline='\n')
    subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],check=True)
print('PASS Database 1.0.12 negative mutations + harmless false-positive control')
