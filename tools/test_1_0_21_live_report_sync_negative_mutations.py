from __future__ import annotations
from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]; verifier=root/'tools/verify_1_0_21_live_report_sync.py'
def mutate(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1021-{name}-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old!r}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative mutation rejected:',name)
mutate('slow-poll-regression','assets/app.v1021.js','LIVE_SYNC_INTERVAL_MS=3000','LIVE_SYNC_INTERVAL_MS=10000')
mutate('sync-head-cache-regression','assets/app.v1021.js',"const head=await fetchJsonBounded(u,{cache:'no-store'})","const head=await fetchJsonBounded(u,{cache:'force-cache'})")
mutate('sync-head-shortcut-broken','assets/app.v1021.js','if(!force&&head.syncToken===liveSyncToken)','if(!force&&false)')
mutate('visibility-force-lost','assets/app.v1021.js',"visibilitychange',()=>{if(!document.hidden){void runLiveSync(true)","visibilitychange',()=>{if(!document.hidden){void runLiveSync(false)")
mutate('payload-cache-bust-lost','assets/app.v1021.js','?compact=1&_live=${Date.now()}','?compact=1')
mutate('atomic-size-gate-lost','assets/app.v1021.js',"if(nextReports.size!==liveIds.size)throw new Error('Live report set could not be completed atomically');",'')
mutate('sync-endpoint-lost','worker/src/index.js',"url.pathname==='/v1/sync'&&request.method==='GET'","url.pathname==='/v1/sync-disabled'&&request.method==='GET'")
mutate('sync-query-count-lost','worker/src/index.js','COUNT(*) OVER() AS report_count','1 AS report_count')
with tempfile.TemporaryDirectory(prefix='vsdb-1021-control-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless 1.0.21 verifier control -->\n',encoding='utf-8',newline='\n')
    subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],check=True)
print('PASS Database 1.0.21 live-sync negative mutations + harmless false-positive control')
