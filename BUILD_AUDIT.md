# VulkanScope Database 1.3.8 build / regression audit

Database 1.3.8 is a presentation-only successor to immutable Database 1.3.7 (ZIP SHA-256 `1d58903dc5a8bf472022b59248c61d13af3a2bef3b6fbc21cdcad227e4010f49`). D1 schema/migrations, stored report payload bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362, VulkanScope 1.2.5 submission floor and validated browser floors are unchanged.

## Scope

- Browser information is text-only in the current frontend; the logo/icon host is removed. The immutable 1.3.7 browser-mark files remain only as one-release predecessor cache dependencies so a stale 1.3.7 document is not broken during propagation.
- Filter/custom-select labels wrap instead of clipping important values. One-page page-jump inputs and Go controls are disabled and removed from the tab order.
- Regional date/time presentation has Automatic / Country / Manual modes. Automatic follows browser/system locale/time-zone data; Country derives country conventions and a representative IANA zone while locking granular controls; Manual unlocks all overrides. Stored/server timestamps and sort/filter identity remain unchanged.

## Release identity

- Database / frontend / Worker: 1.3.8
- Current app: `assets/app.v1308.js`
- Current browser gate: `assets/browser-compat.v1308.js`
- Current release bootstrap: `assets/release-bootstrap.v1308.js`
- Current stylesheet: `assets/site.v1308.css`
- Cache key: 1308
- Immediate predecessor bridge: 1.3.7 JS triplet + predecessor browser-mark dependencies + immutable `site.v0390.css`

## Quality gates

`tools/quality_gate.py` runs repository repair/check, immutable 1.3.7 regression verification, the 1.3.8 regional/filter/browser-cleanup verifier and negative mutations, source audit, JavaScript/Worker checks, D1 migration replay, Pages allow-list staging and release-ready audit. Deterministic packaging repeats strict regression/source/1.3.8 verification against a clean extraction.
