from pathlib import Path
import shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parents[1]; verifier=root/'tools/verify_1_2_3_browser_motion_mobile.py'
required=['assets/app.v1203.js','assets/browser-compat.v1203.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json']
def fixture(name,rel,old,new):
  with tempfile.TemporaryDirectory(prefix='vsdb-123-negative-') as td:
    d=Path(td)
    for r in required:
      dst=d/r; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/r,dst)
    p=d/rel; s=p.read_text(encoding='utf-8')
    if old not in s: raise SystemExit(f'{name}: mutation token absent')
    p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
    q=subprocess.run([sys.executable,str(verifier),'--root',str(d)],capture_output=True,text=True)
    if q.returncode==0: raise SystemExit(f'{name}: verifier accepted mutation')
    print('PASS negative',name)
fixture('browser-floor','assets/browser-compat.v1203.js','chromium:84,firefox:86,safari:14.1','chromium:80,firefox:80,safari:13')
fixture('english-time','assets/app.v1203.js',"const browserLanguage=()=> 'en-US'","const browserLanguage=()=>navigator.language||'en-US'")
fixture('top-endpoint','assets/app.v1203.js',"classList.toggle('at-page-top',atTop)","classList.toggle('at-page-top',false)")
fixture('mobile-overflow','assets/site.v0390.css','html,body{max-width:100%;overflow-x:hidden}','html,body{max-width:100%}')
fixture('compat-page','index.html','This browser is not supported','Browser notice')
print('PASS 1.2.3 negative mutation suite')
