from pathlib import Path
import shutil, subprocess, sys, tempfile

root = Path(__file__).resolve().parents[1]

def run(tree: Path, *args, expect=0):
    p = subprocess.run([sys.executable, *args], cwd=tree, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if (p.returncode == 0) != (expect == 0):
        print(p.stdout)
        raise SystemExit(f'unexpected exit={p.returncode} for {args}, expected {expect}')
    return p.stdout

with tempfile.TemporaryDirectory(prefix='vulkanscope-db-overlay-') as td:
    t = Path(td) / 'repo'
    shutil.copytree(root, t, ignore=shutil.ignore_patterns('.git','node_modules','.wrangler','_site','__pycache__'))
    # Simulate legitimate history/source files present in a long-lived Git checkout but absent
    # from the predecessor release ZIP. Source-overlay regression must tolerate these.
    (t / '.gitattributes').write_text('* text=auto\n', encoding='utf-8')
    (t / 'assets' / 'site.v0001.css').write_text('/* historical source */\n', encoding='utf-8')
    (t / 'rules' / 'HISTORICAL_LOCAL_AUDIT.md').write_text('# historical\n', encoding='utf-8')
    # Overlay extraction leaves the predecessor app behind; repair must be explicit and deterministic.
    shutil.copy2(t / 'assets' / 'app.v1006.js', t / 'assets' / 'app.v03916.js')
    # Simulate the real 1.0.4 failure: an ignored but still Git-tracked legacy lock survives an overlay.
    stale_lock = t / 'worker' / 'package-lock.json'
    stale_lock.write_text('{\n  \"name\": \"vulkanscope-database-worker\",\n  \"lockfileVersion\": 3,\n  \"packages\": {\n    \"\": {\"name\": \"vulkanscope-database-worker\", \"devDependencies\": {\"wrangler\": \"^4.125.0\"}},\n    \"node_modules/wrangler\": {\"version\": \"4.125.0\", \"integrity\": \"sha512-stale-fixture\"}\n  }\n}\n', encoding='utf-8')
    stale = run(t, 'tools/verify_optional_npm_lock.py', expect=1)
    if 'stale optional lock' not in stale:
        raise SystemExit('legacy optional lock mismatch was not rejected before repair')
    chk = run(t, 'tools/repair_repository.py', '--check', expect=1)
    if 'stale versioned frontend assets' not in chk:
        raise SystemExit('repository repair check did not identify stale predecessor app')
    workflow = (t / '.github' / 'workflows' / 'pages.yml').read_text(encoding='utf-8')
    apply_token = 'python tools/repair_repository.py --apply'
    check_token = 'python tools/repair_repository.py --check'
    audit_token = 'python tools/audit_database.py --version'
    if any(token not in workflow for token in (apply_token, check_token, audit_token)):
        raise SystemExit('GitHub Actions preflight is missing repair/apply/check/audit token')
    apply_i = workflow.index(apply_token)
    check_i = workflow.index(check_token, apply_i)
    audit_i = workflow.index(audit_token, check_i)
    if not (apply_i < check_i < audit_i):
        raise SystemExit('GitHub Actions build preflight does not repair stale overlay assets before checking/auditing')
    run(t, 'tools/repair_repository.py', '--apply')
    if stale_lock.exists():
        raise SystemExit('repository repair left ignored legacy worker/package-lock.json behind')
    run(t, 'tools/verify_optional_npm_lock.py')
    run(t, 'tools/repair_repository.py', '--check')
    run(t, 'tools/audit_database.py', '--version')
    if (t / 'assets' / 'app.v03916.js').exists():
        raise SystemExit('CI-style repository repair left stale versioned frontend asset behind')
    out = run(t, 'tools/verify_regression_contract.py')
    if 'mode=source-overlay' not in out:
        raise SystemExit('source-overlay mode was not exercised')
    # Strict release-package mode must still reject the same extras.
    strict = run(t, 'tools/verify_regression_contract.py', '--strict-tree', expect=1)
    if 'unallowlisted release-package file' not in strict:
        raise SystemExit('strict package mode did not reject source-only extras')
    # Generated index must remain valid after normal regeneration and must not be SHA-pinned.
    run(t, 'tools/build_index.py')
    run(t, 'tools/verify_regression_contract.py')
    # A predecessor-owned immutable file must still be protected in overlay mode.
    p = t / '400.html'
    p.write_bytes(p.read_bytes() + b'\n')
    bad = run(t, 'tools/verify_regression_contract.py', expect=1)
    if 'unallowlisted predecessor regression: 400.html' not in bad:
        raise SystemExit('overlay regression did not detect immutable predecessor mutation')

print('PASS existing-repository overlay / generated-index / strict-package regression fixtures')
