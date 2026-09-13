from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]; verifier=root/'tools/verify_1_0_22_live_report_sync.py'
def mutate(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1022-{name}-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'control token missing for {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation was not rejected: {name}')
mutate('preload-visible-state-regression','assets/app.v1022.js','snapshotReports.set(id,hydrateReport(v0,byId.get(id)))','state.reports.set(id,hydrateReport(v0,byId.get(id)))')
mutate('atomic-commit-lost','assets/app.v1022.js','state.reports=nextReports;state.index=indexState(live.meta,validIndex)','state.reports=nextReports')
mutate('favorites-persistence-lost','assets/app.v1022.js',"FAVORITES_STORAGE_KEY='vulkanscopeDatabaseFavorites.v1'","FAVORITES_STORAGE_KEY='broken'")
mutate('network-dns-invented','worker/src/index.js',"dns:{resolver:null,status:'not_observable'","dns:{resolver:'1.1.1.1',status:'observed'")
mutate('network-d1-leak','worker/src/index.js','const currentNetworkInfo=request=>{','const currentNetworkInfo=(request,env)=>{const leaked=env.DB;')
mutate('selection-guard-lost','assets/app.v1022.js','suppressReportNavigationUntil=performance.now()+400','suppressReportNavigationUntil=0')
with tempfile.TemporaryDirectory(prefix='vsdb-1022-control-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst)
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless 1.0.22 verifier control -->\n',encoding='utf-8',newline='\n')
    r=subprocess.run([sys.executable,str(verifier),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if r.returncode!=0: raise SystemExit('harmless mutation false-positive:\n'+r.stdout)
print('PASS Database 1.0.22 negative mutations + harmless false-positive control')
