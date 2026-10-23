from pathlib import Path
import json, subprocess, sys, tempfile, shutil
root=Path(__file__).resolve().parents[1]
pkg=root/'worker/package.json'
audit=root/'worker/scripts/security-audit.mjs'
verifier=root/'tools/verify_optional_npm_lock.py'
original=json.loads(pkg.read_text(encoding='utf-8'))
assert original['devDependencies']['wrangler']=='4.152.0'
assert original['overrides']=={'sharp':'0.35.5','undici':'7.30.1'}
security=audit.read_text(encoding='utf-8')
assert "runNpm(['audit','--audit-level=high'])" in security
assert '--force' not in security and '--omit' not in security
with tempfile.TemporaryDirectory(prefix='vsdb401-security-negative-') as td:
    tmp=Path(td);(tmp/'worker').mkdir();(tmp/'tools').mkdir()
    shutil.copy2(verifier,tmp/'tools/verify_optional_npm_lock.py')
    target=tmp/'worker/package.json'
    for key,value in [('wrangler','4.130.0'),('sharp','0.35.4'),('undici','7.29.0')]:
        data=json.loads(json.dumps(original))
        if key=='wrangler':data['devDependencies']['wrangler']=value
        else:data['overrides'][key]=value
        target.write_text(json.dumps(data),encoding='utf-8')
        p=subprocess.run([sys.executable,str(tmp/'tools/verify_optional_npm_lock.py')],capture_output=True,text=True)
        if p.returncode==0:raise SystemExit('FAIL rejected vulnerable toolchain pin not detected: '+key)
    target.write_text(json.dumps(original),encoding='utf-8')
    p=subprocess.run([sys.executable,str(tmp/'tools/verify_optional_npm_lock.py')],capture_output=True,text=True)
    if p.returncode:raise SystemExit('FAIL safe pins rejected: '+p.stdout+p.stderr)
    lock={'lockfileVersion':3,'packages':{'':{'name':'vulkanscope-database-worker','devDependencies':{'wrangler':'4.152.0'}},'node_modules/wrangler':{'version':'4.152.0','integrity':'sha512-test'},'node_modules/sharp':{'version':'0.35.5','integrity':'sha512-test'},'node_modules/undici':{'version':'7.29.0','integrity':'sha512-test'}}}
    (tmp/'worker/package-lock.json').write_text(json.dumps(lock),encoding='utf-8')
    p=subprocess.run([sys.executable,str(tmp/'tools/verify_optional_npm_lock.py')],capture_output=True,text=True)
    if p.returncode==0:raise SystemExit('FAIL outdated resolved undici not detected')
print('PASS 4.0.3 security gate: safe pins, obsolete-pin negatives, optional resolved-lock negative, fail-closed npm audit command')
