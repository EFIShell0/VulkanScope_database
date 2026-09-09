#!/usr/bin/env python3
from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_0_6_ci_audit_hardening.py'
mutations=[
    ('worker/package.json','"sharp": "0.35.4"','"sharp": "0.34.5"','vulnerable-sharp-override'),
    ('worker/package.json','"security:audit": "node scripts/security-audit.mjs"','"security:audit": "npm audit --audit-level=high"','lockless-audit-regression'),
    ('worker/scripts/security-audit.mjs',"'--package-lock-only'","'--package-lock-only-broken'",'audit-lock-bootstrap-removal'),
    ('tools/generate_encyclopedia_03924.py',"write_bytes(('window.VULKANSCOPE_ENCYCLOPEDIA='+payload+';\\n').encode('utf-8'))","write_text('window.VULKANSCOPE_ENCYCLOPEDIA='+payload+';\\n',encoding='utf-8')",'windows-newline-regression'),
    ('tools/pages.workflow.yml','python tools/verify_1_0_2_producer_baseline.py --skip-version','python tools/verify_1_0_2_producer_baseline.py','historical-verifier-current-identity-regression'),
    ('tools/pages.workflow.yml','run: python tools/test_0809_floor_encyclopedia_state_machine.py','run: python tools/verify_0809_floor_encyclopedia.py','windows-encyclopedia-regeneration-gate-removal'),
]
for rel,a,b,name in mutations:
    with tempfile.TemporaryDirectory(prefix='vsdb106-neg-') as td:
        dst=Path(td)/'db'; shutil.copytree(root,dst)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if a not in s: raise SystemExit('FAIL mutation source missing: '+name)
        p.write_text(s.replace(a,b,1),encoding='utf-8',newline='\n')
        # keep checked-in workflow equal for mutations targeting canonical workflow, so failure is semantic not copy drift
        if rel=='tools/pages.workflow.yml':
            (dst/'.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit('FAIL negative mutation accepted: '+name)

with tempfile.TemporaryDirectory(prefix='vsdb106-control-') as td:
    dst=Path(td)/'db'; shutil.copytree(root,dst)
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n',encoding='utf-8',newline='\n')
    r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],capture_output=True,text=True)
    if r.returncode!=0: raise SystemExit('FAIL harmless changelog whitespace false-positive control rejected\n'+r.stdout+r.stderr)
print('PASS VulkanScope Database 1.0.7 CI/audit hardening negative mutations')
