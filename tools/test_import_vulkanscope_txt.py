from pathlib import Path
import json
import subprocess
import sys
import tempfile

root=Path(__file__).resolve().parents[1]
importer=root/'tools'/'import_vulkanscope_txt.py'
fixture='''VulkanScope report
Application version: 0.41.13
Application version code: 423
GPU: Fixture GPU
API: 1.4.0
Driver version: 1
Driver mode: System Vulkan driver
Loader / instance API: 1.4.0
Vendor: 0x1234
Device ID: 0x5678
Android: Example Model, Android 16, SDK 36
Application ABI: arm64-v8a
Supported device ABIs: arm64-v8a
DEVICE #1: Fixture GPU
[VkPhysicalDeviceExampleProperties] booleanPropertyFalse = false
[VkPhysicalDeviceExampleFeatures] featureFalse = false
LIMITS
zeroLimit = 0
SURFACE
genericBooleanProperty = false
'''

with tempfile.TemporaryDirectory(prefix='vulkanscope-import-test-') as tmp:
    tmp=Path(tmp)
    source=tmp/'report.txt'
    output=tmp/'report.json'
    source.write_text(fixture,encoding='utf-8')
    subprocess.run([sys.executable,str(importer),str(source),'--output',str(output)],cwd=root,check=True,capture_output=True,text=True)
    report=json.loads(output.read_text(encoding='utf-8'))

states={(x['section'],x['name']):x['status'] for x in report['capabilities']}
assert states[('VkPhysicalDeviceExampleProperties','booleanPropertyFalse')]=='available'
assert states[('VkPhysicalDeviceExampleFeatures','featureFalse')]=='unsupported'
assert states[('LIMITS','zeroLimit')]=='available'
assert states[('SURFACE','genericBooleanProperty')]=='available'
print('VulkanScope Database TXT import semantics: ALL PASS')
