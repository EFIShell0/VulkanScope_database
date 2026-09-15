# VulkanScope Database 1.4.1 build / regression audit

Database 1.4.1 succeeds immutable Database 1.4.0 (ZIP SHA-256 `c50af2d9597a86a81f6a24c6f1a9208be3bae325a7a9cf1d62894deaf94322ca`). D1 schema/migrations, stored report bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362, validated browser floors and the VulkanScope 1.4.0 new-submission floor are unchanged.

## Release corrections

- Active address, IPv4, IPv6 and Pseudo IPv4 now own independent privacy reveal state; revealing one row cannot reveal a duplicate address row.
- The address privacy control uses an opaque grid mosaic, blurred hidden text, local eye icon and compact Show/Hide action with smooth reveal/remask motion plus reduced-motion support.
- Closing Settings, leaving Internet or changing an observed address remasks the relevant controls according to the 1.4.1 rules.
- The report filter workspace is parse-time suppressed with `body.database-loading` and remains hidden until the first report-backed render completes, eliminating the old pre-grouped filter flash during preload/report construction.
- VulkanScope 1.4.0+ remains the POST floor; historical lower-version reports remain GET-readable.

## Release identity

- Database / frontend / Worker: 1.4.1
- Current app: `assets/app.v1401.js`
- Current browser gate: `assets/browser-compat.v1401.js`
- Current release bootstrap: `assets/release-bootstrap.v1401.js`
- Current stylesheet: `assets/site.v1401.css`
- Cache key: 1401
- Immediate bridge: v1400 JS triplet + `site.v1400.css`

## Verification

`tools/quality_gate.py` runs repository repair/check, immutable 1.4.0 regression verification, the 1.4.1 focused verifier and negative mutations, source audit, JavaScript/Worker checks, D1 replay, Pages allow-list staging and release-ready transition audit. Deterministic packaging repeats strict regression/source/release verification against a clean extraction.
