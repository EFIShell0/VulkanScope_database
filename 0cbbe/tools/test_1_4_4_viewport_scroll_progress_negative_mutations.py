from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
required=['index.html','assets/app.v1404.js','assets/site.v1404.css','worker/src/index.js','rules/PROJECT_RULES.md','data/release.json','tools/repair_repository.py','tools/build_pages_artifact.py']
cases=[
 ('app-root-transform','assets/site.v1404.css','@keyframes startupShellReveal{from{opacity:0}to{opacity:1}}','@keyframes startupShellReveal{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:none}}'),
 ('progress-not-fixed','assets/site.v1404.css','.page-progress{position:fixed;inset:0 0 auto 0;height:3px;z-index:230;','.page-progress{position:absolute;inset:0 0 auto 0;height:3px;z-index:230;'),
 ('rail-not-fixed','assets/site.v1404.css','.viewport-scrollbar{position:fixed;z-index:220;top:0;right:0;bottom:0;width:18px;','.viewport-scrollbar{position:absolute;z-index:220;top:0;right:0;bottom:0;width:18px;'),
 ('thumb-ratio','assets/app.v1404.js','thumbHeight=Math.max(46,Math.min(trackHeight,trackHeight*(viewport/doc)))','thumbHeight=trackHeight'),
 ('thumb-position','assets/app.v1404.js','thumb.style.transform=`translateY(${travel*ratio}px)`','thumb.style.transform=`translateY(0)`'),
 ('progress-sync','assets/app.v1404.js',"if(progress)progress.classList.toggle('is-scrollable',scrollable)","if(progress)progress.classList.remove('is-scrollable')"),
 ('scroll-listener','assets/app.v1404.js',"window.addEventListener('scroll',()=>{queuePageScrollUi(true);queueCompareStickyState()},{passive:true})","window.addEventListener('scroll',()=>queueCompareStickyState(),{passive:true})"),
 ('mobile-rail','assets/site.v1404.css','@media(max-width:760px){.viewport-scrollbar{width:16px;','@media(max-width:760px){.viewport-scrollbar{width:48px;'),
 ('release-marker','data/release.json','"databaseVersion":"1.4.4"','"databaseVersion":"1.4.3"'),
]
temps=[]
try:
    for name,rel,needle,repl in cases:
        td=tempfile.TemporaryDirectory(prefix=f'vsdb-144-neg-{name}-'); temps.append(td); dst=Path(td.name)/'src'; dst.mkdir()
        for f in required:
            out=dst/f; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,out)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if needle not in s: raise SystemExit(f'negative fixture needle missing for {name}: {needle}')
        p.write_text(s.replace(needle,repl,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(root/'tools/verify_1_4_4_viewport_scroll_progress.py'),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}\n{r.stdout}')
    print(f'PASS Database 1.4.4 negative mutations: {len(cases)} expected failures')
finally:
    for td in temps: td.cleanup()
