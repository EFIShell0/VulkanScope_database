# VulkanScope Database 1.3.3 build / regression audit

## Scope

Database 1.3.3 is a presentation-only successor to the immutable 1.3.2 source release (SHA-256 `77c611aa89f26c6f3de3ed09046f7f54d3c99b35e47f93df0e5ebb88798afa73`). It fixes Compare minimize/expand direction ownership and adds symmetric UI motion to the local License viewer plus filter/modal page changes. D1 schema/migrations, stored report bytes/hashes, normalizer 16, Vulkan 1.4.362/header 362, producer floor and browser floors are unchanged.

## Root cause and fix

The Compare helper already rewrote its SVG path according to state, but CSS also rotated the same SVG under `.is-minimized`. Those two state transformations cancelled each other, leaving a visually downward chevron in both states. 1.3.3 keeps JavaScript path geometry as the only direction owner: full/Minimize points down, minimized/Expand points up, and reset/unpin restores down.

License viewer visibility now uses symmetric opacity/transform transitions with a monotonic motion token so a stale close timer cannot hide a viewer that has already reopened. Searchable custom-selector pagination and bounded modal pagination use one short direction-aware compositor animation after state/DOM commit. Reduced-motion skips decorative motion while preserving final state, focus and keyboard/pointer semantics.

## Release identities

- Database / frontend / Worker: 1.3.3
- Current app: `assets/app.v1303.js`
- Current browser gate: `assets/browser-compat.v1303.js`
- Current release bootstrap: `assets/release-bootstrap.v1303.js`
- Cache key: 1303
- Immediate CDN transition bridge: 1.3.2 app/browser/bootstrap triplet only
- Immutable predecessor ZIP: Database 1.3.2, SHA-256 `77c611aa89f26c6f3de3ed09046f7f54d3c99b35e47f93df0e5ebb88798afa73`

## Mandatory release gates

`tools/quality_gate.py` runs repository repair/check, immutable regression verification, the 1.3.3 contract verifier, negative mutations, source audit, JavaScript syntax/Worker contract checks, D1 migration replay, Pages allow-list staging, and the release-ready transition audit. The packaging tool builds a deterministic ZIP and re-runs strict regression/source/1.3.3 verification against a clean extraction.

The 1.3.3 verifier specifically rejects double Compare chevron inversion, missing state-specific SVG geometry, absent filter/modal page motion, asymmetric License viewer state motion, missing reduced-motion handling, stale Pages predecessor bridging, release-identity drift and missing CI gates.
