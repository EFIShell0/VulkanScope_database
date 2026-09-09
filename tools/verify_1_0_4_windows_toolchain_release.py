from __future__ import annotations
from pathlib import Path
import argparse, json, sys

parser = argparse.ArgumentParser(description='Verify VulkanScope Database 1.0.4 Windows/toolchain/release hardening')
parser.add_argument('--root', default=None)
args = parser.parse_args()
root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors: list[str] = []

def need(ok: bool, msg: str) -> None:
    if not ok:
        errors.append(msg)

def text(rel: str) -> str:
    return (root / rel).read_text(encoding='utf-8')

pkg = json.loads(text('worker/package.json'))
need(pkg.get('version') == '1.0.4', 'Worker package version must be 1.0.4')
need((pkg.get('devDependencies') or {}).get('wrangler') == '4.130.0', 'Wrangler must be exactly pinned to 4.130.0')
allow = pkg.get('allowScripts') or {}
for dep in ('esbuild', 'sharp', 'workerd'):
    need(allow.get(dep) is True, f'allowScripts must explicitly approve reviewed {dep} install scripts')
need((pkg.get('scripts') or {}).get('security:audit') == 'npm audit --audit-level=high', 'security:audit script missing or weakened')

portable = [
    'tools/test_compare_04141_compat.mjs',
    'tools/test_compare_04141_negative_mutations.mjs',
    'tools/test_surface_compare_04142.mjs',
    'tools/test_surface_compare_04142_negative_mutations.mjs',
]
for rel in portable:
    s = text(rel)
    need("fileURLToPath" in s and "from 'node:url'" in s, f'{rel} must use fileURLToPath for import.meta.url')
    need('new URL(import.meta.url).pathname' not in s, f'{rel} retains Windows-unsafe URL pathname conversion')

index = text('index.html')
app = text('assets/app.v1004.js')
need('VulkanScope Database <strong>1.0.4</strong>' in index, '1.0.4 footer identity missing')
need('app.v1004.js?v=1004' in index and 'config.js?v=1004' in index and 'site.v0390.css?v=1004' in index, '1.0.4 cache identity missing')
need('Database 1.0.4 · schema' in app, 'frontend Database 1.0.4 identity missing')

workflow = text('tools/pages.workflow.yml')
need('tags: ["v*"]' in workflow, 'tag trigger missing from canonical workflow')
need('windows-tooling:' in workflow and 'runs-on: windows-latest' in workflow, 'mandatory Windows tooling job missing')
need('node tools/test_compare_04141_compat.mjs' in workflow, 'Windows job does not execute compare path regression')
need('node tools/test_surface_compare_04142.mjs' in workflow, 'Windows job does not execute Surface path regression')
need('release:' in workflow and 'startsWith(github.ref, \'refs/tags/v\')' in workflow, 'tag release job missing')
need('python tools/package_release.py dist' in workflow, 'release job does not build deterministic package')
need('gh release create' in workflow and 'gh release upload' in workflow, 'release job is not retry-safe / GitHub-hosted gh based')
need('GH_TOKEN: ${{ github.token }}' in workflow, 'release job does not use scoped GitHub token')
need(text('.github/workflows/pages.yml') == workflow, 'checked-in pages.yml differs from canonical workflow template')

packager = text('tools/package_release.py')
need('ZipInfo' in packager and '1980, 1, 1, 0, 0, 0' in packager, 'deterministic ZIP timestamp policy missing')
need("worker/package-lock.json" in packager, 'release packager must explicitly exclude local optional package lock')
need('verify_regression_contract.py' in packager and '--strict-tree' in packager, 'release packager must enforce strict regression tree')

rules = text('rules/PROJECT_RULES.md')
need('## Release 1.0.4 Windows/toolchain/release hardening requirements' in rules, '1.0.4 rules section missing')
need('Wrangler 4.130.0' in rules, '1.0.4 rules do not pin reviewed Wrangler version')
need('Windows' in rules and 'fileURLToPath' in rules, '1.0.4 Windows URL-path rule missing')

if errors:
    print('FAIL VulkanScope Database 1.0.4 Windows/toolchain/release audit')
    for e in errors:
        print(' - ' + e)
    raise SystemExit(1)
print('PASS VulkanScope Database 1.0.4: Windows-safe Node paths, reviewed install-script policy, Wrangler 4.130.0, automatic tag release')
