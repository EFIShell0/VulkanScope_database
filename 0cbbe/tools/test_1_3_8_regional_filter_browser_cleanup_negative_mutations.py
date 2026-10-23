from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_3_8_regional_filter_browser_cleanup.py'
fixtures=[
 ('browser-logo-return','assets/app.v1308.js','settings-browser-summary settings-browser-summary-text','settings-browser-summary settings-browser-icon'),
 ('filter-nowrap','assets/site.v1308.css','white-space:normal!important','white-space:nowrap!important'),
 ('disabled-open','assets/app.v1308.js','const open=()=>{if(sel.disabled)return;','const open=()=>{'),
 ('page-input','assets/app.v1308.js','input.disabled=single','input.disabled=false'),
 ('regional-modes','assets/app.v1308.js',"REGIONAL_MODES=new Set(['auto','country','manual'])","REGIONAL_MODES=new Set(['auto','manual'])"),
 ('country-zone','assets/app.v1308.js',"if(mode==='country')return countryPrimaryTimeZone(effectiveCountryCode())","if(mode==='country')return browserTimeZone()"),
 ('country-control-matrix','assets/app.v1308.js',"const enabled=mode==='manual'||(mode==='country'&&id==='settingsRegionalCountry')","const enabled=true"),
 ('manual-date-guard','assets/app.v1308.js',"const effectiveRegionalDateFormat=()=>effectiveRegionalMode()==='manual'?state.regionalDateFormat:'auto'","const effectiveRegionalDateFormat=()=>state.regionalDateFormat"),
 ('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_3_8_regional_filter_browser_cleanup.py','python tools/verify_1_3_7_browser_brand_marks.py'),
]
for name,rel,a,b in fixtures:
    with tempfile.TemporaryDirectory(prefix='vsdb138-mut-') as td:
        dst=Path(td)/'tree'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__'))
        p=dst/rel; t=p.read_text(encoding='utf-8')
        if a not in t: raise SystemExit(f'fixture token missing {name}: {a!r}')
        p.write_text(t.replace(a,b,1),encoding='utf-8')
        if rel=='tools/pages.workflow.yml':
            (dst/'.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if r.returncode==0: raise SystemExit(f'negative mutation escaped verifier: {name}')
print('PASS 1.3.8 negative mutation suite')
