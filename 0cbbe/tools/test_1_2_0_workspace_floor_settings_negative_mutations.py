from __future__ import annotations
from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_2_0_workspace_floor_settings.py'
required=['assets/app.v1200.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','worker/src/index.js','worker/tests/contract.mjs','data/release.json']
flag_files=list((root/'assets/country-flags').glob('*.png'))

def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-120-negative-') as td:
        d=Path(td)
        for r in required:
            dst=d/r; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/r,dst)
        fd=d/'assets/country-flags'; fd.mkdir(parents=True,exist_ok=True)
        for f in flag_files: shutil.copy2(f,fd/f.name)
        p=d/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'{name}: mutation token absent')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(d)],text=True,capture_output=True)
        if r.returncode==0: raise SystemExit(f'{name}: verifier accepted mutation')
        print('PASS negative',name)

fixture('producer-floor','worker/src/index.js','const supportedProducer=p=>producerAtLeast1205(p)','const supportedProducer=p=>producerAtLeast1019(p)')
fixture('silent-network-refresh','assets/app.v1200.js',"settingsNetworkBusy=true;if(!settingsNetworkData)renderNetworkInfo();try{","settingsNetworkBusy=true;renderNetworkInfo();try{")
fixture('country-language','assets/app.v1200.js',"new Intl.DisplayNames(['en'],{type:'region'})","new Intl.DisplayNames([browserLanguage()],{type:'region'})")
fixture('country-flags','assets/app.v1200.js',"sel?.id==='settingsRegionalCountry'","false")
fixture('compare-version-emphasis','assets/site.v0390.css','.compare-producer-version{font-weight:900!important;color:#fff!important','.compare-producer-version{font-weight:500!important;color:var(--muted)!important')
fixture('workspace-coverage','assets/app.v1200.js'," devices:{tone:'hardware'"," devicesMissing:{tone:'hardware'")
fixture('warning-style','assets/site.v0390.css','.settings-message-warning{color:#ffe3a0!important','.settings-message-warning{color:#cbd7ff!important')
with tempfile.TemporaryDirectory(prefix='vsdb-120-negative-flag-') as td:
    d=Path(td)
    for r in required:
        dst=d/r; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/r,dst)
    fd=d/'assets/country-flags'; fd.mkdir(parents=True,exist_ok=True)
    for f in flag_files: shutil.copy2(f,fd/f.name)
    (fd/'tr.png').unlink()
    r=subprocess.run([sys.executable,str(verifier),'--root',str(d)],text=True,capture_output=True)
    if r.returncode==0: raise SystemExit('missing-flag: verifier accepted mutation')
    print('PASS negative missing-flag')
print('PASS 1.2.0 negative mutation suite')
