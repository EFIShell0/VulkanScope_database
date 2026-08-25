# VulkanScope Database 0.39.7 Build / Release Audit

- Database: `0.39.7`
- Current VulkanScope producer baseline: `0.41.9` / `419`
- Published/query Vulkan baseline: `1.4.360`
- Submission schema: `2`
- `technicalReport`: `3`
- Normalizer: `15`
- D1 migration: none

## Image Format Properties2 outcome separation

Database 0.39.7 consumes VulkanScope 0.41.9's bounded `imageFormatQueryResults` dataset separately from normal detailed properties. Exact tuple-level Unsupported/Unavailable evidence remains comparable under the same canonical Image Format Properties2 key, but Properties & Limits aggregation does not count these non-success tuple outcomes as property/query rows. Historical 0.41.8 embedded tuple-state reports remain readable and accepted under their older producer contract.

## Final source-tree gates

- `python tools/audit_database.py --source-tree .`: PASS.
- `node --check assets/app.v0397.js`: PASS.
- `node tools/test_routes.mjs`: ALL PASS.
- `node tools/test_compare_contract.mjs`: ALL PASS.
- `node --check worker/src/index.js`: PASS.
- `node worker/tests/contract.mjs`: ALL PASS.
- `python tools/test_audit_hygiene.py`: ALL PASS.
- `python tools/repair_repository.py --check`: PASS.
- Canonical Pages staging plus `--artifact-tree` audit: PASS.

Worker validation is fail-closed for 0.41.9+ tuple names, uniqueness, semantic state and numeric `VkResult`, while schema 2 / technicalReport 3 / normalizer 15 and existing D1 storage remain unchanged.
