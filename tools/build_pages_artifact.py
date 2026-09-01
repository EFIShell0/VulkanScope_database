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
asset_files=[
    'assets/app.v03917.js',
    'assets/site.v0390.css',
    'assets/apple-touch-icon-v0311.png',
    'assets/favicon-v0311.ico','assets/favicon-v0311.png',
    'assets/favicon.ico','assets/favicon.png',
    'assets/vulkanscope_logo_horizontal.png',
    'assets/gpu-vendors/gpu_vendor_amd.png',
    'assets/gpu-vendors/gpu_vendor_arm.png',
    'assets/gpu-vendors/gpu_vendor_broadcom.png',
    'assets/gpu-vendors/gpu_vendor_huawei.png',
    'assets/gpu-vendors/gpu_vendor_imagination.png',
    'assets/gpu-vendors/gpu_vendor_intel.png',
    'assets/gpu-vendors/gpu_vendor_nvidia.png',
    'assets/gpu-vendors/gpu_vendor_qualcomm.png',
    'assets/gpu-vendors/gpu_vendor_samsung.png',
    'assets/gpu-vendors/gpu_vendor_unknown.png',
    'assets/gpu-vendors/gpu_vendor_vivante.png',
    'assets/gpu-vendors/gpu_vendor_vsi.png',
    'assets/hdr/dolby_vision.png','assets/hdr/dolby_vision_2.png',
    'assets/hdr/hdr10.svg','assets/hdr/hdr10_plus.png',
    'assets/hdr/hdr10_plus_advanced.png','assets/hdr/hdr_vivid.webp',
]
for name in public_files + asset_files:
    src=root/name
    if not src.is_file(): raise SystemExit(f'missing required public file: {name}')
    out=dest/name
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
