from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]; verifier=root/'tools/verify_1_0_24_regional_compare_country.py'
def mutate(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1024-{name}-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'control token missing for {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation was not rejected: {name}')
mutate('unavailable-chip-returned','assets/app.v1024.js',"badge:''","badge:'Unavailable'")
mutate('restore-clobber-returned','assets/app.v1024.js',"if(networkUiState==='restored')return","if(networkUiState==='restored')setNetworkBannerState('online')")
mutate('restore-delay-shortened','assets/app.v1024.js','},3000);renderNetworkInfo()','},30);renderNetworkInfo()')
mutate('regional-storage-bypass','assets/app.v1024.js','const saveUiPrefs=()=>!rememberLocalState||writeJsonStorage','const saveUiPrefs=()=>writeJsonStorage')
mutate('country-name-lost','assets/app.v1024.js',"new Intl.DisplayNames([regionalLocale()],{type:'region'})","null")
mutate('country-flag-lost','assets/app.v1024.js','String.fromCodePoint(...[...cc].map(c=>127397+c.charCodeAt(0)))',"''")
mutate('compare-swap-lost','assets/app.v1024.js','id="swapCompare"','id="swapCompareBroken"')
mutate('compare-b-lane-lost','assets/site.v0390.css','.compare-report-b:before','.compare-report-b-broken:before')
with tempfile.TemporaryDirectory(prefix='vsdb-1024-control-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst)
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless 1.0.24 verifier control -->\n',encoding='utf-8',newline='\n')
    r=subprocess.run([sys.executable,str(verifier),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if r.returncode!=0: raise SystemExit('harmless mutation false-positive:\n'+r.stdout)
print('PASS Database 1.0.24 negative mutations + harmless false-positive control')
