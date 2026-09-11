from pathlib import Path
import shutil, subprocess, sys, tempfile

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='vsdb-1011-workflow-negative-') as td:
    fixture=Path(td)/'fixture'
    shutil.copytree(root,fixture,ignore=shutil.ignore_patterns('.git','node_modules','.wrangler','dist','_site','__pycache__'))
    good="""      - name: Reverify generated index metadata\n        run: |\n          python tools/verify_1_0_11_workflow_command_boundary.py\n          python tools/test_1_0_11_workflow_command_boundary_negative_mutations.py\n"""
    bad="""      - name: Reverify generated index metadata\n        run: python tools/verify_1_0_11_workflow_command_boundary.py\n          python tools/test_1_0_11_workflow_command_boundary_negative_mutations.py\n"""
    for rel in ('.github/workflows/pages.yml','tools/pages.workflow.yml'):
        p=fixture/rel
        text=p.read_text(encoding='utf-8')
        if good not in text:
            raise SystemExit(f'fixture cannot locate corrected workflow command block in {rel}')
        p.write_text(text.replace(good,bad,1),encoding='utf-8',newline='\n')
    r=subprocess.run([sys.executable,str(fixture/'tools/verify_1_0_11_workflow_command_boundary.py'),'--root',str(fixture)],text=True,capture_output=True)
    if r.returncode==0:
        raise SystemExit('negative workflow mutation unexpectedly passed current verifier')
    output=(r.stdout or '')+(r.stderr or '')
    if 'YAML run block with two distinct commands' not in output and 'workflow command boundary regressed' not in output:
        raise SystemExit('negative workflow mutation failed for the wrong reason:\n'+output)
print('PASS Database 1.0.11 negative mutation: malformed GitHub Actions command boundary is rejected')
