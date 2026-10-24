#!/usr/bin/env python3
"""VulkanScope Database 4.0.6 source/Pages audit; never mutates user data."""
from pathlib import Path
import argparse, json, re, subprocess, sys, sqlite3, xml.etree.ElementTree as ET, hashlib
from urllib.parse import urlsplit
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--source-tree',type=Path);p.add_argument('--artifact-tree',type=Path);p.add_argument('--require-release-ready',action='store_true');p.add_argument('--version',action='store_true');a=p.parse_args()
if a.version: print('VulkanScope Database audit 4.0.6');raise SystemExit(0)
errors=[]
def need(expr, msg):
    if not expr: errors.append(msg)
def read(base, rel):
    try:return (base/rel).read_text(encoding='utf-8')
    except (OSError, UnicodeError) as e:errors.append(f'missing/unreadable {rel}: {e}');return ''

def validate_pages(root,ready=False):
    root=root.resolve()
    marker=json.loads(read(root,'data/release.json') or '{}')
    expected={'schemaVersion':2,'databaseVersion':'4.0.6','appAsset':'assets/app.v4006.js','cacheKey':'4006','releaseReady':bool(ready)}
    for k,v in expected.items():need(marker.get(k)==v,f'Pages release marker {k} mismatch')
    index=read(root,'index.html')
    for token in ['assets/app.v4006.js?v=4006','browser-compat.v4006.js?v=4006','site.v4006.css?v=4006','VulkanScope Database <strong>4.0.6</strong>']:
        need(token in index,f'Pages current asset or identity missing {token}')
    top={'.nojekyll','index.html','config.js','report.schema.json','assets','data','licenses','400.html','401.html','403.html','404.html','405.html','408.html','409.html','413.html','415.html','429.html','500.html','502.html','503.html','504.html','error.html','jxl-unsupported.html'}
    need(set(x.name for x in root.iterdir())==top,'Pages must contain only the documented static allow-list')
    for f in root.rglob('*'):
        rel=f.relative_to(root)
        need(not f.is_symlink(),f'Pages symlink forbidden {rel}')
        need(not any(x in {'.git','worker','tools','rules','regression','registry','node_modules','.wrangler'} for x in rel.parts),f'private source leaked to Pages {rel}')
        if f.is_file() and rel.parts[0]=='data':need(f.suffix=='.json',f'non-JSON Pages data {rel}')
    for html in root.glob('*.html'):
        for url in re.findall(r'''(?:href|src)=["']([^"']+)["']''',read(root,html.name),re.I):
            if url.startswith(('https://','http://','data:','#','mailto:','javascript:')):continue
            u=urlsplit(url).path
            if not u or u=='/' or u=='./' or u.endswith('/'):continue
            file=(root/(u.removeprefix('/VulkanScope_database/') if u.startswith('/VulkanScope_database/') else u)).resolve()
            need(file.is_relative_to(root) and file.is_file(),f'broken Pages local asset {html.name}: {u}')


def validate_source(root):
    require=['index.html','data/index.json','data/release.json','report.schema.json','assets/app.v4006.js','assets/browser-compat.v4006.js','assets/release-bootstrap.v4006.js','assets/site.v4006.css','assets/encyclopedia.v4006.js','worker/src/index.js','worker/tests/contract.mjs','worker/wrangler.jsonc','rules/PROJECT_RULES.md','registry/upstream/vk.xml','registry/registry_lock.json','.github/workflows/pages.yml','tools/pages.workflow.yml']
    for f in require:need((root/f).is_file(),f'source missing {f}')
    meta=json.loads(read(root,'data/index.json') or '{}')
    mark=json.loads(read(root,'data/release.json') or '{}')
    schema=json.loads(read(root,'report.schema.json') or '{}')
    lock=json.loads(read(root,'registry/registry_lock.json') or '{}')
    worker=read(root,'worker/src/index.js')
    frontend=read(root,'assets/app.v4006.js')
    for k,v in {'databaseVersion':'4.0.6','publishedVulkanSpec':'Vulkan 1.4.366','producerQueryBaseline':'VulkanScope 4.0.15 · Vulkan 1.4.366','compatibleProducer':'VulkanScope 4.0.15 only · schema 2 / technical report 3'}.items():
        need(meta.get(k)==v,f'data/index.json {k} mismatch')
    need(mark.get('databaseVersion')=='4.0.6' and mark.get('appAsset')=='assets/app.v4006.js','release marker mismatch')
    need("const DATABASE_VERSION='4.0.6'" in frontend,'frontend version mismatch')
    need("const supportedProducer=p=>p?.application?.version==='4.0.15'&&p?.application?.versionCode===4015" in worker,'Worker exact-only producer enforcement missing')
    need("if(v.major===4)return p.application.versionCode===4000+v.minor*100+v.patch" in worker,'4.x versionCode mapping missing')
    need('Only VulkanScope 4.0.15 (versionCode 4015) may submit new reports' in worker,'specific client rejection missing')
    need('manifest?.databaseVersion===\'4.0.6\'' in worker,'snapshot reconciliation old-version check')
    prop=schema.get('properties',{}).get('application',{}).get('properties',{})
    need(prop.get('version',{}).get('const')=='4.0.15' and prop.get('versionCode',{}).get('const')==4015,'schema producer version allow-list mismatch')
    need(prop.get('version',{}).get('pattern')==r'^4\.0\.15$','schema pattern does not accept the current producer')
    need(lock.get('apiVersion')=='1.4.366' and lock.get('headerVersion')==366 and lock.get('registeredVulkanExtensionCount')==479,'registry lock outdated')
    registry=(root/'registry/upstream/vk.xml').read_bytes()
    need(hashlib.sha256(registry).hexdigest()==lock.get('registrySha256'),'registry SHA lock mismatch')
    enc=read(root,'assets/encyclopedia.v4006.js')
    need('"appVersion":"4.0.15"' in enc and '"registryBaseline":"Vulkan 1.4.366"' in enc,'encyclopedia generated data outdated')
    need('"extensions":479' in enc and '"tokens":6274' in enc,'encyclopedia census outdated')
    need(read(root,'.github/workflows/pages.yml')==read(root,'tools/pages.workflow.yml'),'workflow source drift')
    need("'assets/app.v4006.js'" in read(root,'tools/build_pages_artifact.py'),'Pages builder not pinned to the new release')
    need("CURRENT_APP = 'app.v4006.js'" in read(root,'tools/repair_repository.py'),'repository repair could delete current app')
    need('## 4.0.6 submission acceptance rule' in read(root,'rules/PROJECT_RULES.md'),'rule section missing')
    need("default-src 'self'" in read(root,'index.html') and 'connect-src' in read(root,'index.html'),'CSP missing')
    for token in ('readBoundedBody','hasSensitiveKey','2*1024*1024','stableStringify'):
        need(token in worker,f'Worker safety primitive missing {token}')
    pkg=json.loads(read(root,'worker/package.json') or '{}')
    need(pkg.get('version')=='4.0.6' and pkg.get('devDependencies',{}).get('wrangler')=='4.152.0','Worker package pins mismatch')
    try:
        con=sqlite3.connect(':memory:')
        for f in sorted((root/'worker/migrations').glob('*.sql')):con.executescript(f.read_text(encoding='utf-8'))
        need(con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='report_payload_chunks'").fetchone() is not None,'D1 migration chain incomplete')
    except Exception as exc:errors.append(f'D1 migrations invalid: {exc}')
    for f in ['assets/app.v4006.js','assets/browser-compat.v4006.js','assets/release-bootstrap.v4006.js','assets/encyclopedia.v4006.js','worker/src/index.js','worker/tests/contract.mjs']:
        test=subprocess.run(['node','--check',str(root/f)],capture_output=True,text=True)
        need(test.returncode==0,f'JS syntax error {f}: {test.stderr[:180]}')

root=(a.artifact_tree or a.source_tree or R).resolve()
if a.artifact_tree:validate_pages(root,a.require_release_ready)
else:validate_source(root)
if errors:
    print('\n'.join('FAIL '+e for e in errors));raise SystemExit(1)
print('PASS VulkanScope Database 4.0.6 '+('Pages artifact' if a.artifact_tree else 'source')+' audit')
