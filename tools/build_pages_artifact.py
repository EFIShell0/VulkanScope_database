from pathlib import Path
import shutil, sys

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
    '413.html','415.html','429.html','500.html','502.html','503.html','504.html','error.html',
]
for name in public_files:
    src=root/name
    if not src.is_file(): raise SystemExit(f'missing required public file: {name}')
    shutil.copy2(src,dest/name)
for name in ['assets','data']:
    src=root/name
    if not src.is_dir(): raise SystemExit(f'missing required public directory: {name}')
    shutil.copytree(src,dest/name)
print(f'Staged VulkanScope Database Pages artifact: {dest}')
