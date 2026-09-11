from __future__ import annotations
from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_0_13_reports_disclosure_spray_ui.py'

def run_fixture(name, rel, old, new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1013-{name}-') as td:
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

run_fixture('reserved-collapsed-width','assets/site.v0390.css','.submitted-reveal{width:0;max-width:0;max-height:0;','.submitted-reveal{width:232px;max-width:232px;max-height:100px;')
run_fixture('no-disclosure-animation','assets/site.v0390.css','visibility 0s linear .32s','visibility 0s')
run_fixture('squeezing-table','assets/site.v0390.css','.reports-table{width:max-content;min-width:100%;table-layout:auto}', '.reports-table{width:100%;min-width:100%;table-layout:fixed}')
run_fixture('lost-scroller-refresh','assets/app.v1013.js',"window.setTimeout(()=>{document.querySelectorAll('.table-scroll-shell').forEach(updateTableScroller)","window.setTimeout(()=>{document.querySelectorAll('.table-scroll-shell').forEach(()=>{})")
run_fixture('white-spray','assets/site.v0390.css','background:currentColor;color:var(--coverage-spray)','background:#fff;color:#fff')
run_fixture('missing-color-spray','assets/site.v0390.css','animation:coverageColorSpray 1.65s','animation:none')

with tempfile.TemporaryDirectory(prefix='vsdb-1013-false-positive-') as td:
    dst=Path(td)/'repo'
    shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
    p=dst/'changelog.md'
    p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless verifier control -->\n',encoding='utf-8',newline='\n')
    subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],check=True)
print('PASS Database 1.0.13 negative mutations + harmless false-positive control')
