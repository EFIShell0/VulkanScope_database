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
