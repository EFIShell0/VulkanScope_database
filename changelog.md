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
