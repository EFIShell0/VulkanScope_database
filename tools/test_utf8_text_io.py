from pathlib import Path
import ast, subprocess, sys

root = Path(__file__).resolve().parents[1]
errors = []

for path in sorted((root / 'tools').rglob('*.py')):
    tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr not in {'read_text', 'write_text'}:
            continue
        if not any(k.arg == 'encoding' for k in node.keywords):
            errors.append(f'{path.relative_to(root)}:{node.lineno} {node.func.attr} missing explicit encoding')

app = root / 'assets' / 'app.v03918.js'
raw = app.read_bytes()
try:
    raw.decode('cp1252')
except UnicodeDecodeError:
    pass
else:
    errors.append('frontend no longer reproduces the CP1252-vs-UTF-8 regression fixture')
try:
    raw.decode('utf-8')
except UnicodeDecodeError as exc:
    errors.append(f'frontend is not valid UTF-8: {exc}')

r = subprocess.run([sys.executable, str(root / 'tools' / 'verify_vulkanscope_04132.py')], cwd=root)
if r.returncode != 0:
    errors.append(f'verify_vulkanscope_04132.py failed with explicit UTF-8 I/O (exit {r.returncode})')

if errors:
    print('\n'.join('FAIL ' + x for x in errors))
    raise SystemExit(1)
print('PASS deterministic UTF-8 Python text I/O; Windows CP1252 regression fixture covered')
