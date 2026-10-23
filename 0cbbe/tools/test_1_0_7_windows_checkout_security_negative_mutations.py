#!/usr/bin/env python3
from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_0_7_windows_checkout_security.py'
mutations=[
    ('.gitattributes','* text=auto eol=lf','* text=auto','lf-checkout-policy-removal'),
    ('worker/scripts/security-audit.mjs','const fromRun=process.env.npm_execpath','const fromRun=undefined','npm-execpath-removal'),
    ('worker/scripts/security-audit.mjs','spawnSync(process.execPath,[cli,...args]','spawnSync(\'npm.cmd\',args','direct-npm-cmd-regression'),
    ('worker/scripts/security-audit.mjs','if(!fs.existsSync(lockPath))','if(true)','unconditional-lock-regeneration'),
    ('tools/pages.workflow.yml','      - name: Exercise Windows security-audit subprocess path\n        working-directory: worker\n        run: npm run security:audit\n','', 'windows-audit-gate-removal'),
    ('tools/pages.workflow.yml','uses: actions/setup-node@v7','uses: actions/setup-node@v6','setup-node-downgrade'),
]
for rel,a,b,name in mutations:
    with tempfile.TemporaryDirectory(prefix='vsdb107-neg-') as td:
        dst=Path(td)/'db'; shutil.copytree(root,dst)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if a not in s: raise SystemExit('FAIL mutation source missing: '+name)
        p.write_text(s.replace(a,b,1),encoding='utf-8',newline='\n')
        if rel=='tools/pages.workflow.yml':
            (dst/'.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit('FAIL negative mutation accepted: '+name)

with tempfile.TemporaryDirectory(prefix='vsdb107-crlf-') as td:
    dst=Path(td)/'db'; shutil.copytree(root,dst)
    p=dst/'assets/encyclopedia.v03924.js'; raw=p.read_bytes()
    if not raw.endswith(b'\n'): raise SystemExit('FAIL Encyclopedia fixture missing LF terminator')
    p.write_bytes(raw[:-1]+b'\r\n')
    r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],capture_output=True,text=True)
    if r.returncode==0: raise SystemExit('FAIL negative mutation accepted: encyclopedia-crlf-checkout')

with tempfile.TemporaryDirectory(prefix='vsdb107-control-') as td:
    dst=Path(td)/'db'; shutil.copytree(root,dst)
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n',encoding='utf-8',newline='\n')
    r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],capture_output=True,text=True)
    if r.returncode!=0: raise SystemExit('FAIL harmless changelog whitespace false-positive control rejected\n'+r.stdout+r.stderr)
print('PASS VulkanScope Database 1.0.7 Windows checkout/security-audit negative mutations')
