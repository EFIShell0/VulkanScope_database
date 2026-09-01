# VulkanScope Database 0.39.18 build / regression audit

Immutable predecessor: VulkanScope Database 0.39.17 ZIP SHA-256 `3b1a8c62143e090ec827d7b965e125c0695f5122adb089119b9ce6254510e0bf`. Current producer/query baseline: VulkanScope 0.41.43 / versionCode 453; Vulkan registry 1.4.361; schema 2 / technicalReport 3; normalizer 16.

The demonstrated predecessor issue is stale current-producer metadata after the application advances to 0.41.43. 0.39.18 updates Pages/Worker/static-index producer identity and cache-busts the local frontend asset to `app.v03918.js`. No report normalization, Compare evidence semantics, Worker validation, D1 payload/hash behavior or migration changes are introduced.

Failing-before-fix: `tools/test_producer_baseline_04143.mjs <immutable 0.39.17>` fails. The successor verifier and negative-mutation test pass on 0.39.18 while retaining an unrelated generated-state false-positive control.

Database 0.39.17 Surface evidence-state Compare behavior, 0.39.16 historical property identity compatibility, strict UTF-8 handling, security/privacy constraints, route/Pages artifact gates, D1 migration chain and Worker contract remain mandatory.

Cloudflare Worker deployment and production runtime smoke tests are NOT EXECUTED by the packaging environment. No D1 migration is required.
