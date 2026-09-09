from pathlib import Path
import argparse, json, re

parser=argparse.ArgumentParser()
parser.add_argument('--root', default=None)
parser.add_argument('--skip-version', action='store_true')
args=parser.parse_args()
root=Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def text(rel):
    p=root/rel
    return p.read_text(encoding='utf-8') if p.is_file() else ''

def jload(rel):
    try: return json.loads(text(rel))
    except Exception: return {}

worker=text('worker/src/index.js')
tests=text('worker/tests/contract.mjs')
index=text('index.html')
app=text('assets/app.v1000.js') if not args.skip_version else text('assets/app.v1005.js')
rules=text('rules/PROJECT_RULES.md')
audit=text('rules/1.0.0_VULKANSCOPE_1.0.0_PRODUCER_BASELINE_AUDIT.md')
pkg=jload('worker/package.json')
static=jload('data/index.json')

if not args.skip_version:
    need(pkg.get('version')=='1.0.0','Worker package version must be 1.0.0')
    need('VulkanScope Database <strong>1.0.0</strong>' in index,'Database 1.0.0 footer identity missing')
    need('app.v1000.js?v=1000' in index and 'config.js?v=1000' in index and 'site.v0390.css?v=1000' in index,'1.0.0 cache-busted frontend identity missing')
    need('Database 1.0.0' in app and 'VulkanScope 1.0.0 · Vulkan 1.4.362' in app,'1.0.0 frontend producer identity missing')
    need(static.get('databaseVersion')=='1.0.0','static index databaseVersion must be 1.0.0')
    need(static.get('producerQueryBaseline')=='VulkanScope 1.0.0 · Vulkan 1.4.362','static producer baseline must be VulkanScope 1.0.0 / Vulkan 1.4.362')
need(static.get('compatibleProducer')=='VulkanScope 0.80.3+ · schema 2 / technical report 3','new-submission floor/schema metadata drifted')
need(static.get('normalizerVersion')==16,'normalizer must remain 16')

need("/^(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)$/" in worker,'producer parser must accept canonical major.minor.patch across major versions')
need('const versionAtLeast=' in worker and 'v.major' in worker and 'v.minor' in worker and 'v.patch' in worker,'range-aware producer comparator missing')
need(("if(v.major===1&&v.minor===0&&v.patch===0)return p.application.versionCode===1000" in worker) or ("if(v.major===1&&v.minor===0)return p.application.versionCode===1000+v.patch" in worker),'1.0.0 / versionCode 1000 identity is not fail-closed')
need("producerAtLeast0803=p=>{const v=producerVersion(p);return!!v&&versionAtLeast(v,0,80,3)}" in worker,'0.80.3 new-submission floor no longer range-aware across major versions')

if not args.skip_version:
    need("producerQueryBaseline:'VulkanScope 1.0.0 · Vulkan 1.4.362'" in worker,'Worker health/list producer baseline is not 1.0.0')
need("registryVersion=producerAtLeast08010(p)?'1.4.362':'1.4.361'" in worker,'Vulkan 1.4.362 current-producer registry selector drifted')
need('baseline=`Vulkan ${registryVersion}`' in worker,'exact Vulkan-prefixed producer registry baseline drifted')
need('header=`${baseline} compile headers; validated query catalog ${baseline}`' in worker,'exact header provenance derivation drifted')
need('VulkanScope 0.80.3 or newer is required for new submissions' in worker,'0.80.3 floor error contract drifted')

need("current1000.application.version='1.0.0'" in tests and 'current1000.application.versionCode=1000' in tests,'canonical 1.0.0 / 1000 fixture missing')
need("assert.equal(r.status,201,'VulkanScope 1.0.0 / 1000 must be accepted')" in tests,'canonical 1.0.0 acceptance assertion missing')
need('bad1000Identity.application.versionCode=816' in tests and '/producer_identity/' in tests,'1.0.0 producer-identity negative fixture missing')
need("current0812.application.version='0.80.12'" in tests and 'current0812.application.versionCode=812' in tests,'0.80.12 compatibility fixture missing')
need("legacy.application.version='0.80.9'" in tests or "application:{name:'VulkanScope',version:'0.80.9'" in tests,'0.80.9 compatibility fixture missing')

need('Release 1.0.0 / VulkanScope 1.0.0 producer-baseline requirements' in rules,'1.0.0 rules section missing')
need('0.39.27' in rules and 'bc87d37a8475091385ffd8155822c22ecdb65cd5e697307412cdab93cc8c1b63' in rules,'immutable 0.39.27 predecessor identity missing from rules')
need('Database 1.0.0' in audit and 'VulkanScope 1.0.0' in audit and 'versionCode 1000' in audit,'1.0.0 producer-baseline audit identity incomplete')
need((root/'regression/0.39.27_to_1.0.0_contract.json').is_file(),'1.0.0 immutable regression contract missing')

migrations=sorted(p.name for p in (root/'worker/migrations').glob('*.sql')) if (root/'worker/migrations').is_dir() else []
need(migrations==['0001_init.sql','0002_report_cursor_index.sql','0003_payload_chunks.sql'],f'D1 migration set changed unexpectedly: {migrations}')

if errors:
    print('FAIL VulkanScope Database 1.0.0 producer-baseline contract')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('PASS VulkanScope Database 1.0.0 producer baseline: app=1.0.0/1000 floor=0.80.3 Vulkan=1.4.362 schema=2 technicalReport=3 normalizer=16')
