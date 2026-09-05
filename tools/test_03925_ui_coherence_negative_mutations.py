from pathlib import Path
import tempfile, shutil, subprocess, sys
root=Path(__file__).resolve().parents[1]
ver=root/'tools/verify_03925_ui_coherence.py'
mutations=[
 ('index.html','aria-live="polite"','aria-live="off"','loading-live-region'),
 ('index.html','app.v03927.js?v=03927','app.v03927.js','cache-bust'),
 ('assets/app.v03927.js','notice encyclopedia-evidence-note','encyclopedia-evidence-note','shared-notice-language'),
 ('assets/app.v03927.js','entries.length>=24','entries.length>=240','result-bound'),
]
for rel,a,b,label in mutations:
    with tempfile.TemporaryDirectory(prefix='db03925-ui-mut-') as d:
        t=Path(d); shutil.copytree(root,t,dirs_exist_ok=True)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if a not in s: raise SystemExit(f'mutation source missing: {label}')
        p.write_text(s.replace(a,b,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(ver),str(t)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        if r.returncode==0: raise SystemExit(f'negative mutation accepted: {label}')
with tempfile.TemporaryDirectory(prefix='db03925-ui-fp-') as d:
    t=Path(d); shutil.copytree(root,t,dirs_exist_ok=True)
    p=t/'assets/site.v0390.css'; p.write_text(p.read_text(encoding='utf-8')+'\n',encoding='utf-8')
    r=subprocess.run([sys.executable,str(ver),str(t)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    if r.returncode: raise SystemExit('false-positive harmless CSS whitespace rejected')
print('PASS Database 0.39.25 UI coherence negative mutations and false-positive control')
