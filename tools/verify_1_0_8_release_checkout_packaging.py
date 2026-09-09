#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, json

ap=argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.8 tagged-checkout/release-package boundary hardening')
ap.add_argument('--root', default=None)
a=ap.parse_args()
root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
errors=[]

def need(ok,msg):
    if not ok: errors.append(msg)

def text(rel):
    p=root/rel
    return p.read_text(encoding='utf-8') if p.is_file() else ''

def j(rel):
    try:return json.loads(text(rel))
    except:return {}

pkg=j('worker/package.json')
need(pkg.get('version')=='1.0.8','Worker package version must be 1.0.8')
need((pkg.get('devDependencies') or {}).get('wrangler')=='4.130.0','Wrangler must remain exactly 4.130.0')
need((pkg.get('overrides') or {}).get('sharp')=='0.35.4','sharp override must remain exactly 0.35.4')

workflow=text('tools/pages.workflow.yml')
need(text('.github/workflows/pages.yml')==workflow,'checked-in workflow differs from canonical template')
need('name: Repair and verify tagged source' in workflow,'tagged-source release verification step missing')
need('python tools/verify_regression_contract.py --strict-tree' not in workflow,
     'tagged Git checkout must not be strict-tree verified before package construction')
need('python tools/verify_regression_contract.py\n' in workflow,
     'tagged Git checkout must retain source-overlay predecessor verification')
need('python tools/package_release.py dist' in workflow,'deterministic release packager step missing')
need(workflow.count('python tools/verify_1_0_8_release_checkout_packaging.py')>=2,
     '1.0.8 release-boundary verifier must gate build/release jobs')

pack=text('tools/package_release.py')
need("1.0.7_to_1.0.8_contract.json" in pack,'packager must use 1.0.7 -> 1.0.8 immutable contract')
need("VulkanScope-Database-1.0.8.zip" in pack,'packager output identity drifted')
need("subprocess.run([sys.executable, str(root/'tools/verify_regression_contract.py')]" in pack,
     'packager must source-overlay verify the history-bearing checkout')
need("str(extracted/'tools/verify_regression_contract.py'), '--strict-tree'" in pack,
     'packager must strict-tree verify a clean extracted release')
need("if (extracted/rel).read_bytes() != (root/rel).read_bytes()" in pack,
     'packager must compare clean-extract bytes to selected source bytes')
need("paths.discard('worker/package-lock.json')" in pack,'optional local audit lock must remain excluded')
need("parser.add_argument('--root'" in pack,'packager fixture/root override missing')
need("zi = zipfile.ZipInfo(rel, (1980, 1, 1, 0, 0, 0))" in pack,'fixed deterministic ZIP timestamp missing')

reg=text('tools/verify_regression_contract.py')
need("1.0.7_to_1.0.8_contract.json" in reg,'regression verifier must use current contract')
need("'databaseVersion': '1.0.8'" in reg,'generated index validator must require Database 1.0.8')
need("if args.strict_tree:" in reg,'strict-package mode must remain explicit and fail-closed')

test=text('tools/test_1_0_8_release_checkout_packaging.py')
for token in [
    "assets/site.v0380.css",
    "assets/site.v0357.css",
    "assets/app.js",
    "verify_regression_contract.py",
    "--strict-tree",
    "package_release.py",
]:
    need(token in test,f'release-boundary regression fixture missing token: {token}')

index=text('index.html'); app=text('assets/app.v1008.js'); static=j('data/index.json')
need('VulkanScope Database <strong>1.0.8</strong>' in index,'1.0.8 footer identity missing')
need('app.v1008.js?v=1008' in index and 'site.v0390.css?v=1008' in index and 'config.js?v=1008' in index,'1.0.8 cache identity missing')
need('Database 1.0.8 · schema' in app,'1.0.8 frontend identity missing')
need(static.get('databaseVersion')=='1.0.8','static databaseVersion must be 1.0.8')
need(sorted(p.name for p in (root/'assets').glob('app.v*.js'))==['app.v1008.js'],
     'canonical package source must contain exactly the current versioned app asset')

rules=text('rules/PROJECT_RULES.md')
need('## Release 1.0.8 tagged-checkout / strict-package boundary requirements' in rules,'1.0.8 rules section missing')
need((root/'rules/1.0.8_TAGGED_CHECKOUT_RELEASE_BOUNDARY_AUDIT.md').is_file(),'1.0.8 release-boundary audit document missing')
need('414da835326c3414215d598c8cf12b8391bfa112a5f02eff4031a788bfdf1b67' in rules,'1.0.7 predecessor hash missing')
need(sorted(x.name for x in (root/'worker/migrations').glob('*.sql'))==['0001_init.sql','0002_report_cursor_index.sql','0003_payload_chunks.sql'],'D1 migration set changed')

if errors:
    print('FAIL VulkanScope Database 1.0.8 tagged-checkout/release-package boundary hardening')
    for e in errors: print(' - '+e)
    raise SystemExit(1)
print('PASS VulkanScope Database 1.0.8 tagged-checkout/release-package boundary hardening')
