from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]; verifier=root/'tools/verify_1_0_23_connectivity_settings_motion.py'
def mutate(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1023-{name}-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'control token missing for {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation was not rejected: {name}')
mutate('offline-monitor-lost','assets/app.v1023.js',"window.addEventListener('offline'","window.addEventListener('disconnected'")
mutate('restore-delay-lost','assets/app.v1023.js','},3000);renderNetworkInfo()','},30);renderNetworkInfo()')
mutate('local-persistence-optin-lost','assets/app.v1023.js','const saveFavorites=()=>!rememberLocalState||writeJsonStorage','const saveFavorites=()=>writeJsonStorage')
mutate('clear-data-lost','assets/app.v1023.js','const clearSavedLocalState=()=>','const clearLocalStateBroken=()=>')
mutate('ipv6-color-lost','assets/site.v0390.css','.network-ipv6{color:var(--green)!important}','.network-ipv6{color:#fff!important}')
mutate('settings-category-lost','index.html','data-settings-category="favorites"','data-settings-category="favoritez"')
mutate('detail-action-group-lost','assets/app.v1023.js','class="detail-actions" role="group" aria-label="Report actions"','class="report-toolbar"')
mutate('row-motion-lost','assets/site.v0390.css','.click-row td{transition:background-color .22s','.click-row td{transition:none')
mutate('network-d1-leak','worker/src/index.js','const currentNetworkInfo=request=>{','const currentNetworkInfo=(request,env)=>{const leaked=env.DB;')
with tempfile.TemporaryDirectory(prefix='vsdb-1023-control-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst)
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless 1.0.23 verifier control -->\n',encoding='utf-8',newline='\n')
    r=subprocess.run([sys.executable,str(verifier),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if r.returncode!=0: raise SystemExit('harmless mutation false-positive:\n'+r.stdout)
print('PASS Database 1.0.23 negative mutations + harmless false-positive control')
