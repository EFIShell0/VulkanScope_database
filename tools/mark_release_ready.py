from pathlib import Path
import argparse, json, sys

parser=argparse.ArgumentParser(description="Mark only a staged VulkanScope Database Pages artifact as release-ready")
parser.add_argument('artifact', nargs='?', default='_site')
args=parser.parse_args()
root=Path(args.artifact).resolve()
marker=root/'data'/'release.json'
if not marker.is_file(): raise SystemExit(f'missing staged release marker: {marker}')
data=json.loads(marker.read_text(encoding='utf-8'))
expected={'schemaVersion':2,'databaseVersion':'1.0.20','releaseReady':False,'appAsset':'assets/app.v1020.js','cacheKey':'1020'}
if data!=expected: raise SystemExit(f'unexpected source/staged release marker before ready transition: {data!r}')
data['releaseReady']=True
marker.write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
print(f'Marked staged VulkanScope Database 1.0.20 artifact release-ready: {marker}')
