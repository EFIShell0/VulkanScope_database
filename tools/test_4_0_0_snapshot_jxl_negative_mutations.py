from __future__ import annotations
from pathlib import Path
import subprocess,sys,tempfile,shutil
root=Path(__file__).resolve().parents[1]
verify=root/'tools/verify_4_0_0_snapshot_jxl.py'
necessary=['assets','worker/migrations','worker/src/index.js','worker/wrangler.jsonc','tools/jxl_asset_manifest.json','tools/build_pages_artifact.py','tools/build_index.py','rules/PROJECT_RULES.md','index.html','jxl-unsupported.html']
with tempfile.TemporaryDirectory(prefix='vsdb4000-negative-') as td:
    dest=Path(td)
    for rel in necessary:
        src=root/rel; target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True)
        if src.is_dir():shutil.copytree(src,target,ignore=shutil.ignore_patterns('__pycache__'))
        else:shutil.copy2(src,target)
    def check(expect=True):
        p=subprocess.run([sys.executable,str(verify),'--root',str(dest)],capture_output=True,text=True)
        if (p.returncode==0)!=expect:raise SystemExit(('unexpected pass' if not expect else 'unexpected failure')+': '+p.stdout+p.stderr)
    check()
    mutations=[
        ('worker/src/index.js',lambda s:s.replace('async scheduled(controller,env,ctx)','async disabled(controller,env,ctx)',1)),
        ('worker/wrangler.jsonc',lambda s:s.replace('*/5 * * * *','0 0 * * *',1)),
        ('assets/browser-compat.v4000.js',lambda s:s.replace('img.naturalWidth===2', 'img.naturalWidth===3',1)),
        ('index.html',lambda s:s.replace('favicon-v0311.jxl','favicon-v0311.png',1)),
        ('rules/PROJECT_RULES.md',lambda s:s.replace('## Release 4.0.0 Windows build-artifact hygiene and 1.4.13 compatibility requirements','## Removed release rules',1)),
        ('worker/src/index.js',lambda s:s.replace('snapshotIntent(env,id,now)', 'discardSnapshotIntent(env,id,now)',1)),
        ('worker/migrations/0004_snapshot_reconciliation.sql',lambda s:s.replace('CREATE TABLE IF NOT EXISTS snapshot_refresh_control','CREATE TABLE IF NOT EXISTS not_the_refresh_table',1)),
        ('assets/country-flags/tr.jxl',lambda s:s[:12]+bytes((s[12]^1,))+s[13:]),
    ]
    for rel,mutate in mutations:
        f=dest/rel;data=f.read_bytes();is_binary=rel.endswith('.jxl')
        source=data if is_binary else data.decode('utf-8')
        changed=mutate(source)
        if changed==source:raise SystemExit('mutation had no effect: '+rel)
        f.write_bytes(changed if is_binary else changed.encode('utf-8'))
        check(False)
        f.write_bytes(data)
    check()
print('PASS 4.0.0 snapshot and native JPEG XL: 8 negative mutations rejected; clean fixtures accepted')
