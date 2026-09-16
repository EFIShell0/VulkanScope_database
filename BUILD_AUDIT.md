# VulkanScope Database 1.4.2 build / regression audit

Database 1.4.2 succeeds immutable Database 1.4.1 (ZIP SHA-256 `76888732b4e64273f9a0d0df9d45305577b28a242b1d4aca1bd75c83da875bf7`). D1 schema/migrations, stored report bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362, validated browser floors and the VulkanScope 1.4.0 new-submission floor are unchanged.

## Release corrections

- Adds a parse-time `startup-layout-hold` that keeps incomplete navigation, hero, metrics, content, detail, footer and scroll chrome out of the first visible layout while Database data is still being assembled.
- Keeps the centered Database loading surface visible and stable during that hold; the normal path releases the shell only after the first report-backed `render()`, while fatal startup releases before rendering the error state.
- Keeps the existing `database-loading` class as the separate owner of loading-panel/filter suppression so initial native/legacy filter geometry cannot flash.
- Refines observed IP privacy controls with a local shield/status mark, stronger opaque mosaic, family-specific IPv4/IPv6 accents and a compact eye Show/Hide action. Active/IPv4/IPv6/Pseudo IPv4 reveal slots remain independent.
- Keeps remasking on Settings/Internet exit and on changed observations, and keeps reduced-motion behavior privacy-equivalent.
- VulkanScope 1.4.0+ remains the POST floor; historical lower-version reports remain GET-readable.

## Release identity

- Database / frontend / Worker: 1.4.2
- Current app: `assets/app.v1402.js`
- Current browser gate: `assets/browser-compat.v1402.js`
- Current release bootstrap: `assets/release-bootstrap.v1402.js`
- Current stylesheet: `assets/site.v1402.css`
- Cache key: 1402
- Immediate JavaScript bridge: v1401 triplet

## Verification

`tools/quality_gate.py` runs repository repair/check, immutable 1.4.1 regression verification, the 1.4.2 focused verifier and negative mutations, source audit, JavaScript/Worker checks, D1 replay, Pages allow-list staging and release-ready transition audit. Deterministic packaging repeats strict regression/source/release verification against a clean extraction.
