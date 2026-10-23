from __future__ import annotations
from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_0_19_dominant_glow_release_ready.py'
def run_fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1019-{name}-') as td:
        dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing for {name}: {old!r}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print(f'PASS negative mutation rejected: {name}')
run_fixture('absolute-threshold-restored','assets/app.v1019.js',"high=ratio>0&&(rank===true||rank==='dominant')?' high':''","high=ratio>=.8?' high':''")
run_fixture('worker-version-prompt-restored','assets/app.v1019.js','const validIndex=allIndex.filter', 'maybeShowDatabaseUpdate(meta);const validIndex=allIndex.filter')
run_fixture('release-marker-cache-weakened','assets/app.v1019.js',"{cache:'no-store'}","{cache:'force-cache'}")
run_fixture('release-ready-gate-lost','assets/app.v1019.js','marker?.releaseReady===true','true')
run_fixture('refresh-cache-bust-lost','assets/app.v1019.js',"u.searchParams.set('_r',String(Date.now()));",'')
run_fixture('deploy-before-release','.github/workflows/pages.yml','needs: [build, release]','needs: build')
run_fixture('main-deploy-restored','.github/workflows/pages.yml',"if: startsWith(github.ref, 'refs/tags/v')\n    runs-on: ubuntu-latest\n    timeout-minutes: 10\n    needs: [build, release]","if: github.ref == 'refs/heads/main'\n    runs-on: ubuntu-latest\n    timeout-minutes: 10\n    needs: build")
run_fixture('release-marker-not-ready','data/release.json','"releaseReady":true','"releaseReady":false')
with tempfile.TemporaryDirectory(prefix='vsdb-1019-false-positive-') as td:
    dst=Path(td)/'repo'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless 1.0.19 verifier control -->\n',encoding='utf-8',newline='\n')
    subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],check=True)
print('PASS Database 1.0.19 negative mutations + harmless false-positive control')
