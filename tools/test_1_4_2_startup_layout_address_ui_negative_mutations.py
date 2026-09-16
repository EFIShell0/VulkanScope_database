from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
required=['index.html','assets/app.v1402.js','assets/site.v1402.css','worker/src/index.js','rules/PROJECT_RULES.md','data/release.json','tools/repair_repository.py','tools/build_pages_artifact.py']
cases=[
 ('startup-body','index.html','<body class="database-loading startup-layout-hold">','<body class="database-loading">'),
 ('startup-shell-css','assets/site.v1402.css','body.startup-layout-hold .topbar','body.startup-layout-open .topbar'),
 ('startup-finish-owner','assets/app.v1402.js',"body.classList.remove('startup-layout-hold');body.classList.add('startup-layout-ready')","body.classList.add('startup-layout-ready')"),
 ('startup-order','assets/app.v1402.js','render();renderSettingsFavorites();setDatabaseLoading(false);finishStartupLayout();','finishStartupLayout();render();renderSettingsFavorites();setDatabaseLoading(false);'),
 ('privacy-shield','assets/app.v1402.js','class="network-address-privacy-mark"','class="network-address-mark"'),
 ('coupled-address-state','assets/app.v1402.js','const networkAddressReveal={active:false,ipv4:false,ipv6:false,pseudo:false};','const networkAddressReveal={ipv4:false,ipv6:false};'),
 ('mosaic-opacity','assets/site.v1402.css','.network-address-toggle.is-masked .network-address-text{filter:blur(8px)','.network-address-toggle.is-masked .network-address-text{filter:blur(0)'),
 ('reduced-motion-mosaic','assets/site.v1402.css','.network-address-mosaic::after{animation:none!important;display:none}','.network-address-mosaic::after{animation:networkMosaicSheen 6.2s infinite}'),
 ('release-marker','data/release.json','"databaseVersion":"1.4.2"','"databaseVersion":"1.4.1"'),
]
temps=[]
try:
    for name,rel,needle,repl in cases:
        td=tempfile.TemporaryDirectory(prefix=f'vsdb-1402-neg-{name}-'); temps.append(td); dst=Path(td.name)/'src'; dst.mkdir()
        for f in required:
            out=dst/f; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,out)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if needle not in s: raise SystemExit(f'negative fixture needle missing for {name}: {needle}')
        p.write_text(s.replace(needle,repl,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(root/'tools/verify_1_4_2_startup_layout_address_ui.py'),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode==0:
            raise SystemExit(f'negative mutation unexpectedly passed: {name}\n{r.stdout}')
    print(f'PASS Database 1.4.2 negative mutations: {len(cases)} expected failures')
finally:
    for td in temps: td.cleanup()
