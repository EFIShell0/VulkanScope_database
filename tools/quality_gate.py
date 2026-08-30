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
run(sys.executable,'tools/verify_vulkanscope_04132.py')
run(sys.executable,'tools/repair_repository.py','--check')
if (root/'regression/0.39.13_to_0.39.14_contract.json').exists(): run(sys.executable,'tools/verify_regression_contract.py')
run(sys.executable,'tools/test_existing_repo_overlay.py')
run(sys.executable,'tools/audit_database.py','--source-tree','.')
run(sys.executable,'tools/test_audit_hygiene.py')
run('node','--check','assets/app.v03914.js')
run('node','tools/test_routes.mjs')
run('node','tools/test_compare_contract.mjs')
run('node','--check','worker/src/index.js')
run('node','--check','worker/tests/contract.mjs')
run('node','worker/tests/contract.mjs')
con=sqlite3.connect(':memory:')
for migration in sorted((root/'worker/migrations').glob('*.sql')): con.executescript(migration.read_text(encoding='utf-8'))
assert con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='report_payload_chunks'").fetchone()
print('PASS D1 migration chain')
with tempfile.TemporaryDirectory(prefix='vulkanscope-db-pages-') as td:
    run(sys.executable,'tools/build_pages_artifact.py',td)
    run(sys.executable,'tools/audit_database.py','--artifact-tree',td)
print('VulkanScope Database quality gate: PASS')
