# VulkanScope Database 1.3.7 build / regression audit

## Scope

Database 1.3.7 is a Browser information presentation-only successor to immutable Database 1.3.6 (ZIP SHA-256 `864e515dffa51d59ab9bf6b790b96a8bfea791cd782408b283df7264de8d22b8`). D1 schema/migrations, stored report payload bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362, VulkanScope 1.2.5 submission floor and validated browser floors are unchanged.

## Browser information marks

The Browser information summary uses locally bundled, original-color marks for browser identities that can be explicitly distinguished: Google Chrome, Chromium, Microsoft Edge, Firefox, Safari, Opera, Brave, Vivaldi and Samsung Browser. Unknown or ambiguous Chromium-family identity keeps the neutral globe rather than receiving a potentially false product mark.

Samsung's displayed product name follows the current Samsung Browser branding. Brave/Vivaldi recognition is best-effort from browser-exposed signals only. No canvas/WebGL fingerprinting primitive, favicon resolver, logo CDN, third-party JavaScript, analytics request or external logo fetch was introduced.

The logo wrapper is neutral and `.settings-browser-logo` has no CSS colorization/filter. `licenses/browser-marks.md` records official vendor reference pages and trademark/non-affiliation notes.

## Release identities

- Database / frontend / Worker: 1.3.7
- Current app: `assets/app.v1307.js`
- Current browser gate: `assets/browser-compat.v1307.js`
- Current release bootstrap: `assets/release-bootstrap.v1307.js`
- Cache key: 1307
- Immediate CDN transition bridge: immutable 1.3.6 app/browser/bootstrap triplet only
- Immutable predecessor ZIP: Database 1.3.6, SHA-256 `864e515dffa51d59ab9bf6b790b96a8bfea791cd782408b283df7264de8d22b8`

## Mandatory release gates

`tools/quality_gate.py` runs repository repair/check, immutable 1.3.6 regression verification, the 1.3.7 browser-brand verifier and negative mutations, source audit, JavaScript/Worker checks, D1 migration replay, Pages allow-list staging and release-ready audit. Deterministic packaging repeats strict regression/source/1.3.7 verification against a clean extraction.
