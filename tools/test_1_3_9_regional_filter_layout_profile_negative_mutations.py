from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_3_9_regional_filter_layout_profile.py'
# The verifier reads only this small source slice. Build lightweight fixtures and execute
# the independent mutations in parallel so release gates do not repeatedly copy media/flags.
fixture_files=(
    'assets/app.v1309.js','assets/browser-compat.v1309.js','assets/release-bootstrap.v1309.js','assets/site.v1309.css',
    'index.html','rules/PROJECT_RULES.md','worker/src/index.js','tools/build_pages_artifact.py','tools/repair_repository.py',
    '.github/workflows/pages.yml','tools/pages.workflow.yml','data/release.json',
)
fixtures=[
 ('manual-country-enabled','assets/app.v1309.js',"mode==='manual'?id!=='settingsRegionalCountry':false","mode==='manual'?true:false"),
 ('manual-country-retained','assets/app.v1309.js',"else if(state.regionalMode==='manual')state.regionalCountry='auto'","else if(state.regionalMode==='manual')state.regionalCountry=state.regionalCountry"),
 ('manual-country-locale','assets/app.v1309.js',"if(mode==='auto'||mode==='manual')return browserLanguage()","if(mode==='auto')return browserLanguage()"),
 ('profile-date-row','assets/app.v1309.js',"regionalProfileRow('Date format'","regionalProfileRow('Date sample'"),
 ('profile-dst-row','assets/app.v1309.js',"regionalProfileRow('Daylight / summer offset'","regionalProfileRow('Season offset'"),
 ('permanent-gutter','assets/site.v1309.css','.custom-select-scroll{padding-right:0!important}', '.custom-select-scroll{padding-right:23px!important}'),
 ('overflow-class','assets/app.v1309.js',"host.classList.toggle('has-surface-scrollbar',scrollable)","host.classList.toggle('has-surface-scrollbar',true)"),
 ('regional-narrow-grid','assets/site.v1309.css','.settings-regional-group .settings-select-row{grid-template-columns:minmax(0,1fr)!important','.settings-regional-group .settings-select-row{grid-template-columns:1fr 90px!important'),
 ('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_3_9_regional_filter_layout_profile.py','python tools/verify_1_3_8_regional_filter_browser_cleanup.py'),
]

def make_fixture(dst:Path):
    for rel in fixture_files:
        src=root/rel; out=dst/rel
        out.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,out)

with tempfile.TemporaryDirectory(prefix='vsdb139-mut-suite-') as td:
    base=Path(td)
    jobs=[]
    for i,(name,rel,a,b) in enumerate(fixtures):
        dst=base/f'{i:02d}-{name}'; dst.mkdir(); make_fixture(dst)
        p=dst/rel; t=p.read_text(encoding='utf-8')
        if a not in t: raise SystemExit(f'fixture token missing {name}: {a!r}')
        p.write_text(t.replace(a,b,1),encoding='utf-8')
        if rel=='tools/pages.workflow.yml':
            (dst/'.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
        proc=subprocess.Popen([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        jobs.append((name,proc))
    escaped=[]
    for name,proc in jobs:
        if proc.wait()==0: escaped.append(name)
    if escaped: raise SystemExit('negative mutation escaped verifier: '+', '.join(escaped))
print('PASS 1.3.9 negative mutation suite')
