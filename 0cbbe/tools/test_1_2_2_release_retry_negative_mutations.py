from __future__ import annotations
from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_2_2_release_retry.py'
required=['assets/app.v1202.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','worker/src/index.js','worker/tests/contract.mjs','data/release.json','.github/workflows/pages.yml','tools/pages.workflow.yml']
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-122-negative-') as td:
        d=Path(td)
        for r in required:
            dst=d/r; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/r,dst)
        p=d/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'{name}: mutation token absent')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(d)],text=True,capture_output=True)
        if r.returncode==0: raise SystemExit(f'{name}: verifier accepted mutation')
        print('PASS negative',name)
fixture('detail-tab-sync','assets/app.v1202.js','function syncDetailTabUi(ensureVisible=false)','function syncDetailTabUiBroken(ensureVisible=false)')
fixture('temporal-sort','assets/app.v1202.js',"if(field==='submitted'){const t=submissionEpoch(r.submittedAt)","if(field==='submitted'){const t=Date.parse(formatSubmitted(r.submittedAt))")
fixture('temporal-age-filter','assets/app.v1202.js','submissionAgeFilter:(r,v)=>{const days=Number(v),t=submissionEpoch(r.submittedAt)','submissionAgeFilter:(r,v)=>{const days=Number(v),t=Date.parse(formatSubmitted(r.submittedAt))')
fixture('network-physical-label','assets/app.v1202.js',"['Browser effective network class',navigator.connection?.effectiveType?","['Connection profile',navigator.connection?.effectiveType?")
fixture('favorite-confirmation','assets/app.v1202.js','const active=await requestFavoriteToggle(button.dataset.favoriteReport||\'\')','const active=toggleFavorite(button.dataset.favoriteReport||\'\')')
fixture('compare-sticky','assets/site.v0390.css','.compare-workspace{position:sticky;','.compare-workspace{position:relative;')
fixture('scroll-endpoint','assets/app.v1202.js','setButton(up,scrollable,y<=2);setButton(down,scrollable,y>=max-2)','setButton(up,scrollable&&y>2);setButton(down,scrollable&&y<max-2)')
fixture('release-retry','.github/workflows/pages.yml','for attempt in 1 2 3 4 5','for attempt in 1')
print('PASS 1.2.2 negative mutation suite')
