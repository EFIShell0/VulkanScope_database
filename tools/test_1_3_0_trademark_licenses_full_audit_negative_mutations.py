from pathlib import Path
import tempfile,shutil,subprocess,sys
root=Path(__file__).resolve().parents[1]
required=['assets/app.v1300.js','assets/browser-compat.v1300.js','assets/site.v0390.css','index.html','rules/PROJECT_RULES.md','rules/1.3.0_TRADEMARK_LICENSES_FULL_AUDIT.md','data/release.json','tools/build_index.py','tools/build_pages_artifact.py','tools/audit_database.py','tools/pages.workflow.yml','.github/workflows/pages.yml','tools/repair_repository.py','worker/src/index.js','worker/package.json','licenses/wrangler.md','licenses/sharp.md','licenses/esbuild.md','licenses/workerd.md','licenses/nodejs.md','licenses/python.md']
verifier=root/'tools/verify_1_3_0_trademark_licenses_full_audit.py'
def fixture(name,rel,old,new):
    with tempfile.TemporaryDirectory(prefix='vsdb-1300-neg-') as td:
        t=Path(td)
        for f in required:
            q=t/f; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(root/f,q)
        p=t/rel; s=p.read_text(encoding='utf-8')
        if old not in s: raise SystemExit(f'fixture token missing {name}: {old}')
        p.write_text(s.replace(old,new,1),encoding='utf-8')
        r=subprocess.run([sys.executable,str(verifier),'--root',str(t)],capture_output=True,text=True)
        if r.returncode==0: raise SystemExit(f'negative mutation unexpectedly passed: {name}')
        print('PASS negative',name)
fixture('trademark-replacement','assets/app.v1300.js',"replace(VULKAN_TRADEMARK_RE,'Vulkan®')","replace(VULKAN_TRADEMARK_RE,'Vulkan')")
fixture('raw-preservation','assets/app.v1300.js','pre,code,script,style,textarea,.raw','script,style,textarea')
fixture('footer-disclaimer','index.html','VulkanScope projesinin Khronos Group ile hiçbir ilgisi yoktur, resmi Khronos Group projesi değildir','VulkanScope independence notice')
fixture('information-disclaimer','assets/app.v1300.js','VulkanScope projesinin Khronos Group ile hiçbir ilgisi yoktur, resmi Khronos Group projesi değildir','VulkanScope independence notice')
fixture('license-action','assets/app.v1300.js','Read license (.md)','License')
fixture('wrangler-license-file','assets/app.v1300.js',"licenseFile:'./licenses/wrangler.md'","licenseFile:'https://example.invalid/wrangler.md'")
fixture('license-pages-copy','tools/build_pages_artifact.py',"license_files=['wrangler.md','sharp.md','esbuild.md','workerd.md','nodejs.md','python.md']","license_files=['wrangler.md']")
fixture('selector-page-limit','assets/app.v1300.js','const CUSTOM_SELECT_OPTION_LIMIT=50;','const CUSTOM_SELECT_OPTION_LIMIT=100;')
fixture('json-download','assets/app.v1300.js','?compact=1&_download=${Date.now()}','?_download=${Date.now()}')
fixture('workflow-gate','tools/pages.workflow.yml','python tools/verify_1_3_0_trademark_licenses_full_audit.py','python tools/verify_1_2_15_information_json_export.py')
print('PASS 1.3.0 Vulkan® / licenses / full-audit negative mutation suite')
