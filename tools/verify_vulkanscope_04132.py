from pathlib import Path
import json,re,sys
root=Path(__file__).resolve().parents[1]
c=json.loads((root/'compat/vulkanscope-0.41.32-contract.json').read_text(encoding='utf-8'))
w=(root/'worker/src/index.js').read_text(encoding='utf-8'); schema=json.loads((root/'report.schema.json').read_text(encoding='utf-8')); app=(root/'assets/app.v03918.js').read_text(encoding='utf-8'); errors=[]
def check(v,m):
    if not v: errors.append(m)
check(c['producerVersion']=='0.41.32' and c['producerVersionCode']==442,'producer contract identity')
check(c['submissionSchema']==2 and c['technicalReportSchema']==3,'schema contract')
for k in c['requiredEnvelopeAdditions']['gpu']: check(k in schema['properties']['gpu']['properties'],f'schema missing gpu.{k}')
for k in c['requiredEnvelopeAdditions']['driver']: check(k in schema['properties']['driver']['properties'],f'schema missing driver.{k}')
for k in c['requiredEnvelopeAdditions']['vulkan']: check(k in schema['properties']['vulkan']['properties'],f'schema missing vulkan.{k}')
for token in ["producerExactly04132",c['vulkanRegistryBaseline'],c['headerBaseline'],c['requiredPhysicalDeviceStruct'],f"r.catalogSchemaVersion!=={c['catalogSchemaVersion']}",f"r.implementedPhysicalDeviceStructCount!=={c['implementedPhysicalDeviceStructCount']}",f"r.validatedRuntimeQueryGroupCount!=={c['validatedRuntimeQueryGroupCount']}",f"r.runtimeRegistryTokenReferenceCount!=={c['runtimeRegistryTokenReferenceCount']}"]:
    check(str(token) in w,f'worker current producer contract missing {token}')
for marker in c['requiredCompleteMarkers']: check(marker in w,f'worker missing complete marker {marker}')
check('?compact=1' in app and "url.searchParams.get('compact')==='1'" in w,'frontend/Worker compact detail contract')
check('D1_INLINE_PAYLOAD_BYTES=1500000' in w and 'report_payload_chunks' in w,'D1 payload chunking contract')
check((root/'worker/migrations/0003_payload_chunks.sql').is_file(),'payload chunk migration missing')
if errors:
    print('\n'.join('FAIL '+x for x in errors));sys.exit(1)
print(f"PASS VulkanScope {c['producerVersion']} compatibility schema={c['submissionSchema']}/{c['technicalReportSchema']} registry={c['vulkanRegistryBaseline']} maxBytes={c['maxSubmissionBytes']}")
