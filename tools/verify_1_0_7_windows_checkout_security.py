#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, json

ap=argparse.ArgumentParser(description='Verify retained VulkanScope Database 1.0.7 Windows checkout/security-audit hardening on the current release')
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
need(pkg.get('version')=='1.0.8','current Worker package version must be 1.0.8')
need((pkg.get('devDependencies') or {}).get('wrangler')=='4.130.0','Wrangler must remain exactly 4.130.0')
need((pkg.get('overrides') or {}).get('sharp')=='0.35.4','sharp override must remain exactly 0.35.4')

attrs=text('.gitattributes')
need('* text=auto eol=lf' in attrs,'root .gitattributes must force canonical LF text checkouts')
for ext in ('*.png -text','*.ico -text','*.webp -text'):
    need(ext in attrs,f'.gitattributes binary exception missing: {ext}')
enc=(root/'assets/encyclopedia.v03924.js').read_bytes() if (root/'assets/encyclopedia.v03924.js').is_file() else b''
need(bool(enc) and b'\r' not in enc,'committed Encyclopedia fixture must be LF-only bytes')
state=text('tools/test_0809_floor_encyclopedia_state_machine.py')
need("if b'\\r' in expected" in state and 'checkout line-ending drift' in state,'Encyclopedia state-machine must diagnose checkout CRLF drift explicitly')
need('actual=out.read_bytes()' in state and 'generated={len(actual)} expected={len(expected)}' in state,'Encyclopedia state-machine byte-drift diagnostics missing')

sec=text('worker/scripts/security-audit.mjs')
need("const fromRun=process.env.npm_execpath" in sec,'security audit must resolve npm CLI from npm_execpath')
need("spawnSync(process.execPath,[cli,...args]" in sec,'security audit must launch npm-cli.js through current Node executable')
need("'npm.cmd'" not in sec and '"npm.cmd"' not in sec,'direct npm.cmd spawning is forbidden')
need('if(!fs.existsSync(lockPath))' in sec,'security audit should reuse an existing validated lock instead of recreating it unconditionally')
need("runNpm(['install','--package-lock-only','--ignore-scripts','--no-audit','--no-fund'])" in sec,'lock bootstrap command missing')
need("runNpm(['audit','--audit-level=high'])" in sec,'high-severity npm audit gate missing')

workflow=text('tools/pages.workflow.yml')
need(text('.github/workflows/pages.yml')==workflow,'checked-in workflow differs from canonical template')
need(workflow.count('uses: actions/setup-node@v7')>=2,'Windows and Linux build jobs must pin setup-node v7')
need(workflow.count('node-version: "24"')>=2,'Windows and Linux build jobs must pin Node 24')
need(workflow.count('package-manager-cache: false')>=2,'automatic npm caching must stay disabled for these no-lock source jobs')
need('name: Install audited Worker toolchain on Windows' in workflow and 'working-directory: worker\n        run: npm install' in workflow,'Windows CI must install the Worker dependency graph')
need('name: Exercise Windows security-audit subprocess path' in workflow and 'run: npm run security:audit' in workflow,'Windows CI must execute the real security-audit helper')
need(workflow.count('python tools/verify_1_0_7_windows_checkout_security.py')>=3,'1.0.7 verifier must gate Windows, build and release jobs')
need("node','tools/test_1_0_7_security_audit_runner.mjs" in text('tools/quality_gate.py'),'behavioral npm-cli runner state-machine must be part of quality gate')

index=text('index.html'); app=text('assets/app.v1008.js'); static=j('data/index.json')
need('VulkanScope Database <strong>1.0.8</strong>' in index,'current 1.0.8 footer identity missing')
need('app.v1008.js?v=1008' in index and 'site.v0390.css?v=1008' in index and 'config.js?v=1008' in index,'current 1.0.8 cache identity missing')
need('Database 1.0.8 · schema' in app,'current 1.0.8 frontend identity missing')
need(static.get('databaseVersion')=='1.0.8','static databaseVersion must be 1.0.8')
need(sorted(p.name for p in (root/'assets').glob('app.v*.js'))==['app.v1008.js'],'exactly one current versioned app asset must remain')

repair=text('tools/repair_repository.py')
need("CURRENT_APP = 'app.v1008.js'" in repair,'repository repair current app identity drifted')
pack=text('tools/package_release.py')
need('1.0.7_to_1.0.8_contract.json' in pack,'current release packager must use 1.0.7 -> 1.0.8 contract')
need('VulkanScope-Database-1.0.8.zip' in pack,'current release packager output identity drifted')
need("paths.discard('worker/package-lock.json')" in pack,'local audit lock must remain excluded from release package')

rules=text('rules/PROJECT_RULES.md')
need('## Release 1.0.7 Windows checkout / npm subprocess hardening requirements' in rules,'1.0.7 rules section missing')
need(sorted(x.name for x in (root/'worker/migrations').glob('*.sql'))==['0001_init.sql','0002_report_cursor_index.sql','0003_payload_chunks.sql'],'D1 migration set changed')

if errors:
    print('FAIL retained VulkanScope Database 1.0.7 Windows checkout/security-audit hardening on Database 1.0.8')
    for e in errors: print(' - '+e)
    raise SystemExit(1)
print('PASS retained VulkanScope Database 1.0.7 Windows checkout/security-audit hardening on Database 1.0.8')
