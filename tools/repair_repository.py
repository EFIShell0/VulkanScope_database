from pathlib import Path
import argparse, hashlib, shutil, sys

root = Path(__file__).resolve().parents[1]
canonical = root / 'tools' / 'pages.workflow.yml'
workflow_dir = root / '.github' / 'workflows'
workflow = workflow_dir / 'pages.yml'
CURRENT_APP = 'app.v1400.js'
CURRENT_BROWSER_COMPAT = 'browser-compat.v1400.js'
CURRENT_RELEASE_BOOTSTRAP = 'release-bootstrap.v1400.js'
PREDECESSOR_BRIDGE = {'app.v1310.js','browser-compat.v1310.js','release-bootstrap.v1310.js'}

parser = argparse.ArgumentParser(description='Verify or repair VulkanScope Database repository update-critical files')
parser.add_argument('--check', action='store_true', help='Verify canonical workflow and stale versioned assets only')
parser.add_argument('--apply', action='store_true', help='Replace workflow directory with canonical pages.yml, remove stale versioned app/browser-compat assets, and purge ignored legacy worker/package-lock.json workspace state')
args = parser.parse_args()
if not (args.check or args.apply):
    parser.error('choose --check or --apply')

if not canonical.is_file():
    raise SystemExit('missing canonical workflow template tools/pages.workflow.yml')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stale_workflows():
    if not workflow_dir.is_dir():
        return []
    return sorted(p for p in workflow_dir.iterdir() if p.is_file() and p.name != 'pages.yml')


def stale_apps():
    assets = root / 'assets'
    return sorted(p for p in assets.glob('app.v*.js') if p.name not in {CURRENT_APP,*PREDECESSOR_BRIDGE})

def stale_browser_compats():
    assets = root / 'assets'
    return sorted(p for p in assets.glob('browser-compat.v*.js') if p.name not in {CURRENT_BROWSER_COMPAT,*PREDECESSOR_BRIDGE})

def stale_release_bootstraps():
    assets = root / 'assets'
    return sorted(p for p in assets.glob('release-bootstrap.v*.js') if p.name not in {CURRENT_RELEASE_BOOTSTRAP,*PREDECESSOR_BRIDGE})

optional_lock = root / 'worker' / 'package-lock.json'

if args.apply:
    workflow_dir.mkdir(parents=True, exist_ok=True)
    for p in list(workflow_dir.iterdir()):
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
    shutil.copy2(canonical, workflow)
    for p in stale_apps():
        p.unlink()
    for p in stale_browser_compats():
        p.unlink()
    for p in stale_release_bootstraps():
        p.unlink()
    lock_removed = False
    if optional_lock.is_file():
        optional_lock.unlink()
        lock_removed = True
    suffix = '; ignored legacy worker/package-lock.json removed' if lock_removed else ''
    print('Repository repair applied: canonical pages.yml installed; stale workflows/versioned frontend JS removed; immediate predecessor bridge retained' + suffix + '.')

errors=[]
if not workflow.is_file():
    errors.append('missing .github/workflows/pages.yml')
elif workflow.read_bytes() != canonical.read_bytes():
    errors.append('stale/non-canonical .github/workflows/pages.yml; run: python tools/repair_repository.py --apply')
extras=stale_workflows()
if extras:
    errors.append('stale workflow files: ' + ', '.join(str(p.relative_to(root)) for p in extras))
apps=stale_apps()
if apps:
    errors.append('stale versioned frontend app assets: ' + ', '.join(str(p.relative_to(root)) for p in apps))
compats=stale_browser_compats()
if compats:
    errors.append('stale versioned browser-compat assets: ' + ', '.join(str(p.relative_to(root)) for p in compats))
boots=stale_release_bootstraps()
if boots:
    errors.append('stale versioned release-bootstrap assets: ' + ', '.join(str(p.relative_to(root)) for p in boots))
if not (root/'assets'/CURRENT_APP).is_file():
    errors.append(f'missing assets/{CURRENT_APP}')
if not (root/'assets'/CURRENT_BROWSER_COMPAT).is_file():
    errors.append(f'missing assets/{CURRENT_BROWSER_COMPAT}')
if not (root/'assets'/CURRENT_RELEASE_BOOTSTRAP).is_file():
    errors.append(f'missing assets/{CURRENT_RELEASE_BOOTSTRAP}')
for bridge in sorted(PREDECESSOR_BRIDGE):
    if not (root/'assets'/bridge).is_file(): errors.append(f'missing predecessor bridge asset assets/{bridge}')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'VulkanScope Database 1.4.0 repository state: PASS')
print(f'pages.yml sha256={digest(workflow)}')
print(f'audit.py sha256={digest(root / "tools" / "audit_database.py")}')
