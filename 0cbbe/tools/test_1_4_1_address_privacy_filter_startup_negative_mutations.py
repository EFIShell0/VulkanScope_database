from pathlib import Path
import shutil, subprocess, sys, tempfile
root=Path(__file__).resolve().parents[1]
required=['index.html','assets/app.v1401.js','assets/site.v1401.css','worker/src/index.js','rules/PROJECT_RULES.md','data/release.json']
cases=[
 ('coupled-address-state','assets/app.v1401.js','const networkAddressReveal={active:false,ipv4:false,ipv6:false,pseudo:false};','const networkAddressReveal={ipv4:false,ipv6:false};'),
 ('active-slot','assets/app.v1401.js',"networkAddressMarkup(n.activeAddress,activeFamily,'active')","networkAddressMarkup(n.activeAddress,activeFamily,'ipv6')"),
 ('startup-body','index.html','<body class="database-loading">','<body>'),
 ('startup-css','assets/site.v1401.css','body.database-loading #filters{display:none!important}','body.database-loading #filters{display:flex!important}'),
 ('mosaic-layer','assets/site.v1401.css','.network-address-mosaic{grid-area:1/1;','.network-address-obscurer{grid-area:1/1;'),
 ('release-marker','data/release.json','"databaseVersion":"1.4.1"','"databaseVersion":"1.4.0"'),
]
temps=[]
try:
    for name,rel,needle,repl in cases:
        td=tempfile.TemporaryDirectory(prefix=f'vsdb-1401-neg-{name}-'); temps.append(td); dst=Path(td.name)/'src'; dst.mkdir()
        for f in required:
            out=dst/f; out.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,out)
        # verifier itself is executed from the real tree against --root
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if needle not in s: raise SystemExit(f'negative fixture needle missing for {name}: {needle}')
        p.write_text(s.replace(needle,repl,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(root/'tools/verify_1_4_1_address_privacy_filter_startup.py'),'--root',str(dst)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        if r.returncode==0:
            raise SystemExit(f'negative mutation unexpectedly passed: {name}\n{r.stdout}')
    print(f'PASS Database 1.4.1 negative mutations: {len(cases)} expected failures')
finally:
    for td in temps: td.cleanup()
