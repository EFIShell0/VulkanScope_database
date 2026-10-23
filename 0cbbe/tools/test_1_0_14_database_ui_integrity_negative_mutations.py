from __future__ import annotations
from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
verifier=root/'tools/verify_1_0_14_database_ui_integrity.py'

def run_fixture(name, rel, old, new):
    with tempfile.TemporaryDirectory(prefix=f'vsdb-1014-{name}-') as td:
        dst=Path(td)/'repo'
        shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
        p=dst/rel
        s=p.read_text(encoding='utf-8')
        if old not in s:
            raise SystemExit(f'fixture token missing for {name}: {old!r}')
        p.write_text(s.replace(old,new,1),encoding='utf-8',newline='\n')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],capture_output=True,text=True)
        if r.returncode==0:
            raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print(f'PASS negative mutation rejected: {name}')

run_fixture('toggle-slides-right','assets/site.v0390.css','justify-content:flex-start!important;gap:0!important','justify-content:space-between!important;gap:10px!important')
run_fixture('toggle-padding-shifts','assets/site.v0390.css','.reports-table.submitted-expanded th:first-child,.reports-table.submitted-expanded td.submitted-cell{padding-left:6px;padding-right:12px}', '.reports-table.submitted-expanded th:first-child,.reports-table.submitted-expanded td.submitted-cell{padding-left:12px;padding-right:12px}')
run_fixture('vendor-id-fabricated-fallback','assets/app.v1014.js',"r?.gpu?.vendorId??'Unknown'","r?.gpu?.vendorId??r?.gpu?.vendor??'Unknown'")
run_fixture('unknown-omitted','assets/app.v1014.js','[x.supported,x.unsupported,x.available,x.unavailable,x.not_applicable,x.unknown]','[x.supported,x.unsupported,x.available,x.unavailable,x.not_applicable]')
run_fixture('tied-max-lower-not-hatched','assets/app.v1014.js',"const max=Math.max(...xs);if(max<=0)return'';return v===max?'dominant':'subordinate'","const max=Math.max(...xs),winners=xs.filter(x=>x===max).length;if(max<=0||winners!==1)return'';return v===max?'dominant':'subordinate'")
run_fixture('subordinate-no-hatch','assets/site.v0390.css','repeating-linear-gradient(135deg,rgba(0,0,0,.86)','linear-gradient(rgba(0,0,0,.0),rgba(0,0,0,.0))')
run_fixture('zero-invisible','assets/site.v0390.css','.coverage.zero .coverage-bar{','.coverage.zero .coverage-bar.broken{')
run_fixture('reports-down-arrow','assets/app.v1014.js','aria-label="Open ${count} coverage reports"><span>${count} reports</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6l6 6-6 6"/>','aria-label="Open ${count} coverage reports"><span>${count} reports</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/>')
run_fixture('high-endpoint-unclamped','assets/site.v0390.css','left:clamp(4px,calc(var(--coverage-pct)*1%),calc(100% - 4px))','left:calc(var(--coverage-pct)*1%)')
run_fixture('hdr-filter-regression','assets/site.v0390.css','.hdr-logo-hdr10plus img{filter:none!important;max-height:30px}', '.hdr-logo-hdr10plus img{filter:invert(1)!important;max-height:30px}')
run_fixture('gamut-plain-text','assets/app.v1014.js',"gamutCell=v=>hasValue(v)?displayValueChip(v,'gamut')","gamutCell=v=>hasValue(v)?esc(v)")
run_fixture('developer-identity-loss','index.html','<strong>Semih Boran</strong><small>Nickname · EFI Shell</small>','<strong>Unknown</strong><small>Nickname · Unknown</small>')

with tempfile.TemporaryDirectory(prefix='vsdb-1014-false-positive-') as td:
    dst=Path(td)/'repo'
    shutil.copytree(root,dst,ignore=shutil.ignore_patterns('.git','node_modules','dist','_site','__pycache__','.wrangler'))
    p=dst/'changelog.md'
    p.write_text(p.read_text(encoding='utf-8')+'\n<!-- harmless verifier control -->\n',encoding='utf-8',newline='\n')
    subprocess.run([sys.executable,str(verifier),'--root',str(dst),'--skip-version'],check=True)
print('PASS Database 1.0.14 negative mutations + harmless false-positive control')
