# VulkanScope Database 0.39.14

- Fixes regression-gate false positives when a release is overlaid onto the real long-lived Git repository containing historical source/audit/assets that were not shipped in the predecessor release ZIP.
- Adds explicit source-overlay and strict-release-package regression modes: predecessor-owned files remain hash-protected in both, while only strict-package mode rejects unrelated source-history files.
- Treats generated `data/index.json` as semantic generated state so `build_index.py` no longer invalidates the predecessor contract merely by regenerating metadata/report inventory.
- Adds an existing-repository fixture covering historical extras, stale app repair, generated-index regeneration, strict-package rejection and immutable predecessor mutation detection.
- Cache-busts the frontend to `app.v03914.js` for release identity only; Worker/D1/API behavior is unchanged from 0.39.13.
- Preserves VulkanScope 0.41.32 / Vulkan 1.4.361, schema 2 / technicalReport 3, normalizer 16, D1 payload chunking and the 2 MiB non-truncating transport limit without a new migration.

# VulkanScope Database 0.39.13

- Fixes the Windows Python quality-gate crash caused by implicit CP1252 decoding of UTF-8 repository assets.
- Makes every Python `Path.read_text` / `Path.write_text` operation in release tooling encoding-explicit and reads D1 migrations as UTF-8.
- Adds a permanent regression test that proves the real frontend asset fails CP1252, succeeds UTF-8, and the VulkanScope 0.41.32 compatibility verifier completes successfully.
- Runs the UTF-8 determinism test both directly in the Pages workflow and inside the aggregate quality gate.
- Cache-busts the frontend as `app.v03913.js` only to publish the 0.39.13 Database release identity; capability, normalization and API behavior are unchanged.
- Preserves VulkanScope 0.41.32 / Vulkan 1.4.361, schema 2 / technicalReport 3, normalizer 16, D1 chunk storage, 2 MiB transport, report hashes and existing stored data without a new migration.

# VulkanScope Database 0.39.12

- Adds verified VulkanScope 0.41.32 compatibility while preserving submission schema 2, technicalReport 3 and normalizer 16.
- Advances the canonical producer/query baseline to Vulkan 1.4.361 and locks the packaged `vk.xml` snapshot by SHA-256.
- Accepts and cross-checks the additive 0.41.24+ multi-device summary provenance fields that 0.39.11 incorrectly rejected as unexpected keys.
- Enforces authoritative 0.41.18+ complete-report markers and 0.41.24+ physical-device enumeration completeness before accepting current reports.
- Enforces the 0.41.32 registry-coverage contract, including `VkPhysicalDevicePrivateDataBaseHandleFeaturesNV`.
- Preserves the producer's 2 MiB non-truncating transport contract despite D1's 2,000,000-byte single-row value limit by adding atomic payload chunk storage for large canonical reports.
- Switches request-body decoding to bounded incremental strict UTF-8, avoiding a second full raw-byte buffer and rejecting malformed byte sequences.
- Adds a compact report-detail path used by the frontend to avoid duplicating normalized large arrays inside Worker memory; the legacy expanded detail response remains available.
- Adds negative/current/historical, large-payload reconstruction and concurrent-idempotency contract tests plus registry/producer/regression quality gates.
- Requires D1 migration `0003_payload_chunks.sql`; existing inline report rows require no rewrite.

# VulkanScope Database 0.39.11

- Fixed HTTP 400 rejection of complete VulkanScope 0.41.12 reports when the isolated Image Format Properties2 query group explicitly finishes as Unavailable or Not applicable before tuple evidence can be produced.
- Keeps the complete six-slot Image Format Properties2 tuple ledger mandatory whenever that query group is Available.
- Rejects contradictory unavailable-group reports that also contain tuple, successful property or aggregate diagnostic evidence.
- Adds bounded validation-class text to HTTP 400 schema rejections for deterministic producer/Worker diagnosis.
- Advances the current producer baseline to VulkanScope 0.41.13 / 423 while keeping VulkanScope 0.41.12 / 422 compatible with the corrected query-group contract.
- Preserves schema 2, technicalReport 3, normalizer 16, Vulkan 1.4.360, existing D1 records and the 0.39.10 canonical ASTC format-token fix; no migration is required.

# VulkanScope Database 0.39.10

- Fixed valid Vulkan Image Format Properties2 submissions being rejected when canonical `VK_FORMAT_ASTC_*` names contain the registry-defined lowercase `x` dimension separator.
- Advanced the current producer baseline to VulkanScope 0.41.12 / 422 while preserving schema 2, technicalReport 3, normalizer 16 and existing D1 data without migration.

# VulkanScope Database 0.39.9

- Corrected zero-mask, format-mask, Not applicable and Compare state semantics for VulkanScope 0.41.11.
- Advanced normalizer to 16 and current producer baseline to VulkanScope 0.41.11 / 421 without a D1 migration.

# VulkanScope Database 0.39.8

- Adds native support for VulkanScope 0.41.10's complete bounded Image Format Properties2 tuple-state ledger.
- Eliminates ambiguous current-producer `Not reported` holes for scheduled base, OPAQUE_FD and Android Hardware Buffer tuples by requiring exactly six canonical slots per scheduled format.
- `AVAILABLE` requires `VkResult=0` plus the matching successful full property payload; the ledger never replaces that full value.
- `UNSUPPORTED` remains exact `VK_ERROR_FORMAT_NOT_SUPPORTED` (-11); other non-zero results remain `UNAVAILABLE`.
- Missing external-memory prerequisites are represented explicitly as `NOT APPLICABLE` with null `VkResult` and an exact reason, never inferred Unsupported.
- Worker validation cross-checks tuple counts/states against the fixed query recipe and aggregate query diagnostics and rejects missing, duplicate, malformed or contradictory current-producer evidence.
- The complete tuple ledger remains excluded from Properties & Limits totals; Compare overlays only non-available states under the canonical tuple identity.
- Historical VulkanScope 0.41.9 separated outcomes and 0.41.8 embedded negative tuple evidence remain compatible.
- Current producer baseline is VulkanScope 0.41.10 / 420; schema 2, technicalReport 3, normalizer 15, Vulkan 1.4.360 and D1 storage remain unchanged.
