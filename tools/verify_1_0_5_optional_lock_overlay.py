from __future__ import annotations
from pathlib import Path
import argparse, json, sys

parser=argparse.ArgumentParser(description='Verify retained VulkanScope Database 1.0.5 stale optional npm-lock overlay hardening on the current release')
parser.add_argument('--root', default=None)
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]

def need(ok: bool, msg: str) -> None:
    if not ok: errors.append(msg)

def text(rel: str) -> str:
    p=root/rel
    return p.read_text(encoding='utf-8') if p.is_file() else ''

pkg=json.loads(text('worker/package.json'))
need(pkg.get('version')=='1.0.8','Worker package version must be 1.0.8')
need((pkg.get('devDependencies') or {}).get('wrangler')=='4.130.0','Wrangler must remain exactly pinned to 4.130.0')
need('worker/package-lock.json' in text('.gitignore'),'optional worker/package-lock.json must remain ignored')

repair=text('tools/repair_repository.py')
for token in ["optional_lock = root / 'worker' / 'package-lock.json'",'if optional_lock.is_file():','optional_lock.unlink()','ignored legacy worker/package-lock.json removed']:
    need(token in repair,f'repository repair missing stale-lock cleanup token: {token}')

lock_verifier=text('tools/verify_optional_npm_lock.py')
for token in ["pkg_path = root / 'worker' / 'package.json'","want = '4.130.0'",'canonical worker/package.json wrangler=', 'stale optional lock: run']:
    need(token in lock_verifier,f'optional-lock verifier missing fail-closed token: {token}')
need('^4.125.0' not in lock_verifier,'optional-lock verifier must not preserve the stale 4.125 range')

overlay=text('tools/test_existing_repo_overlay.py')
for token in ['real 1.0.4 failure','^4.125.0','stale optional lock','repository repair left ignored legacy worker/package-lock.json behind']:
    need(token in overlay,f'existing-repository overlay fixture missing stale-lock regression token: {token}')

workflow=text('tools/pages.workflow.yml')
need(text('.github/workflows/pages.yml')==workflow,'checked-in pages workflow differs from canonical template')
repair_token='python tools/repair_repository.py --apply'
lock_token='python tools/verify_optional_npm_lock.py'
need(repair_token in workflow and lock_token in workflow,'build workflow must contain repair and optional-lock verification steps')
if repair_token in workflow and lock_token in workflow:
    need(workflow.index(repair_token) < workflow.index(lock_token),'repository repair must run before optional-lock verification')
need('python tools/verify_1_0_5_optional_lock_overlay.py' in workflow,'retained 1.0.5 stale-lock hardening verifier missing from workflow')

packager=text('tools/package_release.py')
need("1.0.7_to_1.0.8_contract.json" in packager,'current release packager must use 1.0.7 -> 1.0.8 immutable contract')
need("paths.discard('worker/package-lock.json')" in packager,'release packager must continue excluding optional local lock')

rules=text('rules/PROJECT_RULES.md')
need('## Release 1.0.5 stale optional-lock overlay hardening requirements' in rules,'retained 1.0.5 rules section missing')
need('tracked-but-ignored' in rules and 'worker/package-lock.json' in rules,'retained 1.0.5 rules do not describe tracked-but-ignored lock failure class')

index=text('index.html'); app=text('assets/app.v1008.js')
need('VulkanScope Database <strong>1.0.8</strong>' in index,'1.0.8 footer identity missing')
need('app.v1008.js?v=1008' in index and 'config.js?v=1008' in index,'1.0.8 cache identity missing')
need('Database 1.0.8 · schema' in app,'frontend 1.0.8 identity missing')

if errors:
    print('FAIL retained VulkanScope Database 1.0.5 optional-lock overlay hardening on Database 1.0.8')
    for e in errors: print(' - '+e)
    raise SystemExit(1)
print('PASS Database 1.0.8 retains 1.0.5 stale tracked-but-ignored npm-lock repair semantics')
