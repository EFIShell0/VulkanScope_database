# VulkanScope Database 1.4.3 build / regression audit

Database 1.4.3 succeeds immutable Database 1.4.2 (ZIP SHA-256 `29dbf337d2305dfc1d898bd0dc8279f287af7ce06444bae7c22e613267e226f6`). D1 schema/migrations, stored report bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362, validated browser floors and the VulkanScope 1.4.0 new-submission floor are unchanged.

## Release corrections

- Removes the `database-loading` class-name collision between the `<body>` runtime state and the visual loading panel. The loading surface now uses `database-loading-panel`, preventing body-level flex/padding/border styles from corrupting first paint.
- During `startup-layout-hold`, pins the Database loading panel to the viewport center with bounded viewport width/height on desktop and mobile. The rest of the application shell remains non-paintable until the first report-backed render.
- Gives every observed address row a full-width responsive row. Revealed IPv4/IPv6 values use safe wrapping rather than ellipsis/nowrap clipping, while the mosaic remains opaque and the Show/Hide control stays reachable.
- Retains independent Active/IPv4/IPv6/Pseudo IPv4 reveal slots, automatic remasking, keyboard focus and reduced-motion behavior.
- VulkanScope 1.4.0+ remains the POST floor; historical lower-version reports remain GET-readable.

## Release identity

- Database / frontend / Worker: 1.4.3
- Current app: `assets/app.v1403.js`
- Current browser gate: `assets/browser-compat.v1403.js`
- Current release bootstrap: `assets/release-bootstrap.v1403.js`
- Current stylesheet: `assets/site.v1403.css`
- Cache key: 1403
- Immediate JavaScript bridge: v1402 triplet

## Verification

`tools/quality_gate.py` runs repository repair/check, immutable 1.4.2 regression verification, the 1.4.3 focused verifier and negative mutations, source audit, JavaScript/Worker checks, D1 replay, Pages allow-list staging and release-ready transition audit. Deterministic packaging repeats strict regression/source/release verification against a clean extraction.
