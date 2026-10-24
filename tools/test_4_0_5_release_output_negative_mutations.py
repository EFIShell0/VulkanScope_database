from pathlib import Path
import ast
root=Path(__file__).resolve().parents[1]
source=(root/'tools/package_release.py').read_text(encoding='utf-8')
tree=ast.parse(source)
# Require an actual executed preflight rejection before source hygiene and mkdir.
required=["out_dir.relative_to(root)", "raise SystemExit('FAIL release output directory must be OUTSIDE source checkout", "repair_repository.py", "out_dir.mkdir(parents=True, exist_ok=True)", 'ZipInfo(rel, (1980, 1, 1, 0, 0, 0))', 'compresslevel=9', 'clean-extract=strict-PASS']
for token in required:
    if token not in source: raise SystemExit('FAIL missing release output safety/determinism guard: '+token)
if not (source.index('out_dir.relative_to(root)') < source.index('OUTSIDE source checkout') < source.index('repair_repository.py') < source.index('out_dir.mkdir(')):
    raise SystemExit('FAIL release output preflight is not before source check/output creation')
try:
    (root/'dist').relative_to(root)
except ValueError:raise SystemExit('FAIL regression fixture: in-source dist not recognized')
try:
    (root.parent/'vsdb405-external-output').relative_to(root)
except ValueError: pass
else: raise SystemExit('FAIL regression fixture: external build destination not recognized')
for rel in ('.github/workflows/pages.yml','tools/pages.workflow.yml'):
    wf=(root/rel).read_text(encoding='utf-8')
    for token in ('$RUNNER_TEMP/vulkanscope-release-405', 'python tools/package_release.py', 'cmp', 'sha256sum', 'VulkanScope-Database-4.0.5.zip.sha256'):
        if token not in wf: raise SystemExit(f'FAIL {rel} lacks external repeated hash-gated package step: {token}')
    if 'python tools/package_release.py dist' in wf: raise SystemExit('FAIL in-checkout release destination restored')
print('PASS 4.0.5 release output: pre-mkdir fail-closed source path guard, external CI double build and SHA comparison')
