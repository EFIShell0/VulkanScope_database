from __future__ import annotations
from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_0_15_database_ui_integrity.py'
def run_fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1015-{name}-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing for {name}: {old!r}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print(f'PASS negative mutation rejected: {name}')
run_fixture('vendor-toggle-loss','assets/app.v1015.js',"bindReportColumnDisclosure(7,'vendorToggle','Vendor','reportVendorExpanded'","bindReportColumnDisclosure(7,'vendorToggleMissing','Vendor','reportVendorExpanded'")
run_fixture('type-toggle-loss','assets/app.v1015.js',"bindReportColumnDisclosure(8,'typeToggle','Type','reportTypeExpanded'","bindReportColumnDisclosure(8,'typeToggleMissing','Type','reportTypeExpanded'")
run_fixture('search-clear-no-fade','assets/site.v0390.css','.search-clear-button.is-hidden{opacity:0;visibility:hidden;pointer-events:none;transform:scale(.72)}','.search-clear-button.is-hidden{display:none}')
run_fixture('versions-bar-regression','assets/app.v1015.js','const reportTable=`<section class="version-report-counts">','const forbidden=coverage(1,2);const reportTable=`<section class="version-report-counts">')
run_fixture('versions-ring-loss','assets/app.v1015.js','class="version-ring" role="img"','class="version-square" role="img"')
run_fixture('global-clear-loss','index.html','id="globalSearchClear"','id="globalSearchClearMissing"')
run_fixture('native-search-x-return','assets/site.v0390.css','-webkit-appearance:none','-webkit-appearance:auto')
run_fixture('loading-pulse-loss','assets/app.v1015.js','function render(){pulseUiLoading();','function render(){')
run_fixture('stale-overlay-repair-loss','tools/pages.workflow.yml','python tools/repair_repository.py --apply','python tools/repair_repository.py --check',)
run_fixture('press-motion-loss','assets/site.v0390.css','button:not(:disabled):active,.repo-link:active,.card:active','button.not-active,.repo-link.not-active,.card.not-active')
with tempfile.TemporaryDirectory(prefix='vsdb-1015-false-positive-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless 1.0.15 verifier control -->\n',encoding='utf-8',newline='\n')
    subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],check=True)
print('PASS Database 1.0.15 negative mutations + harmless false-positive control')
