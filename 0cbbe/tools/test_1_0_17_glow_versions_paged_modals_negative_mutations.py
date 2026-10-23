from __future__ import annotations
from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_0_17_glow_versions_paged_modals.py'
def run_fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1017-{name}-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing for {name}: {old!r}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print(f'PASS negative mutation rejected: {name}')
run_fixture('coverage-position-unit-loss','assets/app.v1017.js','--coverage-position:${ratio*100}%','--coverage-position:${ratio*100}')
run_fixture('coverage-anchor-loss','assets/site.v0390.css','.coverage.high .coverage-bar{position:relative!important;overflow:visible!important','.coverage.high .coverage-bar{position:static!important;overflow:visible!important')
run_fixture('coverage-valid-endpoint-loss','assets/site.v0390.css','left:clamp(4px,var(--coverage-position),calc(100% - 4px))!important','left:clamp(4px,calc(var(--coverage-pct)*1%),calc(100% - 4px))!important')
run_fixture('versions-logo-loss','assets/app.v1017.js','gpuNameCell(x.r,x.gpu)}${gpuLogoCell(x.r)','gpuNameCell(x.r,x.gpu)}${`<td>no logo</td>`')
run_fixture('versions-vendor-loss','assets/app.v1017.js','identity=`${gpuNameCell(x.r,x.gpu)}${gpuLogoCell(x.r)}<td>${esc(vendorDisplay(x.r))}</td>`','identity=`${gpuNameCell(x.r,x.gpu)}${gpuLogoCell(x.r)}<td>${esc(x.gpu)}</td>`')
run_fixture('modal-50-cap-loss','assets/app.v1017.js','<select class="modal-page-size">${[10,25,50].map','<select class="modal-page-size">${[10,25,100].map')
run_fixture('reports-paged-loss','assets/app.v1017.js','coverage-report-list modal-paged-list','coverage-report-list')
run_fixture('distinct-paged-loss','assets/app.v1017.js','modal-value-list modal-paged-list','modal-value-list')
run_fixture('modal-scrollbar-loss','assets/site.v0390.css','overflow-y:auto','overflow-y:visible')
run_fixture('live-sync-loss','assets/app.v1017.js','window.setInterval(runLiveSync,LIVE_SYNC_INTERVAL_MS)','window.setTimeout(runLiveSync,LIVE_SYNC_INTERVAL_MS)')
with tempfile.TemporaryDirectory(prefix='vsdb-1017-false-positive-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless 1.0.17 verifier control -->\n',encoding='utf-8',newline='\n')
    subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],check=True)
print('PASS Database 1.0.17 negative mutations + harmless false-positive control')
