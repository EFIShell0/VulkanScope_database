# VulkanScope Database 0.39.20 build / regression audit

Immutable predecessor: VulkanScope Database 0.39.19 ZIP SHA-256 `91e059a52264d5ab1c95ccd8cea9e84925a1a8b12987d2d0b05a0a124af59c7f`. Current producer/query baseline: VulkanScope 0.41.45 / versionCode 455; Vulkan registry 1.4.361; schema 2 / technicalReport 3; normalizer 16.

0.39.20 updates only Pages/Worker/static-index producer identity and cache-busts the local frontend asset to `app.v03920.js`. VulkanScope 0.41.45 changes application-side Vulkan Video capability collection but preserves the Database submission envelope and technicalReport schema. No report normalization, Compare evidence semantics, Worker validation, D1 payload/hash behavior or migration changes are introduced.

Failing-before-fix: `tools/test_producer_baseline_04145.mjs <immutable 0.39.19>` fails. The successor verifier and negative-mutation test pass on 0.39.20 with an unrelated generated-state false-positive control.

Source/full gate and final extracted-package evidence are recorded at packaging. Live Cloudflare deployment/runtime smoke remains a separate evidence class and is NOT EXECUTED by the packaging environment.
