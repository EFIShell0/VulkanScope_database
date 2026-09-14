# VulkanScope Database 1.3.9 build / regression audit

Database 1.3.9 is a presentation-only successor to immutable Database 1.3.8 (ZIP SHA-256 `2a5ea00208403d2fb823eab4725669447d8052281a29277d86c95f74570b4abe`). D1 schema/migrations, stored report payload bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362, VulkanScope 1.2.5 submission floor and validated browser floors are unchanged.

## Release focus

- Regional settings controls use the full available settings width and no longer force long labels such as Automatic (browser / system) into a narrow split column.
- Regional mode remains Automatic / Country / Manual. Automatic locks every regional override; Country enables only Country / region; Manual locks Country / region to Browser / system region while enabling Date format, Clock format, Time zone and Seasonal offset.
- Entering Manual clears any prior country override, so Manual cannot silently inherit country-derived locale behavior.
- Country mode now renders a separate presentation profile for the selected country: date pattern, clock format, representative IANA zone, current UTC offset, standard/winter offset, daylight/summer offset, seasonal clock-change status and current offset state. These are display preferences only and do not mutate stored/server timestamps.
- Filter/custom-select scrollbar gutter is demand-driven. A rail and its reserved width exist only for real overflow; non-overflowing lists use the entire menu width. Long option labels wrap vertically and remain fully readable with or without a scrollbar.

## Release identity

- Database / frontend / Worker: 1.3.9
- Current app: `assets/app.v1309.js`
- Current browser gate: `assets/browser-compat.v1309.js`
- Current release bootstrap: `assets/release-bootstrap.v1309.js`
- Current stylesheet: `assets/site.v1309.css`
- Cache key: 1309
- Immediate cache bridge: immutable 1.3.8 JS triplet
- New D1 migration: none

## Gates

`tools/quality_gate.py` runs repository repair/check, immutable 1.3.8 regression verification, the 1.3.9 regional/filter layout-profile verifier and negative mutations, source audit, JavaScript/Worker checks, D1 migration replay, Pages allow-list staging and release-ready audit. Deterministic packaging repeats strict regression/source/1.3.9 verification against a clean extraction.
