from __future__ import annotations
from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]; verifier=root/'tools/verify_1_0_20_release_state_handshake.py'
def mutate(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1020-{name}-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old!r}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative mutation rejected:',name)
mutate('legacy-worker-refresh-signal','worker/src/index.js',"status:'ok',databaseReleaseVersion:","status:'ok',databaseVersion:'1.0.20',databaseReleaseVersion:")
mutate('source-marker-premature-ready','data/release.json','"releaseReady":false','"releaseReady":true')
mutate('marker-cache-weakened','assets/app.v1020.js',"fetchJsonBounded(`./data/release.json?_=${Date.now()}`,{cache:'no-store'})","fetchJsonBounded(`./data/release.json?_=${Date.now()}`,{cache:'force-cache'})")
mutate('published-shell-probe-removed','assets/app.v1020.js','&&await publishedFrontendReady(marker)','')
mutate('retry-suppression-removed','assets/app.v1020.js','||suppressRepeatedUpdatePrompt(remote)','')
mutate('tag-trigger-restored','tools/pages.workflow.yml','branches: ["main"]','branches: ["main"]\n    tags: ["v*"]')
mutate('release-dependency-lost','tools/pages.workflow.yml','needs: [build, release]','needs: build')
mutate('marker-transition-lost','tools/pages.workflow.yml','python tools/mark_release_ready.py _site','python -c "print(\'skip ready transition\')"')
mutate('pages-deploy-v5-restored','tools/pages.workflow.yml','actions/deploy-pages@v4','actions/deploy-pages@v5')
mutate('ready-transition-not-fail-closed','tools/mark_release_ready.py',"'releaseReady':False","'releaseReady':True")
with tempfile.TemporaryDirectory(prefix='vsdb-1020-control-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless 1.0.20 verifier control -->\n',encoding='utf-8',newline='\n')
    subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],check=True)
print('PASS Database 1.0.20 negative mutations + harmless false-positive control')
