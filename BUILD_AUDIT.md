# VulkanScope Database 0.35.9 build audit

## Scope
Properties/Limits semantic parity audit against VulkanScope 0.33.10, with regression checks for Worker normalization and frontend classification.

## Fixed
- Properties no longer uses the broad TXT-normalized capability collection.
- DEVICE and Surface metadata cannot inflate Properties.
- Limits no longer relies on `Limits|Sparse Properties` section-name heuristics.
- Schema-v3 structured `detailedProperties` and `limits` arrays are authoritative.
- TXT compatibility fallback builds dedicated property/limit arrays without merging their semantics.
- Detail-tab counts and aggregate views consume the same authoritative datasets.

## Preserved
- Raw TXT remains available.
- Compare retains the broader compatibility capability collection.
- Supported / Unsupported / Available / Unavailable / Unknown semantics are unchanged.
- Missing aggregate evidence remains Unknown.
- Cloudflare account/D1 pins, CORS/CSP/privacy/body bounds and cursor/detail-fetch limits are unchanged.
- No D1 migration or stored-payload rewrite.

## Validation
- Frontend JavaScript syntax: PASS.
- Worker JavaScript syntax: PASS.
- Worker contract tests: PASS.
- Structured Properties authority regression: PASS.
- Structured Limits authority regression: PASS.
- DEVICE/SURFACE contamination regression: PASS.
- JSON schema parse: PASS.
- Static database audit: PASS.
- ZIP integrity: PASS.
