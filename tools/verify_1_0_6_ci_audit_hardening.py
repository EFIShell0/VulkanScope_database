#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, json

ap=argparse.ArgumentParser(description='Verify retained VulkanScope Database 1.0.6 CI/audit/Encyclopedia hardening')
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
need(pkg.get('version')=='1.0.7','current Worker package version must be 1.0.7')
need((pkg.get('devDependencies') or {}).get('wrangler')=='4.130.0','Wrangler must remain exactly 4.130.0')
need((pkg.get('overrides') or {}).get('sharp')=='0.35.4','sharp security override must remain exactly 0.35.4')
allow=pkg.get('allowScripts') or {}
need(all(allow.get(x) is True for x in ('esbuild','sharp','workerd')),'reviewed install-script allow-list drifted')
need((pkg.get('scripts') or {}).get('security:audit')=='node scripts/security-audit.mjs','security:audit must use the lock-backed audit helper')
need((pkg.get('scripts') or {}).get('predeploy')=='npm run verify:account && npm run security:audit','predeploy order/account+audit gate drifted')

sec=text('worker/scripts/security-audit.mjs')
for token in [
    "const wantWrangler='4.130.0'",
    "const wantSharp='0.35.4'",
    "'--package-lock-only'",
    "'--ignore-scripts'",
    "'--no-audit'",
    "'--no-fund'",
    "runNpm(['audit','--audit-level=high'])",
    "packages['node_modules/wrangler']",
    "packages['node_modules/sharp']",
]:
    need(token in sec,f'retained security-audit helper missing token: {token}')

lockv=text('tools/verify_optional_npm_lock.py')
need("want = '4.130.0'" in lockv and "want_sharp = '0.35.4'" in lockv,'optional-lock verifier pins drifted')
need("packages.get('node_modules/sharp')" in lockv and 'resolved sharp package missing integrity hash' in lockv,'optional-lock verifier does not validate patched sharp lock resolution')

encgen=text('tools/generate_encyclopedia_03924.py')
need("write_bytes(('window.VULKANSCOPE_ENCYCLOPEDIA='+payload+';\\n').encode('utf-8'))" in encgen,'Encyclopedia generator must retain explicit UTF-8 bytes/LF')
need("Path(args.output).write_text('window.VULKANSCOPE_ENCYCLOPEDIA='" not in encgen,'platform-newline-translating Encyclopedia write_text path remains')

workflow=text('tools/pages.workflow.yml')
need(text('.github/workflows/pages.yml')==workflow,'checked-in workflow differs from canonical template')
need('run: python tools/test_0809_floor_encyclopedia_state_machine.py' in workflow,'Windows CI must retain Encyclopedia regeneration state machine')
need('python tools/verify_1_0_2_producer_baseline.py --skip-version' in workflow,'historical 1.0.2 verifier must run with --skip-version')
need('python tools/verify_1_0_2_producer_baseline.py\n' not in workflow,'bare current-identity 1.0.2 verifier invocation remains in workflow')
need(workflow.count('python tools/verify_1_0_6_ci_audit_hardening.py')>=2,'retained 1.0.6 hardening verifier must gate Windows/build jobs')

alias=text('tools/verify_1_0_5_stale_lock_repair.py')
need('verify_1_0_5_optional_lock_overlay.py' in alias,'documented 1.0.5 verifier compatibility wrapper missing')

index=text('index.html'); app=text('assets/app.v1007.js'); static=j('data/index.json')
need('VulkanScope Database <strong>1.0.7</strong>' in index,'current 1.0.7 browser footer identity missing')
need('app.v1007.js?v=1007' in index and 'site.v0390.css?v=1007' in index and 'config.js?v=1007' in index,'current 1.0.7 cache identity missing')
need('Database 1.0.7 · schema' in app,'current 1.0.7 frontend identity missing')
need(static.get('databaseVersion')=='1.0.7','static databaseVersion must be 1.0.7')
need(sorted(p.name for p in (root/'assets').glob('app.v*.js'))==['app.v1007.js'],'exactly one current versioned app asset must remain')

rules=text('rules/PROJECT_RULES.md')
need('## Release 1.0.6 CI / deterministic Encyclopedia / npm-audit hardening requirements' in rules,'historical 1.0.6 rules section missing')
need('a91af4ad277936683ef1eb01802fd201934217b78a9dc808d58575aa7c6cc00e' in rules,'1.0.5 predecessor hash missing from historical 1.0.6 rules')

need(sorted(x.name for x in (root/'worker/migrations').glob('*.sql'))==['0001_init.sql','0002_report_cursor_index.sql','0003_payload_chunks.sql'],'D1 migration set changed')

if errors:
    print('FAIL retained VulkanScope Database 1.0.6 CI/audit hardening')
    for e in errors: print(' - '+e)
    raise SystemExit(1)
print('PASS retained VulkanScope Database 1.0.6 CI/audit hardening on Database 1.0.7')
