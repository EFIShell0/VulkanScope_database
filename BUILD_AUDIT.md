# VulkanScope Database 0.39.11 Build / Release Audit

- Database: 0.39.11.
- Current VulkanScope producer baseline: 0.41.13 / 423.
- Vulkan producer/query baseline: 1.4.360.
- Submission schema: 2; technicalReport: 3; normalizer: 16.
- Compatibility floor: VulkanScope 0.32.4+.
- D1 migration: none.
- Stored payload/hash rewrite: none.

## HTTP 400 root cause and correction

Database 0.39.10 unconditionally required the 0.41.10+ complete Image Format Properties2 tuple ledger even when VulkanScope had explicitly completed the entire isolated Image Format Properties2 query group as Unavailable/Not applicable. That contradicted the producer's global complete-report rule and rejected a valid complete report with HTTP 400.

0.39.11 makes the tuple-ledger requirement conditional on an Available query-group result. Available retains all exact six-slot ledger, VkResult, prerequisite, property and aggregate-diagnostic checks. Explicit Unavailable/Not applicable is accepted only with no fabricated tuple/property/diagnostic evidence. Missing or contradictory state remains fail-closed.

For VulkanScope 0.41.13 the Worker additionally cross-checks structured `imageFormatQueryStatus` / `imageFormatQueryReason` against the existing query-status row. VulkanScope 0.41.12 remains compatible without these additive fields.

## Final gates

- canonical repository repair/check: PASS.
- source-tree audit: PASS.
- audit-hygiene regression: PASS.
- frontend JavaScript syntax: PASS.
- hash-route contract: PASS.
- Compare contract: PASS.
- Worker JavaScript syntax: PASS.
- Worker contract suite: PASS, including application-shaped available, group-Unavailable, group-Not-applicable, contradiction rejection and bounded validation-class cases.
- allow-listed Pages staging + artifact audit: PASS.
- no D1 migration required.
