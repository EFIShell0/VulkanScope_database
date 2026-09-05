from pathlib import Path
import argparse, hashlib, shutil, sys

root = Path(__file__).resolve().parents[1]
canonical = root / 'tools' / 'pages.workflow.yml'
workflow_dir = root / '.github' / 'workflows'
workflow = workflow_dir / 'pages.yml'
CURRENT_APP = 'app.v03927.js'

parser = argparse.ArgumentParser(description='Verify or repair VulkanScope Database repository update-critical files')
parser.add_argument('--check', action='store_true', help='Verify canonical workflow and stale versioned assets only')
parser.add_argument('--apply', action='store_true', help='Replace workflow directory with canonical pages.yml and remove stale versioned app assets')
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
    return sorted(p for p in assets.glob('app.v*.js') if p.name != CURRENT_APP)

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
    print('Repository repair applied: canonical pages.yml installed; stale workflows/versioned app JS removed.')

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
    errors.append('stale versioned frontend assets: ' + ', '.join(str(p.relative_to(root)) for p in apps))
if not (root/'assets'/CURRENT_APP).is_file():
    errors.append(f'missing assets/{CURRENT_APP}')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'VulkanScope Database 0.39.27 repository state: PASS')
print(f'pages.yml sha256={digest(workflow)}')
print(f'audit.py sha256={digest(root / "tools" / "audit_database.py")}')
