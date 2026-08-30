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
    shutil.copy2(t / 'assets' / 'app.v03914.js', t / 'assets' / 'app.v03913.js')
    chk = run(t, 'tools/repair_repository.py', '--check', expect=1)
    if 'stale versioned frontend assets' not in chk:
        raise SystemExit('repository repair check did not identify stale predecessor app')
    run(t, 'tools/repair_repository.py', '--apply')
    run(t, 'tools/repair_repository.py', '--check')
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
