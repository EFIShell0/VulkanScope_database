# VulkanScope Database 1.4.0 build / regression audit

Database 1.4.0 succeeds immutable Database 1.3.10 (ZIP SHA-256 `3f9932e9661ec93398c6a608234597c1c1fbf20ab2a97bf93dd87364ffdf3581`). D1 schema/migrations, stored report bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362 and validated browser floors are unchanged. The new-report producer floor intentionally advances from VulkanScope 1.2.5 to VulkanScope 1.4.0.

## Release focus

- Enforce VulkanScope 1.4.0+ only for new POST submissions while retaining historical GET readability.
- Order Settings as Favorites, Preferences, Internet, Information.
- Start observed IPv4/IPv6 values mosaicked; reveal/remask smoothly and reset concealment when leaving Internet/closing Settings or when an observed value changes.
- Keep unobserved address families unobserved rather than fabricating a second family.
- Hide the native filter panel in initial HTML so old filter controls cannot flash during report-set loading; normal render ownership reveals the enhanced filters afterward.
- Preserve the 1.3.10 searchable Country / region and Time zone 50-option paging contract.

## Release identity

- Database / frontend / Worker: 1.4.0
- Current app: `assets/app.v1400.js`
- Current browser gate: `assets/browser-compat.v1400.js`
- Current release bootstrap: `assets/release-bootstrap.v1400.js`
- Current stylesheet: `assets/site.v1400.css`
- Cache key: 1400
- Immediate JS cache bridge: immutable 1.3.10 triplet
- Immediate stylesheet bridge: `assets/site.v1309.css`
- New D1 migration: none

## Gates

`tools/quality_gate.py` runs repository repair/check, immutable 1.3.10 regression verification, the 1.4.0 focused verifier and negative mutations, source audit, JavaScript/Worker checks, D1 replay, Pages allow-list staging and release-ready transition audit. Deterministic packaging repeats strict regression/source/release verification against a clean extraction.
