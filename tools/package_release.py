#!/usr/bin/env python3
"""Deterministic archive; excludes Git, local credentials and generated caches."""
from pathlib import Path
import hashlib, sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'dist'
OUT.mkdir(parents=True,exist_ok=True)
FORBIDDEN={'.git','node_modules','.wrangler','.gradle','_site','dist','build','__pycache__','.pytest_cache','tmp','temp'}
filenames=[]
for file in ROOT.rglob('*'):
    if not file.is_file() or file.is_symlink():continue
    rel=file.relative_to(ROOT)
    if any(x in FORBIDDEN for x in rel.parts):continue
    if file.name in {'.env','.dev.vars','worker/package-lock.json'} or file.name.startswith(('.env.','.dev.vars.')):continue
    if file.suffix.lower() in {'.pyc','.pyo','.tmp','.log','.apk','.so','.class','.zip'}:continue
    filenames.append(rel)
filenames.sort(key=lambda x:x.as_posix())
zipname='VulkanScope-Database-4.0.6.zip'
pkg=OUT/zipname
with zipfile.ZipFile(pkg,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,allowZip64=True) as z:
    for rel in filenames:
        info=zipfile.ZipInfo(rel.as_posix(),date_time=(2026,10,24,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=(0o644<<16)
        z.writestr(info,(ROOT/rel).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
sha=hashlib.sha256(pkg.read_bytes()).hexdigest()
(OUT/(zipname+'.sha256')).write_text(sha+'  '+zipname+'\n',encoding='ascii')
print(f'CREATED {pkg.name} size={pkg.stat().st_size} sha256={sha}')
