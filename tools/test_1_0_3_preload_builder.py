from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json, subprocess, sys, tempfile, threading

root=Path(__file__).resolve().parents[1]
ids=['a'*64,'b'*64]
index=[
 {'id':ids[0],'submitted_at':'2026-09-09T08:00:00Z','schema_version':2,'gpu_name':'GPU A','vendor_id':'0x1','device_id':'0x2','driver_mode':'System','driver_version':'1','device_api_version':'1.4.362','manufacturer':'A','model':'One'},
 {'id':ids[1],'submitted_at':'2026-09-09T07:00:00Z','schema_version':2,'gpu_name':'GPU B','vendor_id':'0x3','device_id':'0x4','driver_mode':'System','driver_version':'2','device_api_version':'1.4.362','manufacturer':'B','model':'Two'},
]
payloads={rid:{'schemaVersion':2,'id':rid,'submittedAt':index[i]['submitted_at'],'application':{'name':'VulkanScope','version':'1.0.15','versionCode':1015},'device':{'manufacturer':index[i]['manufacturer'],'model':index[i]['model']},'gpu':{'name':index[i]['gpu_name']},'driver':{'mode':'System','version':str(i+1)},'vulkan':{'deviceApiVersion':'1.4.362'},'technicalReport':{'schemaVersion':3}} for i,rid in enumerate(ids)}

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def do_GET(self):
        if self.path.startswith('/v1/reports?'):
            body={'schemaVersion':2,'normalizerVersion':16,'publishedVulkanSpec':'Vulkan 1.4.362 (2026-09-04)','vulkanRegistryBaseline':'VulkanScope producer/query baseline 1.4.362','producerQueryBaseline':'VulkanScope 1.0.15 · Vulkan 1.4.362','compatibleProducer':'VulkanScope 0.80.3+ · schema 2 / technical report 3','reports':index,'nextCursor':None}
        elif self.path.startswith('/v1/reports/'):
            rid=self.path.split('/')[3].split('?')[0]
            body=payloads.get(rid)
            if body is None: self.send_error(404); return
        else: self.send_error(404); return
        raw=json.dumps(body,separators=(',',':')).encode()
        self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)

server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
try:
    with tempfile.TemporaryDirectory(prefix='vulkanscope-preload-test-') as td:
        out=Path(td)/'preload'
        cmd=[sys.executable,str(root/'tools/build_preload_snapshot.py'),str(out),'--api',f'http://127.0.0.1:{server.server_port}','--workers','2']
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode: raise SystemExit(r.stdout+r.stderr)
        manifest=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
        assert manifest['databaseVersion']=='1.0.3'
        assert manifest['reportCount']==2
        assert [x['id'] for x in manifest['reports']]==ids
        found=[]
        for item in manifest['chunks']:
            assert item['file'].startswith('reports.') and item['file'].endswith('.json')
            chunk=json.loads((out/item['file']).read_text(encoding='utf-8'))
            found.extend(x['id'] for x in chunk['reports'])
        assert found==ids
        print('PASS 1.0.3 preload builder: paged index -> bounded static chunk snapshot')
finally:
    server.shutdown(); server.server_close()
