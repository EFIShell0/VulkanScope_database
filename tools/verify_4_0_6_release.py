#!/usr/bin/env python3
"""Assert strict app/Worker/Pages compatibility of the current 4.0.6 release."""
from pathlib import Path
import hashlib, json, subprocess, sys
R=Path(__file__).resolve().parents[1]
failures=[]
def require(cond,msg):
    if not cond:failures.append(msg)
def read(path):return (R/path).read_text(encoding='utf-8')
worker=read('worker/src/index.js')
require("const supportedProducer=p=>p?.application?.version==='4.0.15'&&p?.application?.versionCode===4015" in worker,'strict POST producer check missing')
require('if(v.major===4)return p.application.versionCode===4000+v.minor*100+v.patch' in worker,'4.x producer identity mapping missing')
require("manifest?.databaseVersion==='4.0.6'" in worker,'snapshot publication comparison uses old version')
require("Only VulkanScope 4.0.15 (versionCode 4015) may submit new reports" in worker,'correct rejection error missing')
require('await env.DB.batch(statements)' in worker,'database write path missing')
require('databaseReleaseVersion:\'4.0.6\'' in worker,'Worker release identity mismatch')
release=json.loads(read('data/release.json'))
require(release=={'schemaVersion':2,'databaseVersion':'4.0.6','releaseReady':False,'appAsset':'assets/app.v4006.js','cacheKey':'4006'},'source release marker not 4.0.6')
meta=json.loads(read('data/index.json'))
require(meta.get('producerQueryBaseline')=='VulkanScope 4.0.15 · Vulkan 1.4.366','frontend producer metadata mismatch')
schema=json.loads(read('report.schema.json'))['properties']['application']['properties']
require(schema['version'].get('pattern')==r'^4\.0\.15$' and schema['version'].get('const')=='4.0.15','schema exact version restriction missing')
require(schema['versionCode'].get('const')==4015,'schema exact versionCode restriction missing')
lock=json.loads(read('registry/registry_lock.json'))
require(lock['snapshotSha256']==hashlib.sha256((R/'registry/upstream/vk.xml').read_bytes()).hexdigest(),'registry hash mismatch')
require(lock['apiBaseline']=='Vulkan 1.4.366' and lock['registeredVulkanExtensionCount']==479,'registry version/census mismatch')
require('"appVersion":"4.0.15"' in read('assets/encyclopedia.v4006.js'),'encyclopedia producer version mismatch')
require('const DATABASE_VERSION=\'4.0.6\'' in read('assets/app.v4006.js'),'frontend release version mismatch')
require('assets/app.v4006.js?v=4006' in read('index.html'),'index stale asset')
for name in ['app','browser-compat','release-bootstrap']:
    require((R/f'assets/{name}.v4006.js').is_file(),'missing current JS '+name)
    require((R/f'assets/{name}.v4005.js').is_file(),'missing predecessor bridge '+name)
    require(not (R/f'assets/{name}.v4004.js').exists(),'stale bridge still shipped '+name)
require(read('.github/workflows/pages.yml')==read('tools/pages.workflow.yml'),'release workflow not canonical')
require('python tools/quality_gate.py' in read('tools/pages.workflow.yml'),'CI quality gate missing')
require('4.0.6' in read('rules/PROJECT_RULES.md'),'rules version not updated')
if failures:
    print('\n'.join('FAIL '+s for s in failures));sys.exit(1)
print('PASS VulkanScope Database 4.0.6 release source lock: only 4.0.15 / 4015 new submissions')
