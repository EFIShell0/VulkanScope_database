# VulkanScope Database 1.4.8 build / compatibility audit

- Release focus: VulkanScope 2.0.6+ POST admission, Vulkan 1.4.364 registry/header compatibility and exact 2.0.6 device-envelope acceptance.
- Immutable predecessor: VulkanScope Database 1.4.7, ZIP SHA-256 `72464d6e0aa9fb1518cd045281428458cd480fafa7c5333b22643f619a781fcb`.
- New submissions below VulkanScope 2.0.6 are rejected before generic validation; historical stored reports remain readable and unchanged.
- Database/frontend/Worker source: 1.4.8; current assets v1408; immediate JavaScript bridge v1407.
- Producer/query baseline: VulkanScope 2.0.6 · Vulkan 1.4.364.
- Registry/header lock: Vulkan 1.4.364 / VK_HEADER_VERSION 364 / 477 registered extensions.
- D1 migration: none. Normalizer: 16 unchanged. Stored payload/hash rewrite: forbidden.
- Live Cloudflare Worker deployment remains a separate evidence class and is not implied by source/package verification.

# VulkanScope Database 1.4.7 build audit

- Release focus: producer-floor metadata coherence between Pages, preload and Worker source.
- VulkanScope 1.4.3+ remains the new-submission floor.
- Live Cloudflare Worker deploy/runtime evidence is separate and NOT EXECUTED by source/package verification.

# VulkanScope Database 1.4.7 build / regression audit

Database 1.4.7 succeeds immutable Database 1.4.5 (ZIP SHA-256 `1b2a4119dd5abb2474535548d07d3c0d1057bf9bc427d1a29ae210cda4e4adc5`). D1 schema/migrations, stored report bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362, validated browser floors and all Vulkan® evidence semantics remain unchanged.

This admission release raises the server-enforced new-report producer floor from VulkanScope 1.4.0 to **VulkanScope 1.4.3**. VulkanScope 1.4.3 is accepted at the floor; 1.4.2 and every lower producer are rejected before generic submission validation. Existing stored historical reports below the floor remain readable and are not deleted, rewritten or rehashed.

- Database / frontend / Worker: 1.4.7
- Current producer/query baseline: VulkanScope 1.4.3 · Vulkan 1.4.362
- New-submission compatibility floor: VulkanScope 1.4.3+ · schema 2 / technical report 3
- Current app: `assets/app.v1407.js`
- Current browser gate: `assets/browser-compat.v1407.js`
- Current release bootstrap: `assets/release-bootstrap.v1407.js`
- Current stylesheet: `assets/site.v1407.css`
- Cache key: 1407
- Immutable predecessor: 1.4.5

`tools/quality_gate.py` verifies the immutable 1.4.5 boundary, focused producer-floor contract and negative mutations, Worker transport behavior, historical-read compatibility, source audit, D1 replay, Pages allow-list staging and release-ready transition. Deterministic packaging repeats strict verification against a clean extraction.

## Executed 1.4.8 release evidence
- `tools/verify_vulkan_registry.py`: PASS for Vulkan 1.4.364, header 364, 477 registered extensions and locked registry SHA-256.
- `tools/verify_1_4_8_vulkanscope_2_0_6_compatibility.py`: PASS.
- `tools/test_1_4_8_vulkanscope_2_0_6_compatibility_negative_mutations.py`: PASS for nine contract mutations plus unrelated-documentation false-positive control.
- `worker/tests/contract.mjs`: PASS, including 2.0.6 acceptance, 2.0.5/1.x rejection, 2.x versionCode identity, 2.0.6 device environment validation and historical stored-report readability.
- `tools/quality_gate.py`: PASS, including source audit, D1 migration replay, Pages allow-list staging and release-ready transition.
- Deterministic strict package clean extraction: PASS. No D1 migration was added or applied by this source verification.
- Live Cloudflare Worker deployment: NOT EXECUTED by the source/package build; the 2.0.6 production POST floor requires an explicit successful Worker deployment.
