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
run(sys.executable,'tools/verify_1_0_20_release_state_handshake.py')
run(sys.executable,'tools/test_1_0_20_release_state_handshake_negative_mutations.py')
run(sys.executable,'tools/audit_database.py','--source-tree','.')
run('node','--check','assets/app.v1020.js')
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
    assert (staged/'assets/app.v1020.js').is_file()
    assert (staged/'assets/site.v0390.css').is_file()
    assert (staged/'assets/hdr/hdr10_plus_v1014.png').is_file()
    assert not (staged/'worker').exists()
    assert not (staged/'rules').exists()
    marker=__import__('json').loads((staged/'data/release.json').read_text(encoding='utf-8'))
    assert marker.get('releaseReady') is False
    run(sys.executable,'tools/audit_database.py','--artifact-tree',td)
    run(sys.executable,'tools/mark_release_ready.py',td)
    run(sys.executable,'tools/audit_database.py','--artifact-tree',td,'--require-release-ready')
    print('PASS Pages allow-list + release-ready transition boundary')
print('VulkanScope Database 1.0.20 quality gate: PASS')
