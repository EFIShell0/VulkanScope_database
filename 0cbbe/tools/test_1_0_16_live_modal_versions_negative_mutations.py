from __future__ import annotations
from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_0_16_live_modal_versions.py'
def run_fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1016-{name}-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing for {name}: {old!r}')
        p.write_text(s.replace(old,new),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print(f'PASS negative mutation rejected: {name}')
run_fixture('submitted-width-regression','assets/site.v0390.css','.reports-table.submitted-expanded .submitted-head{width:320px!important}', '.reports-table.submitted-expanded .submitted-head{width:250px!important}')
run_fixture('vendor-width-regression','assets/site.v0390.css','.reports-table.vendor-expanded th:nth-child(7),.reports-table.vendor-expanded td:nth-child(7){width:286px!important', '.reports-table.vendor-expanded th:nth-child(7),.reports-table.vendor-expanded td:nth-child(7){width:190px!important')
run_fixture('distinct-accordion-regression','assets/app.v1016.js','const dist=distinctDetails(values);','const dist=accordionMarkup(`${values.length} distinct`,`x`);')
run_fixture('distinct-arrow-regression','assets/app.v1016.js','M9 6l6 6-6 6','M6 9l6 6 6-6')
run_fixture('versions-donut-loss','assets/app.v1016.js',"donutChart('GPU / Vulkan version / reports',chartItems,rs.length,'',state.versionSliceLimit)","'<div>no chart</div>'")
run_fixture('versions-gpu-table-loss','assets/app.v1016.js',"table(['GPU','Device API','Loader / instance API','Reports','Share'],rows)","table(['Device API','Loader / instance API','Reports','Share'],rows)")
run_fixture('live-poll-loss','assets/app.v1016.js','window.setInterval(runLiveSync,LIVE_SYNC_INTERVAL_MS)','window.setTimeout(runLiveSync,LIVE_SYNC_INTERVAL_MS)')
run_fixture('live-atomic-loss','assets/app.v1016.js','state.reports=nextReports','for(const x of nextReports)state.reports.set(x[0],x[1])')
run_fixture('api-version-loss','worker/src/index.js',"databaseVersion:'1.0.16'","databaseVersion:'1.0.15'")
run_fixture('update-refresh-loss','assets/app.v1016.js',"modal.querySelector('#databaseUpdateRefresh').onclick=()=>location.reload()","modal.querySelector('#databaseUpdateRefresh').onclick=()=>{}")
run_fixture('vendor-toggle-loss','assets/app.v1016.js',"bindReportColumnDisclosure(7,'vendorToggle','Vendor','reportVendorExpanded'","bindReportColumnDisclosure(7,'vendorToggleMissing','Vendor','reportVendorExpanded'")
run_fixture('zero-hatch-loss','assets/site.v0390.css','.coverage.zero .coverage-bar{','.coverage.zero-missing .coverage-bar{')
with tempfile.TemporaryDirectory(prefix='vsdb-1016-false-positive-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless 1.0.16 verifier control -->\n',encoding='utf-8',newline='\n')
    subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],check=True)
print('PASS Database 1.0.16 negative mutations + harmless false-positive control')
