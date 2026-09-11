# VulkanScope Database 1.0.10 build / regression audit

## Release identity
- Immutable predecessor: VulkanScope Database 1.0.9
- Predecessor ZIP SHA-256: `0d75cfe949901636635a1039ac53921834fe690be7099ad96d45ef14a4ee6517`
- Current producer/query baseline: VulkanScope 1.0.19 / versionCode 1019 / Vulkan 1.4.362
- New-submission floor: VulkanScope 1.0.19
- Submission schema 2 / technicalReport 3 / normalizer 16
- D1 migration: none

## Corrected failure class
Database 1.0.9 prematurely serialized Reports rows with `rs.map(...).join('')` and then passed the resulting string to `table()`. The shared table helper owns row serialization and therefore called `rows.join('')` on that string, producing the observed `rows.join is not a function` error and the misleading Database unavailable view.

1.0.10 keeps the Reports mapping as an Array through `table(..., rows)`. The shared helper remains strict; it is not made permissive to hide type-contract regressions.

## Retained behavior
The 1.0.9 atomic live reconciliation path, one committed report Map for all statistics, submission Date/Time/Time-zone presentation, full Report ID copy control, low/very-low coverage treatment and VulkanScope 1.0.19 submission floor are unchanged. Worker/D1 report semantics and storage are unchanged.

## Required evidence
- `tools/verify_1_0_10_reports_render_hotfix.py`: current release/type-contract verification.
- `tools/test_1_0_10_reports_render_hotfix_negative_mutations.py`: reintroduces the exact premature `.join('')` mutation and requires the verifier to reject it.
- JavaScript syntax, Worker contract, D1 migration-chain replay, Pages allow-list staging, immutable predecessor regression and clean-extract strict-package verification remain mandatory.
- Live Cloudflare Pages/Worker deployment and production D1 smoke testing are not claimed by this offline package.
