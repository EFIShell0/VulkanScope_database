from __future__ import annotations
import argparse, hashlib, json, time, urllib.parse, urllib.request

p=argparse.ArgumentParser(description='Verify live GitHub Pages snapshot identity and all content-addressed chunks')
p.add_argument('--base-url', required=True)
p.add_argument('--report-id', default='')
p.add_argument('--attempts', type=int, default=12)
p.add_argument('--delay', type=float, default=3.0)
a=p.parse_args()
base=a.base_url.rstrip('/')+'/'
if urllib.parse.urlparse(base).scheme!='https': raise SystemExit('HTTPS Pages URL required')
rid=a.report_id.strip().lower()
if rid and (len(rid)!=64 or any(c not in '0123456789abcdef' for c in rid)):
    raise SystemExit('invalid --report-id')

def get(path,limit):
    url=urllib.parse.urljoin(base,path)
    if not url.startswith(base):raise RuntimeError('snapshot path escapes Pages base URL')
    url+='?verify='+str(time.time_ns())
    req=urllib.request.Request(url,headers={'Accept':'application/json','Cache-Control':'no-cache','User-Agent':'VulkanScope-Database-snapshot-verifier/4.0.0'})
    with urllib.request.urlopen(req,timeout=25) as response:
        raw=response.read(limit+1)
        if len(raw)>limit:raise RuntimeError('response exceeds configured bound: '+path)
        return raw

def verify():
    raw=get('data/preload/manifest.json',8*1024*1024)
    manifest=json.loads(raw.decode('utf-8'))
    if manifest.get('databaseVersion')!='4.0.0':raise RuntimeError('wrong Database release version')
    reports=manifest.get('reports'); chunks=manifest.get('chunks')
    if not isinstance(reports,list) or not isinstance(chunks,list):raise RuntimeError('invalid manifest arrays')
    if manifest.get('reportCount')!=len(reports):raise RuntimeError('manifest reportCount mismatch')
    ids=[str(x.get('id','')) for x in reports if isinstance(x,dict)]
    if len(ids)!=len(reports) or len(set(ids))!=len(ids):raise RuntimeError('duplicate/invalid report identities')
    if rid and rid not in ids:raise RuntimeError('trigger report absent from manifest')
    seen=set();covered=set();total=0
    for chunk in chunks:
        name=chunk.get('file')
        if not isinstance(name,str) or not name.startswith('reports.') or not name.endswith('.json') or '/' in name or name in seen:raise RuntimeError('invalid/duplicate chunk name')
        seen.add(name)
        body=get('data/preload/'+name,20*1024*1024)
        total+=len(body)
        if total>256*1024*1024:raise RuntimeError('total snapshot exceeds verification bound')
        if hashlib.sha256(body).hexdigest()!=chunk.get('sha256') or len(body)!=chunk.get('byteLength'):raise RuntimeError('chunk SHA-256/byteLength mismatch: '+name)
        chunk_data=json.loads(body.decode('utf-8'))
        chunk_reports=chunk_data.get('reports')
        if not isinstance(chunk_reports,list) or len(chunk_reports)!=chunk.get('reportCount'):raise RuntimeError('chunk report count mismatch')
        for row in chunk_reports:
            ident=str(row.get('id','')) if isinstance(row,dict) else ''
            if ident not in ids or ident in covered:raise RuntimeError('unexpected/duplicate report in chunk')
            covered.add(ident)
    if covered!=set(ids):raise RuntimeError('chunk coverage does not equal manifest report ids')
    print(f'PASS published snapshot database=4.0.0 reports={len(reports)} chunks={len(chunks)} expected={rid or "none"}')

last=None
for attempt in range(max(1,min(30,a.attempts))):
    try:verify();raise SystemExit(0)
    except SystemExit:raise
    except Exception as exc:
        last=exc
        if attempt+1<max(1,min(30,a.attempts)):time.sleep(max(.5,min(10.,a.delay)))
raise SystemExit(f'published snapshot verification failed: {last}')
