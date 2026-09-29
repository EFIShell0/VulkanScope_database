from __future__ import annotations
import argparse, json, time, urllib.parse, urllib.request

p=argparse.ArgumentParser(description='Verify that the deployed Pages preload snapshot contains an expected report')
p.add_argument('--base-url', required=True)
p.add_argument('--report-id', default='')
p.add_argument('--attempts', type=int, default=12)
p.add_argument('--delay', type=float, default=3.0)
a=p.parse_args()
base=a.base_url.rstrip('/')+'/'
rid=a.report_id.strip().lower()
if rid and (len(rid)!=64 or any(c not in '0123456789abcdef' for c in rid)):
    raise SystemExit('invalid --report-id')
last=None
for attempt in range(max(1,min(30,a.attempts))):
    try:
        url=urllib.parse.urljoin(base,'data/preload/manifest.json')+f'?verify={time.time_ns()}'
        req=urllib.request.Request(url,headers={'Accept':'application/json','Cache-Control':'no-cache','User-Agent':'VulkanScope-Database-snapshot-verifier/1.4.12'})
        with urllib.request.urlopen(req,timeout=20) as response:
            raw=response.read(4*1024*1024+1)
            if len(raw)>4*1024*1024: raise RuntimeError('manifest response exceeds 4 MiB')
        data=json.loads(raw.decode('utf-8'))
        if data.get('databaseVersion')!='1.4.12': raise RuntimeError(f"databaseVersion={data.get('databaseVersion')!r}")
        reports=data.get('reports')
        if not isinstance(reports,list): raise RuntimeError('manifest reports is not an array')
        ids={str(x.get('id','')) for x in reports if isinstance(x,dict)}
        if rid and rid not in ids: raise RuntimeError(f'expected report {rid} is not in deployed snapshot')
        print(f'PASS published snapshot database=1.4.12 reports={len(reports)} expected={rid or "none"}')
        raise SystemExit(0)
    except SystemExit: raise
    except Exception as exc:
        last=exc
        if attempt+1<max(1,min(30,a.attempts)): time.sleep(max(.5,min(10.0,a.delay)))
raise SystemExit(f'published snapshot verification failed: {last}')
