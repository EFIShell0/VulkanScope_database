from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parents[1]
errors=[]
def check(cond,msg):
    if not cond: errors.append(msg)
index=(root/'index.html').read_text()
app=(root/'assets/app.v0357.js').read_text()
worker=(root/'worker/src/index.js').read_text()
rules=(root/'rules/PROJECT_RULES.md').read_text()
check('VulkanScope Database <strong>0.35.7</strong>' in index,'index version')
check('site.v0357.css' in index and 'app.v0357.js' in index and 'config.js?v=0357' in index,'cache-busted asset refs')
check('connect-src \'self\' https://vulkanscope-database-api.vulkanscope.workers.dev' in index,'CSP API pin')
check('Database 0.35.7' in app,'frontend version')
check('fetchJsonBounded' in app and '20000' in app and '4194304' in app,'bounded frontend API reads')
check('seenCursors' in app and 'Math.min(4,queue.length)' in app,'cursor/concurrency bounds')
check("hdrCapabilityStatus" in app and "return'unknown'" in app,'HDR missing/explicit semantics')
check('Not reported' in app and 'universe=new Map()' in app,'aggregate unknown denominator')
check("publishedVulkanSpec:'Vulkan 1.4.359 (2026-08-07)'" in worker,'published spec metadata')
check("VulkanScope producer/query baseline 1.4.360" in worker,'producer baseline metadata')
check('normalizerVersion:10' in worker,'normalizer version')
check('validTechnicalReport' in worker and 'validReportText' in worker,'producer contract validation')
check('cross-origin-resource-policy' in worker and 'cross-origin-opener-policy' in worker and 'content-security-policy' in worker,'API response security headers')
check("'clientip'" in worker and 'normalizedKey' in worker and 'hasSensitiveKey' in worker,'privacy key filter')
check('2*1024*1024' in worker and 'readBoundedBody' in worker,'streaming body bound')
check('1.4.359' in rules and '1.4.360' in rules,'spec/baseline distinction rules')
check('Release 0.35.7 producer/database full audit' in rules,'release rules')
json.loads((root/'report.schema.json').read_text())
for f in ['400.html','401.html','403.html','404.html','405.html','408.html','409.html','413.html','415.html','429.html','500.html','502.html','503.html','504.html','error.html']:
    t=(root/f).read_text();check('site.v0357.css' in t,f'{f} CSS version')
if errors:
    print('AUDIT FAIL')
    for e in errors: print('-',e)
    sys.exit(1)
print('VulkanScope Database 0.35.7 audit: PASS')
