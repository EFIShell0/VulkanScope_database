from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='vsdb-1010-render-negative-') as td:
    fixture=Path(td)/'fixture'
    shutil.copytree(root, fixture, ignore=shutil.ignore_patterns('.git','node_modules','.wrangler','dist','_site','__pycache__'))
    app=fixture/'assets/app.v1010.js'
    text=app.read_text(encoding='utf-8')
    good="</td></tr>`});const pager="
    bad="</td></tr>`}).join('');const pager="
    if good not in text:
        raise SystemExit('fixture cannot locate corrected Reports row-array boundary')
    app.write_text(text.replace(good,bad,1),encoding='utf-8',newline='\n')
    r=subprocess.run([sys.executable,str(fixture/'tools/verify_1_0_10_reports_render_hotfix.py'),'--root',str(fixture)],text=True,capture_output=True)
    if r.returncode==0:
        raise SystemExit('negative mutation unexpectedly passed current verifier')
    output=(r.stdout or '')+(r.stderr or '')
    if 'prematurely serialized' not in output:
        raise SystemExit('negative mutation failed for the wrong reason:\n'+output)
print('PASS Database 1.0.10 negative mutation: reintroduced rows.join failure is rejected')
