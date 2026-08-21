# VulkanScope Database 0.35.7 build audit

## Scope
Full application/database compatibility, data correctness, specification provenance, frontend reliability and Worker security audit against VulkanScope 0.33.7.

## Key findings fixed
- Missing aggregate fields could disappear from property/limit/feature denominators instead of remaining Unknown.
- Missing format rows likewise had no Unknown representation.
- Display/HDR inferred state only from `hdrTypes`, so truly missing evidence could be mislabeled Unavailable and explicit producer status was ignored.
- Browser API reads had no timeout or response-size ceiling and did not detect a repeated cursor.
- Worker accepted structurally shallow schema-v2 submissions without cross-checking current schema-v3 primary-device metadata or current report-text identity.
- Public specification notes still referenced Vulkan 1.4.358; current published Vulkan specification is 1.4.359 (2026-08-07). The VulkanScope 1.4.360 producer/query staging baseline remains separate.

## Preserved invariants
- Supported / Unsupported / Available / Unavailable / Unknown remain distinct.
- Enumerated extension absence is not fabricated as Unsupported.
- Exact-width U64 strings remain preferred for unsafe-width masks.
- Raw report text remains accessible.
- Request IP data is not stored.
- Production Worker/D1 account pins remain unchanged.
- No D1 migration or stored report rewrite is required.

## Validation
- Frontend JavaScript syntax: PASS.
- Worker JavaScript syntax: PASS.
- JSON schema parse: PASS.
- Current VulkanScope 0.33.7 submission contract fixture: PASS.
- Cross-field mismatch rejection: PASS.
- Sensitive-key rejection: PASS.
- Wrong Content-Type rejection: PASS.
- 2 MiB request bound: PASS.
- Version/cache references: PASS.
- ZIP integrity: PASS.
