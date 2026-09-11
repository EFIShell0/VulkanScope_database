from __future__ import annotations
from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_0_18_full_audit.py'
def run_fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1018-{name}-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing for {name}: {old!r}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print(f'PASS negative mutation rejected: {name}')
run_fixture('modal-selector-anchor-loss','assets/app.v1018.js',"classList.add('modal-page-size-select','drop-up')","classList.add('modal-page-size-select')")
run_fixture('modal-selector-css-loss','assets/site.v0390.css','bottom:calc(100% + 7px)!important','bottom:auto!important')
run_fixture('android-brand-color-loss','assets/app.v1018.js','fill="#3DDC84"','fill="#E2676A"')
run_fixture('devices-chart-loss','assets/app.v1018.js',"donutChart('GPU / reports',chartItems,rs.length,'',state.deviceSliceLimit)","'<div>No chart</div>'")
run_fixture('devices-logo-loss','assets/app.v1018.js','gpuNameCell(x.r)}${gpuLogoCell(x.r)','gpuNameCell(x.r)}${`<td>no logo</td>`')
run_fixture('source-audit-current-app-loss','tools/audit_database.py',"APP_ASSET='app.v1018.js'","APP_ASSET='app.v1017.js'")
run_fixture('quality-source-audit-loss','tools/quality_gate.py',"run(sys.executable,'tools/audit_database.py','--source-tree','.')","# source audit removed")
run_fixture('csp-object-hardening-loss','index.html',"object-src 'none'","object-src *")
run_fixture('body-bound-loss','worker/src/index.js','2*1024*1024','20*1024*1024')
with tempfile.TemporaryDirectory(prefix='vsdb-1018-false-positive-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless 1.0.18 verifier control -->\n',encoding='utf-8',newline='\n')
    subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],check=True)
print('PASS Database 1.0.18 negative mutations + harmless false-positive control')
