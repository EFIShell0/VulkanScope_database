from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
required=['index.html','assets/app.v1403.js','assets/site.v1403.css','worker/src/index.js','rules/PROJECT_RULES.md','data/release.json','tools/repair_repository.py','tools/build_pages_artifact.py']
cases=[
 ('panel-class-collision','index.html','class="database-loading-panel"','class="database-loading"'),
 ('generic-body-style','assets/site.v1403.css','.database-loading-panel{display:flex','.database-loading{display:flex'),
 ('viewport-position','assets/site.v1403.css','body.startup-layout-hold #databaseLoading{position:fixed','body.startup-layout-hold #databaseLoading{position:static'),
 ('viewport-center','assets/site.v1403.css','left:50%;top:50%;right:auto;bottom:auto;transform:translate(-50%,-50%)','left:0;top:50%;right:auto;bottom:auto;transform:translateY(-50%)'),
 ('address-row-class','assets/app.v1403.js',"?' settings-info-row-address':''","?'':''"),
 ('address-wrap','assets/site.v1403.css','text-overflow:clip;white-space:normal;overflow-wrap:anywhere;word-break:break-all','text-overflow:ellipsis;white-space:nowrap;overflow-wrap:normal;word-break:normal'),
 ('mobile-fit','assets/site.v1403.css','.settings-info-row-address .network-address-toggle{grid-template-columns:28px minmax(0,1fr) auto;gap:6px}','.settings-info-row-address .network-address-toggle{grid-template-columns:30px 260px 66px;gap:10px}'),
 ('coupled-address-state','assets/app.v1403.js','const networkAddressReveal={active:false,ipv4:false,ipv6:false,pseudo:false};','const networkAddressReveal={ipv4:false,ipv6:false};'),
 ('release-marker','data/release.json','"databaseVersion":"1.4.3"','"databaseVersion":"1.4.2"'),
]
temps=[]
try:
    for name,rel,needle,repl in cases:
        td=tempfile.TemporaryDirectory(prefix=f'vsdb-143-neg-{name}-'); temps.append(td); dst=Path(td.name)/'src'; dst.mkdir()
        for f in required:
            out=dst/f; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,out)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if needle not in s: raise SystemExit(f'negative fixture needle missing for {name}: {needle}')
        p.write_text(s.replace(needle,repl,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(root/'tools/verify_1_4_3_startup_loader_address_fit.py'),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode==0:
            raise SystemExit(f'negative mutation unexpectedly passed: {name}\n{r.stdout}')
    print(f'PASS Database 1.4.3 negative mutations: {len(cases)} expected failures')
finally:
    for td in temps: td.cleanup()
