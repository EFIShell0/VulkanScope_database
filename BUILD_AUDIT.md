# VulkanScope Database 1.4.5 build / regression audit

Database 1.4.5 succeeds immutable Database 1.4.4 (ZIP SHA-256 `ae6fa79be8ec23c0aaa1e4245cb375cb02707d9d92979d92df86f7e4d822f6d6`). D1 schema/migrations, stored report bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362, validated browser floors and the VulkanScope 1.4.0 new-submission floor are unchanged.

This interaction-only release makes observed IP address rows non-interactive except for the explicit Show/Hide button and adds a shared animated X clear action to every enhanced searchable filter/listbox. Existing global/Encyclopedia/row-search clear controls, independent address slots, responsive address fit, startup-loader isolation and viewport-fixed scroll chrome remain regression-protected.

- Database / frontend / Worker: 1.4.5
- Current app: `assets/app.v1405.js`
- Current browser gate: `assets/browser-compat.v1405.js`
- Current release bootstrap: `assets/release-bootstrap.v1405.js`
- Current stylesheet: `assets/site.v1405.css`
- Cache key: 1405
- Immutable predecessor: 1.4.4

`tools/quality_gate.py` verifies the immutable 1.4.4 boundary, focused action-only address/filter-clear contract and negative mutations, source audit, JavaScript/Worker checks, D1 replay, Pages allow-list staging and release-ready transition. Deterministic packaging repeats strict verification against a clean extraction.
