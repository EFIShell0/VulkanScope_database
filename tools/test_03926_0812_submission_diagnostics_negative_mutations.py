from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_03926_0812_submission_diagnostics.py'
mutations=[('worker/src/index.js',"validation='producer_identity'","validation='envelope_or_report_contract'"),('worker/src/index.js',"'vulkan_1_4_362_registry_contract'","'envelope_or_report_contract'"),('worker/tests/contract.mjs',"current0812.application.versionCode=812","current0812.application.versionCode=810")]
for rel,a,b in mutations:
    with tempfile.TemporaryDirectory() as td:
        dst=Path(td)/'db';shutil.copytree(root,dst)
        p=dst/rel;s=p.read_text(encoding='utf-8');assert a in s;p.write_text(s.replace(a,b,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),str(dst)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit('FAIL negative mutation accepted: '+rel+' '+a)
print('PASS Database 0.39.26 submission-diagnostics negative mutations')
