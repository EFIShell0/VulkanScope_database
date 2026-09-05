from pathlib import Path
import json, sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
errors=[]
def need(cond,msg):
    if not cond: errors.append(msg)
def text(rel):
    p=root/rel
    return p.read_text(encoding='utf-8') if p.is_file() else ''
worker=text('worker/src/index.js')
tests=text('worker/tests/contract.mjs')
rules=text('rules/PROJECT_RULES.md')
index=text('index.html')
app=text('assets/app.v03927.js')
package=json.loads(text('worker/package.json'))
need(package.get('version')=='0.39.27','Database/Worker version is not 0.39.27')
need('VulkanScope Database <strong>0.39.27</strong>' in index and 'app.v03927.js?v=03927' in index,'0.39.27 browser identity/cache-bust missing')
need('Database 0.39.27 · schema' in app,'0.39.27 frontend release identity missing')
need("registryVersion=producerAtLeast08010(p)?'1.4.362':'1.4.361'" in worker,'registry version selection drifted')
need('baseline=`Vulkan ${registryVersion}`' in worker,'Worker does not require the producer-emitted Vulkan-prefixed registry baseline')
need('header=`${baseline} compile headers; validated query catalog ${baseline}`' in worker,'header baseline is not derived from the exact prefixed producer baseline')
need("registryBaseline:'Vulkan 1.4.361'" in tests and "registryCoverage:{baseline:'Vulkan 1.4.361'" in tests,'0.80.9 canonical fixture does not use the exact producer baseline string')
need("current0810.vulkan.registryBaseline='Vulkan 1.4.362'" in tests and "current0810.technicalReport.registryCoverage.baseline='Vulkan 1.4.362'" in tests,'0.80.10+/0.80.12 canonical fixture does not use the exact producer baseline string')
need("unprefixed0812.vulkan.registryBaseline='1.4.362'" in tests and "unprefixed0809.vulkan.registryBaseline='1.4.361'" in tests,'unprefixed negative fixtures are missing')
need("assert.equal(r.status,400,'0.80.12 unprefixed registry baseline is not the producer contract')" in tests,'0.80.12 unprefixed baseline rejection assertion missing')
need("assert.equal(r.status,400,'0.80.9 unprefixed registry baseline is not the producer contract')" in tests,'0.80.9 unprefixed baseline rejection assertion missing')
need('Release 0.39.27 exact producer registry-baseline string requirements' in rules,'0.39.27 rules section missing')
need('`Vulkan 1.4.362`' in rules and '`Vulkan 1.4.361`' in rules,'rules do not lock exact producer-emitted registry baseline strings')
if errors:
    print('FAIL Database 0.39.27 registry-baseline producer-string contract')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('PASS Database 0.39.27 exact registry-baseline strings: 0.80.3-0.80.9=Vulkan 1.4.361; 0.80.10+=Vulkan 1.4.362')
