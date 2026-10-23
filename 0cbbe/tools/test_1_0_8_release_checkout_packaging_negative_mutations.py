#!/usr/bin/env python3
from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_1_0_8_release_checkout_packaging.py'
mutations=[
    ('tools/pages.workflow.yml','          python tools/verify_regression_contract.py\n',
     '          python tools/verify_regression_contract.py --strict-tree\n','raw-tag-strict-tree-regression'),
    ('tools/package_release.py',"subprocess.run([sys.executable, str(root/'tools/verify_regression_contract.py')], cwd=root, check=True)",
     "subprocess.run([sys.executable, str(root/'tools/verify_regression_contract.py'), '--strict-tree'], cwd=root, check=True)",
     'packager-raw-root-strict-tree-regression'),
    ('tools/package_release.py',"str(extracted/'tools/verify_regression_contract.py'), '--strict-tree'",
     "str(extracted/'tools/verify_regression_contract.py')",'clean-extract-strict-removal'),
    ('tools/package_release.py',"if (extracted/rel).read_bytes() != (root/rel).read_bytes():",
     "if False:",'clean-extract-byte-equality-removal'),
    ('tools/package_release.py',"VulkanScope-Database-1.0.8.zip","VulkanScope-Database-1.0.7.zip",'release-output-identity-regression'),
]
for rel,a,b,name in mutations:
    with tempfile.TemporaryDirectory(prefix='vsdb108-neg-') as td:
        dst=Path(td)/'db'; shutil.copytree(root,dst)
        p=dst/rel; s=p.read_text(encoding='utf-8')
        if a not in s: raise SystemExit('FAIL mutation source missing: '+name)
        p.write_text(s.replace(a,b,1),encoding='utf-8',newline='\n')
        if rel=='tools/pages.workflow.yml':
            (dst/'.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit('FAIL negative mutation accepted: '+name)

with tempfile.TemporaryDirectory(prefix='vsdb108-control-') as td:
    dst=Path(td)/'db'; shutil.copytree(root,dst)
    p=dst/'changelog.md'; p.write_text(p.read_text(encoding='utf-8')+'\n',encoding='utf-8',newline='\n')
    r=subprocess.run([sys.executable,str(ver),'--root',str(dst)],capture_output=True,text=True)
    if r.returncode!=0: raise SystemExit('FAIL harmless changelog whitespace false-positive control rejected\n'+r.stdout+r.stderr)
print('PASS VulkanScope Database 1.0.8 release-boundary negative mutations')
