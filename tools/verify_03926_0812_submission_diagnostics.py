from pathlib import Path
import sys
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
w=(root/"worker/src/index.js").read_text(encoding="utf-8")
t=(root/"worker/tests/contract.mjs").read_text(encoding="utf-8")
a=(root/"assets/app.v03926.js").read_text(encoding="utf-8")
e=[]
def need(c,m):
    if not c:e.append(m)
need("VulkanScope 0.80.12 · Vulkan 1.4.362" in w and "VulkanScope 0.80.12 · Vulkan 1.4.362" in a,"0.80.12 producer baseline metadata missing")
need("validation='envelope_shape'" in w,"envelope shape diagnostic missing")
need("validation='producer_identity'" in w,"producer identity diagnostic missing")
need("'vulkan_1_4_362_registry_contract'" in w,"1.4.362 registry diagnostic missing")
need("current0812.application.version='0.80.12'" in t and "current0812.application.versionCode=812" in t,"0.80.12 worker acceptance fixture missing")
need("assert.match(await r.text(),/producer_identity/)" in t,"producer diagnostic regression assertion missing")
need("assert.match(await r.text(),/vulkan_1_4_362_registry_contract/)" in t,"registry diagnostic regression assertion missing")
need("assert.match(await r.text(),/envelope_shape/)" in t,"envelope diagnostic regression assertion missing")
if e: raise SystemExit("FAIL Database 0.39.26 0.80.12 submission diagnostics\n- "+"\n- ".join(e))
print("PASS Database 0.39.26 VulkanScope 0.80.12 submission diagnostics")
