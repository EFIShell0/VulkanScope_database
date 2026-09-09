from pathlib import Path
import json, shutil, subprocess, sys, tempfile

root = Path(__file__).resolve().parents[1]
verifier = root / 'tools' / 'verify_1_0_4_windows_toolchain_release.py'

def run(tree: Path) -> int:
    return subprocess.run([sys.executable, str(verifier), '--root', str(tree)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode

with tempfile.TemporaryDirectory(prefix='vsdb104-neg-') as td:
    base = Path(td) / 'tree'
    shutil.copytree(root, base, ignore=shutil.ignore_patterns('.git','node_modules','_site','__pycache__'))
    if run(base) != 0:
        raise SystemExit('FAIL control tree rejected by 1.0.4 verifier')
    mutations = []
    mutations.append(('windows-url-path', 'tools/test_compare_04141_compat.mjs', "path.dirname(fileURLToPath(import.meta.url))", "path.dirname(new URL(import.meta.url).pathname)"))
    mutations.append(('release-job', 'tools/pages.workflow.yml', '  release:\n', '  release_disabled:\n'))
    mutations.append(('cache-key', 'index.html', 'app.v1006.js?v=1006', 'app.v1006.js?v=1003'))
    for label, rel, old, new in mutations:
        p = base / rel
        original = p.read_text(encoding='utf-8')
        if old not in original:
            raise SystemExit(f'FAIL mutation source missing: {label}')
        p.write_text(original.replace(old, new, 1), encoding='utf-8')
        if rel == 'tools/pages.workflow.yml':
            (base / '.github/workflows/pages.yml').write_text(p.read_text(encoding='utf-8'), encoding='utf-8')
        if run(base) == 0:
            raise SystemExit(f'FAIL negative mutation accepted: {label}')
        p.write_text(original, encoding='utf-8')
        if rel == 'tools/pages.workflow.yml':
            (base / '.github/workflows/pages.yml').write_text(original, encoding='utf-8')
    pkgp = base / 'worker/package.json'
    original = pkgp.read_text(encoding='utf-8')
    pkg = json.loads(original); pkg['devDependencies']['wrangler'] = '4.125.0'; pkgp.write_text(json.dumps(pkg, indent=2)+'\n', encoding='utf-8')
    if run(base) == 0:
        raise SystemExit('FAIL negative mutation accepted: stale Wrangler')
    pkgp.write_text(original, encoding='utf-8')
    pkg = json.loads(original); del pkg['allowScripts']['workerd']; pkgp.write_text(json.dumps(pkg, indent=2)+'\n', encoding='utf-8')
    if run(base) == 0:
        raise SystemExit('FAIL negative mutation accepted: unreviewed workerd install script')
print('PASS VulkanScope Database 1.0.6 negative mutations')
