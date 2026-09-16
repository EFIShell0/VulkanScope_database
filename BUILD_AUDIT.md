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
