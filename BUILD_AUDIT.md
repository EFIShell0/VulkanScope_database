# VulkanScope Database 1.3.10 build / regression audit

Database 1.3.10 is a presentation-only successor to immutable Database 1.3.9 (ZIP SHA-256 `6f0180d5f53559f418b46b6e43aef66163c60ef768249ea9c7c51e3124edf059`). D1 schema/migrations, stored report payload bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362, VulkanScope 1.2.5 submission floor and validated browser floors are unchanged.

## Release focus

- Settings Country / region is explicitly part of the shared searchable custom-select family. Search runs over the complete native country/region option set before deterministic 50-option pagination.
- Country / region shows Previous/Next, direct numeric page entry and Go using the same one-page disabled-state contract as existing searchable filters.
- Opening the Country selector starts at browse page 1 while preserving the selected native value in the closed control. This removes the Türkiye-selected failure mode where the menu opened around Solomon Islands and earlier countries were unreachable because the pager was hidden.
- Search resets to page 1, country ordering remains English-display-name alphabetical, and native option selection remains the only path that mutates the selected country.
- Settings Time zone uses the same large-selector search/pagination opt-in so its full option set is reachable. Automatic/Country/Manual lock ownership, country profiles and all server timestamp semantics remain unchanged.

## Release identity

- Database / frontend / Worker: 1.3.10
- Current app: `assets/app.v1310.js`
- Current browser gate: `assets/browser-compat.v1310.js`
- Current release bootstrap: `assets/release-bootstrap.v1310.js`
- Current stylesheet: `assets/site.v1309.css` (unchanged)
- Cache key: 1310
- Immediate cache bridge: immutable 1.3.9 JavaScript triplet
- New D1 migration: none

## Gates

`tools/quality_gate.py` runs repository repair/check, immutable 1.3.9 regression verification, the 1.3.10 country-selector search/pagination verifier and negative mutations, source audit, JavaScript/Worker checks, D1 migration replay, Pages allow-list staging and release-ready audit. Deterministic packaging repeats strict regression/source/1.3.10 verification against a clean extraction.
