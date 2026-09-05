# VulkanScope Database 0.39.25 source audit

## Release identity
- Database version: 0.39.25
- Immutable predecessor: VulkanScope Database 0.39.24
- Predecessor ZIP SHA-256: `73f9d9c72c8512957e2bdfb6e5e75f77c82548610c3f1947b9635b4915638155`
- Predecessor census: 196 files
- Producer/query baseline: VulkanScope 0.80.10 / Vulkan 1.4.362
- New-submission floor: VulkanScope 0.80.3
- Submission schema 2 / technicalReport 3 / normalizer 16
- D1 migration: none

## UI correction
- Reworked the immediate database loading surface to reuse the Database neutral panel, border, radius, typography and rose-accent system while retaining `role=status`, polite live-region behavior and truthful index/body progress.
- Reworked Encyclopedia presentation to use the same Database panel/card, badge, notice, search and typography language instead of a separate red-gradient/pill subsystem.
- Encyclopedia census is presented with Database-style compact stat cards. Evidence semantics remain in the shared notice language.
- No nested vertical Encyclopedia scroller was added; global page-scroll controls remain authoritative.
- Main CSS/JS presentation is cache-busted for 0.39.25.

## Unchanged technical contract
- Locked Vulkan registry remains Vulkan 1.4.362 / header 362 / SHA-256 `cf31c965cf6e788697139601da0c7e02a75a9b6c7ac764e7641f5521ffd9da06`.
- Encyclopedia corpus remains exactly 842 commands / 6248 VK_* tokens / 2461 Vk* types / 476 extensions / 50 VkResult entries.
- Search categories, two-character large-family threshold and 24-result visible bound are unchanged.
- Registry/reference presence remains separate from runtime capability evidence, including the Vulkan Video Not applicable clarification.
- Worker validation, D1 schema/data, report hashes, payload chunking and historical report readability are unchanged.

## Verification
- 0.39.24 -> 0.39.25 immutable-predecessor regression contract: PASS in source-overlay mode.
- Source audit: PASS.
- Loading/scroll/floor, Encyclopedia state machine and negative mutations: PASS.
- Vulkan 1.4.362 verifier and negative mutations: PASS.
- 0.39.25 UI-coherence verifier and negative mutations: PASS.
- Aggregate quality gate reached and passed all retained application/registry/frontend gates through the Vulkan 1.4.362 negative-mutation suite before the execution wrapper time limit. Remaining Worker/D1/Pages/strict-package constituents are executed separately; the timed-out aggregate invocation itself is not labeled PASS.
- Live Cloudflare Pages/Worker/D1 deployment is not executed by this packaging environment.
