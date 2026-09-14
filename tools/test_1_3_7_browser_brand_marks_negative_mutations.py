from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_3_7_browser_brand_marks.py'
fixtures=[
 ('chrome-map','assets/app.v1307.js',"'Google Chrome':'./assets/browser-logos/google-chrome.v1307.svg'","'Google Chrome':'https://example.invalid/chrome.svg'"),
 ('brave-detect','assets/app.v1307.js','const braveDetected=!!navigator.brave||brandEntries.some','const braveDetected=false&&brandEntries.some'),
 ('vivaldi-detect','assets/app.v1307.js',"['Vivaldi',/Vivaldi\\/","['Vivaldi',/BrokenVivaldi\\/"),
 ('generic-misbrand','assets/app.v1307.js',"'Chromium':'./assets/browser-logos/chromium.v1307.png',","'Chromium':'./assets/browser-logos/chromium.v1307.png','Chromium-based browser':'./assets/browser-logos/chromium.v1307.png',"),
 ('recolor','assets/site.v0390.css','.settings-browser-logo{display:block;width:32px;height:32px;max-width:32px;max-height:32px;object-fit:contain;filter:none!important;opacity:1}', '.settings-browser-logo{display:block;width:32px;height:32px;max-width:32px;max-height:32px;object-fit:contain;filter:grayscale(1)!important;opacity:1}'),
 ('missing-logo','assets/browser-logos/firefox.v1307.svg','<svg','<broken'),
 ('provenance','licenses/browser-marks.md','Brave: https://brave.com/brave-branding-assets/','Brave: https://example.invalid/'),
 ('staging','tools/build_pages_artifact.py',"'assets/browser-logos/safari.v1307.svg',",""),
 ('privacy','assets/app.v1307.js','canvas.toDataURL','canvas.toDataURL'),
 ('bridge','tools/build_pages_artifact.py',"'assets/app.v1306.js'","'assets/app.v1305.js'"),
 ('workflow','tools/pages.workflow.yml','python tools/verify_1_3_7_browser_brand_marks.py','python tools/verify_1_3_6_report_detail_workspace_raw_download.py'),
]
for name,rel,a,b in fixtures:
    with tempfile.TemporaryDirectory(prefix='vsdb137-mut-') as td:
        dst=Path(td)/'tree'; shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__'))
        p=dst/rel; t=p.read_text(encoding='utf-8')
        if name=='privacy':
            # Introduce a forbidden fingerprinting primitive rather than replace an existing token.
            p.write_text(t+'\n// canvas.toDataURL\n',encoding='utf-8')
        else:
            if a not in t: raise SystemExit(f'fixture token missing {name}: {a!r}')
            p.write_text(t.replace(a,b,1),encoding='utf-8')
        if rel=='tools/pages.workflow.yml': (dst/'.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if r.returncode==0: raise SystemExit(f'negative mutation escaped verifier: {name}')
print('PASS 1.3.7 browser brand-mark negative mutation suite')
