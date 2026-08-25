from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
python=sys.executable
audit=root/'tools/audit_database.py'
builder=root/'tools/build_pages_artifact.py'

def run(args, expect=0, contains=None):
    p=subprocess.run(args,cwd=root,text=True,capture_output=True)
    out=(p.stdout or '')+(p.stderr or '')
    if (p.returncode==0)!=(expect==0):
        raise SystemExit(f'Unexpected return code {p.returncode}: {out}')
    if contains and contains not in out:
        raise SystemExit(f'Missing expected text {contains!r}: {out}')
    return out

# The real checkout's root .git metadata, when present, is validated by the normal source audit.
run([python,str(audit),'--source-tree',str(root)])

negative=root/'assets/.audit-hygiene-negative'
try:
    (negative/'.git').mkdir(parents=True)
    (negative/'.git/HEAD').write_text('ref: refs/heads/test\n',encoding='utf-8')
    run([python,str(audit),'--source-tree',str(root)],expect=1,contains='forbidden source artifact assets/.audit-hygiene-negative/.git')
finally:
    shutil.rmtree(negative,ignore_errors=True)

with tempfile.TemporaryDirectory(prefix='vulkanscope-pages-audit-') as tmp:
    site=Path(tmp)/'_site'
    run([python,str(builder),str(site)])
    run([python,str(audit),'--artifact-tree',str(site)])
    (site/'.git').mkdir()
    (site/'.git/HEAD').write_text('x',encoding='utf-8')
    run([python,str(audit),'--artifact-tree',str(site)],expect=1,contains='forbidden Pages artifact')

print('VulkanScope Database audit hygiene regression tests: ALL PASS')
