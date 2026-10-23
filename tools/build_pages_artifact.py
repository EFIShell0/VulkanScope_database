from pathlib import Path
import shutil, sys, json

root=Path(__file__).resolve().parents[1]
dest=Path(sys.argv[1]) if len(sys.argv)>1 else root/'_site'
if not dest.is_absolute(): dest=root/dest
dest=dest.resolve()
if dest==root:
    raise SystemExit('refusing to stage Pages artifact over repository root')
if dest.exists(): shutil.rmtree(dest)
dest.mkdir(parents=True)

public_files=[
    '.nojekyll','index.html','config.js','report.schema.json',
    '400.html','401.html','403.html','404.html','405.html','408.html','409.html',
    '413.html','415.html','429.html','500.html','502.html','503.html','504.html','error.html','jxl-unsupported.html',
]
asset_files=[
    'assets/app.v1413.js','assets/browser-compat.v1413.js','assets/release-bootstrap.v1413.js',
    'assets/app.v4000.js','assets/browser-compat.v4000.js','assets/release-bootstrap.v4000.js','assets/encyclopedia.v4000.js',
    'assets/site.v0390.css','assets/site.v1308.css','assets/site.v1309.css','assets/site.v1400.css','assets/site.v1401.css','assets/site.v1402.css','assets/site.v1403.css','assets/site.v1404.css','assets/site.v1405.css','assets/site.v1406.css','assets/site.v1407.css','assets/site.v1408.css','assets/site.v1409.css','assets/site.v1410.css','assets/site.v1411.css','assets/site.v1412.css','assets/site.v1413.css','assets/site.v4000.css',
    'assets/jxl-probe.v4000.jxl',
]
# Checked-in inventory is the sole source of deployable JPEG XL assets.
inventory=json.loads((root/'tools/jxl_asset_manifest.json').read_text(encoding='utf-8'))
if inventory.get('assetCount') != len(inventory.get('assets',[])): raise SystemExit('JPEG XL inventory count mismatch')
asset_files += [r['to'] for r in inventory['assets']]
for name in public_files + asset_files:
    src=root/name
    if not src.is_file(): raise SystemExit(f'missing required public file: {name}')
    out=dest/name
    out.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,out)

license_files=['wrangler.md','sharp.md','esbuild.md','workerd.md','nodejs.md','python.md','browser-marks.md']
for name in license_files:
    src=root/'licenses'/name
    if not src.is_file(): raise SystemExit(f'missing required public license file: licenses/{name}')
    out=dest/'licenses'/name
    out.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,out)

flag_dir=root/'assets/country-flags'
flag_files=sorted(flag_dir.glob('*.jxl')) if flag_dir.is_dir() else []
if len(flag_files)!=250: raise SystemExit(f'expected 250 bundled JPEG XL country flags, found {len(flag_files)}')
for src in flag_files:
    out=dest/'assets/country-flags'/src.name
    out.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,out)

# data is generated/public JSON only; copy JSON files, not arbitrary leftovers.
data_src=root/'data'
if not data_src.is_dir(): raise SystemExit('missing required public directory: data')
for src in sorted(data_src.rglob('*.json')):
    if not src.is_file(): continue
    rel=src.relative_to(root)
    out=dest/rel
    out.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,out)
print(f'Staged VulkanScope Database Pages artifact: {dest}')
