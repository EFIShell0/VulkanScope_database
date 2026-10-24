#!/usr/bin/env python3
"""Current-release checks; historical immutable 4.0.5 validators remain archived."""
from pathlib import Path
import subprocess,sys, tempfile
R=Path(__file__).resolve().parents[1]
def run(*cmd,cwd=R):
    print('>',' '.join(map(str,cmd)),flush=True)
    p=subprocess.run(cmd,cwd=cwd)
    if p.returncode:raise SystemExit(p.returncode)
run(sys.executable,'-B','tools/test_utf8_text_io.py')
run(sys.executable,'-B','tools/verify_optional_npm_lock.py')
run(sys.executable,'-B','tools/verify_vulkan_registry.py')
run(sys.executable,'-B','tools/verify_4_0_6_release.py')
run(sys.executable,'-B','tools/repair_repository.py','--check')
run('node','tools/test_report_text_identity.mjs')
run('node','tools/test_routes.mjs')
run('node','tools/test_compare_contract.mjs')
run('node','worker/tests/contract.mjs')
run(sys.executable,'-B','tools/audit_database.py','--source-tree','.')
with tempfile.TemporaryDirectory(prefix='vulkanscope-db-406-') as stage:
    run(sys.executable,'-B','tools/build_pages_artifact.py',stage)
    run(sys.executable,'-B','tools/audit_database.py','--artifact-tree',stage)
    run(sys.executable,'-B','tools/mark_release_ready.py',stage)
    run(sys.executable,'-B','tools/audit_database.py','--artifact-tree',stage,'--require-release-ready')
print('PASS VulkanScope Database 4.0.6 QA; source only, no live Cloudflare deployment')
