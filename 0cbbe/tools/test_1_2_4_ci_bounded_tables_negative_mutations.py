from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1204.js','assets/browser-compat.v1204.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','data/release.json','tools/build_index.py','tools/pages.workflow.yml','.github/workflows/pages.yml','worker/src/index.js','worker/tests/contract.mjs']
verifier=root/'tools/verify_1_2_4_ci_bounded_tables.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-124-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('stale-workflow-verifier','tools/pages.workflow.yml','python tools/verify_1_2_4_ci_bounded_tables.py','python tools/verify_1_2_2_release_retry.py')
fixture('generated-index-version','tools/build_index.py','"databaseVersion":"1.2.4"','"databaseVersion":"1.2.3"')
fixture('devices-pagination','assets/app.v1204.js',"boundedReportTable('devices-main'","table(['Device'")
fixture('queues-pagination','assets/app.v1204.js',"boundedReportTable('queues-main'","table(['Device'")
fixture('surface-pagination','assets/app.v1204.js',"boundedReportTable('surface-formats'","table(['Device'")
fixture('display-pagination','assets/app.v1204.js',"boundedReportTable('display-main'","table(['Device'")
fixture('row-slice','assets/app.v1204.js','rows.slice(start,end)','rows')
print('PASS 1.2.4 negative mutation suite')
