# VulkanScope Database 1.4.4 build / regression audit

Database 1.4.4 succeeds immutable Database 1.4.3 (ZIP SHA-256 `07d258de359c8fbde49738bbb1799f8f125f4a217f580461a665ce0908d5fa52`). D1 schema/migrations, stored report bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362, validated browser floors and the VulkanScope 1.4.0 new-submission floor are unchanged.

The UI-only repair removes containing-block creation from the startup `#appRoot` reveal so fixed page-scroll chrome is again viewport-relative. The current stylesheet is cache-busted as `assets/site.v1404.css`; current JS/bootstrap/browser-gate assets use the matching 1404 identity and retain 1403 as the immediate deployment bridge.

- Database / frontend / Worker: 1.4.4
- Current app: `assets/app.v1404.js`
- Current browser gate: `assets/browser-compat.v1404.js`
- Current release bootstrap: `assets/release-bootstrap.v1404.js`
- Current stylesheet: `assets/site.v1404.css`
- Cache key: 1404
- Immutable predecessor: 1.4.3

`tools/quality_gate.py` verifies the immutable 1.4.3 boundary, focused viewport-scroll/progress contract and negative mutations, source audit, JavaScript/Worker checks, D1 replay, Pages allow-list staging and release-ready transition. Deterministic packaging repeats strict verification against a clean extraction.
