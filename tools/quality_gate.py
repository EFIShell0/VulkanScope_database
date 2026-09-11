from pathlib import Path
import subprocess,sys,tempfile,sqlite3
root=Path(__file__).resolve().parents[1]

def run(*cmd,cwd=root):
    print('+',' '.join(map(str,cmd)))
    r=subprocess.run(cmd,cwd=cwd,text=True)
    if r.returncode: raise SystemExit(r.returncode)

run(sys.executable,'tools/test_utf8_text_io.py')
run(sys.executable,'tools/verify_optional_npm_lock.py')
run(sys.executable,'tools/verify_vulkan_registry.py')
run('node','tools/test_report_text_identity.mjs')
run(sys.executable,'tools/repair_repository.py','--apply')
run(sys.executable,'tools/repair_repository.py','--check')
run(sys.executable,'tools/verify_regression_contract.py')
run(sys.executable,'tools/verify_1_0_18_full_audit.py')
run(sys.executable,'tools/test_1_0_18_full_audit_negative_mutations.py')
run(sys.executable,'tools/audit_database.py','--source-tree','.')
run('node','--check','assets/app.v1018.js')
run('node','--check','assets/encyclopedia.v03924.js')
run('node','--check','worker/src/index.js')
run('node','--check','worker/tests/contract.mjs')
run('node','worker/tests/contract.mjs')
con=sqlite3.connect(':memory:')
for migration in sorted((root/'worker/migrations').glob('*.sql')): con.executescript(migration.read_text(encoding='utf-8'))
assert con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='report_payload_chunks'").fetchone()
print('PASS D1 migration chain')
with tempfile.TemporaryDirectory(prefix='vulkanscope-db-pages-') as td:
    run(sys.executable,'tools/build_pages_artifact.py',td)
    staged=Path(td)
    assert (staged/'assets/app.v1018.js').is_file()
    assert (staged/'assets/site.v0390.css').is_file()
    assert (staged/'assets/hdr/hdr10_plus_v1014.png').is_file()
    assert not (staged/'worker').exists()
    assert not (staged/'rules').exists()
    run(sys.executable,'tools/audit_database.py','--artifact-tree',td)
    print('PASS Pages allow-list artifact boundary')
print('VulkanScope Database 1.0.18 quality gate: PASS')
