# VulkanScope Database 1.4.12 build audit

- Immutable predecessor: 1.4.11 (`b2255293731e6a4b5dcb2b51466805b3a993378174446b7b0cd754395103a4eb`).
- Submission floor: VulkanScope 3.0.12 / versionCode 3012, schema 2 / technicalReport 3, Vulkan 1.4.364.
- Snapshot repair: D1 insert -> `ctx.waitUntil()` -> authenticated GitHub Actions workflow dispatch -> live-API snapshot rebuild -> Pages audit/deploy -> published-manifest report-ID verification.
- Admission/snapshot failure domains are separated; duplicate rows do not dispatch. The GitHub token remains a Worker secret.
- Release gates include focused verifier, negative mutations, Worker transport test, source/Pages audit, D1 replay, deterministic strict package and immutable predecessor regression contract.

# VulkanScope Database 1.4.11 build / VulkanScope 3.0.2 compatibility audit

- Immutable predecessor: VulkanScope Database 1.4.10, ZIP SHA-256 `c52ff548c05745d6a9e4c439406afe42179bc7a430f9df78772e0a4eb29750d0`, 827 files.
- Release focus: raise only the new-report producer floor to VulkanScope 3.0.2 / versionCode 3002 and advance release-authored compatibility metadata to the 3.0.2 producer contract.
- Database/frontend/Worker source: 1.4.11; current assets v1411; immediate JavaScript bridge v1410; stale v1409 JavaScript excluded from the strict package.
- New `POST /v1/reports` submissions below VulkanScope 3.0.2 are rejected before generic report validation. VulkanScope 3.0.2 / 3002 and a valid schema 2 / technicalReport 3 envelope are accepted by the Worker contract. VulkanScope 3.0.1 / 3001 and 2.x producers are rejected by the new floor.
- Historical stored reports below the floor remain readable through existing GET/list/Compare paths; no stored payload, timestamp, canonical report ID or hash rewrite is introduced.
- Vulkan registry/header remains Vulkan 1.4.364 / header 364 / 477 registered extensions. D1 migrations are unchanged, normalizer remains 16, and the 2 MiB submission ceiling is unchanged.
- VulkanScope 3.x producer identity is fail-closed with `versionCode = 3000 + minor*100 + patch`; unknown future major versions are not inferred.
- Failing-before-fix oracle: the 1.4.11 focused verifier was executed against an immutable 1.4.10 copy and failed non-zero because the predecessor lacks the v1411/current 3.0.2 release contract.
- `tools/verify_1_4_11_vulkanscope_3_0_2_compatibility.py`: PASS.
- `tools/test_1_4_11_vulkanscope_3_0_2_compatibility_negative_mutations.py`: PASS for nine contract mutations plus unrelated-documentation false-positive control.
- `worker/tests/contract.mjs`: PASS, including 3.0.2 floor acceptance, 3.0.1 and 2.1.16 floor rejection, bad 3.0.2 versionCode rejection, future 3.0.3 acceptance, exact environment-envelope validation and historical stored-report readability.
- `tools/audit_database.py --source-tree .`: PASS.
- `tools/quality_gate.py`: PASS, including Vulkan registry lock, immutable predecessor regression, Worker contract, D1 migration replay, Pages allow-list staging and release-ready transition.
- Deterministic strict package construction and clean-extract byte equality: PASS for the final release package; two independent package builds are required to be byte-identical before publication.
- Live Cloudflare Worker deployment: NOT EXECUTED by this source/package build. The VulkanScope 3.0.2 production submission floor is not live until the intended Worker source is explicitly deployed successfully.

# VulkanScope Database 1.4.10 build / UI audit

- Immutable predecessor: VulkanScope Database 1.4.9, ZIP SHA-256 `6f06b29623a76389562e391dfc018311f672e31cbe07fa6f381c8152b41c1265`.
- Release focus: readable Profiles evaluator detail, single-stage startup loader with restored rotating circle and no scrollbar chrome, complete report Submitted seasonal-time evidence, and animated open/close column geometry.
- Database/frontend/Worker source: 1.4.10; current assets v1410; immediate JavaScript bridge v1409.
- New-submission floor remains VulkanScope 2.0.6+ · schema 2 / technical report 3. Registry/header remains Vulkan 1.4.364 / 364.
- Report-time presentation remains derived from server-authored `submitted_at`; D1 timestamps, stored payloads, hashes and IDs are unchanged.
- Static preload + live index + `/v1/sync` delta behavior is retained; no per-report Pages deployment is required.
- D1 migration: none. Normalizer: 16 unchanged. Stored payload/hash rewrite: forbidden.
- Live Cloudflare Worker deployment remains a separate evidence class and is not implied by source/package verification.

# VulkanScope Database 1.4.9 build / UI-startup audit

- Immutable predecessor: VulkanScope Database 1.4.8, ZIP SHA-256 `ea6233a92cc5ec95951caef9d17eb11c0bdeb6c7a2794637b8ab07fd66af911e`.
- Release focus: application-style Profile evaluator detail, non-touching page-scroll chrome, complete animated regional time preview, parallel live/snapshot startup, and responsive application-logo loading animation.
- Database/frontend/Worker source: 1.4.9; current assets v1409; immediate JavaScript bridge v1408.
- New-submission floor remains VulkanScope 2.0.6+ · schema 2 / technical report 3. Registry/header remains Vulkan 1.4.364 / 364.
- Static preload remains deployment-time fast-start/fallback data; live `/v1/sync` delta ingestion is the automatic path for reports submitted after page load. No per-report Pages deployment is required.
- D1 migration: none. Normalizer: 16 unchanged. Stored payload/hash rewrite: forbidden.
- Live Cloudflare Worker deployment remains a separate evidence class and is not implied by source/package verification.

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
