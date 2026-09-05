from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
python=sys.executable
audit=root/'tools/audit_database.py'
builder=root/'tools/build_pages_artifact.py'
repair=root/'tools/repair_repository.py'

def run(args, expect=0, contains=None, cwd=None):
    p=subprocess.run(args,cwd=cwd or root,text=True,capture_output=True)
    out=(p.stdout or '')+(p.stderr or '')
    if (p.returncode==0)!=(expect==0):
        raise SystemExit(f'Unexpected return code {p.returncode}: {out}')
    if contains and contains not in out:
        raise SystemExit(f'Missing expected text {contains!r}: {out}')
    return out

# Normal source audit must pass regardless of repository-owned root .git metadata.
out=run([python,str(audit),'--source-tree',str(root)])
if 'VulkanScope Database audit tool 0.39.26' not in out:
    raise SystemExit('audit version fingerprint missing')
run([python,str(repair),'--check'])

# Stale files left by an in-place ZIP extraction must be detected explicitly.
stale_app=root/'assets/app.v0000.js'
try:
    stale_app.write_text('// stale',encoding='utf-8')
    run([python,str(audit),'--source-tree',str(root)],expect=1,contains='exactly one versioned frontend app asset')
finally:
    stale_app.unlink(missing_ok=True)

stale_workflow=root/'.github/workflows/stale.yml'
try:
    stale_workflow.write_text('name: stale\n',encoding='utf-8')
    run([python,str(audit),'--source-tree',str(root)],expect=1,contains='exactly one GitHub Actions workflow')
finally:
    stale_workflow.unlink(missing_ok=True)

# Pages staging copies an exact asset allow-list, so a stale source app must not be deployed.
with tempfile.TemporaryDirectory(prefix='vulkanscope-pages-audit-') as tmp:
    site=Path(tmp)/'_site'
    stale_app.write_text('// stale',encoding='utf-8')
    try:
        run([python,str(builder),str(site)])
        if (site/'assets/app.v0000.js').exists():
            raise SystemExit('stale source asset leaked into staged Pages artifact')
    finally:
        stale_app.unlink(missing_ok=True)
    run([python,str(audit),'--artifact-tree',str(site)])
    (site/'.git').mkdir()
    (site/'.git/HEAD').write_text('x',encoding='utf-8')
    run([python,str(audit),'--artifact-tree',str(site)],expect=1,contains='forbidden Pages artifact')

print('VulkanScope Database audit hygiene regression tests: ALL PASS')
