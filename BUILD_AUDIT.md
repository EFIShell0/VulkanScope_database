# VulkanScope Database 1.2.4 build / regression audit

- Database/frontend/Worker release identity: **1.2.4**.
- Immutable predecessor: **VulkanScope Database 1.2.3**, ZIP SHA-256 `e93a67fa86a0070b3aba5ba93b1695a60b83cdefc6d557ad7dff674c6607382e`.
- Frontend identity: `assets/app.v1204.js`, browser gate `assets/browser-compat.v1204.js`, cache key **1204**.
- CI fix: canonical Windows/build/release verification calls the current 1.2.4 verifier and negative suite; no 1.2.2 release-identity verifier is used against generated 1.2.4 metadata.
- Bounded identity tables: Devices, Versions, Memory heaps/per-report types, Queues, Surface formats/presentation queues, Display & HDR, Portability and Statistics GPU models. Pagination is 10/25/50 and slices only rendered rows after complete filtering/aggregation.
- Inherited protections: fail-closed GitHub Release tag ownership + bounded transient retry, browser floors Chromium 84+/Firefox 86+/Safari 14.1+, English UI locale, reduced-motion, endpoint scrollbar state, mobile overflow containment, live sync and VulkanScope 1.2.5 submission floor.
- D1 schema/migrations, stored report payload bytes/hashes, report IDs, schema 2, technical report 3, normalizer 16 and Vulkan 1.4.362 registry baseline are unchanged.
- Mandatory gates: current 1.2.4 verifier + negative mutations, immutable 1.2.3 regression contract, Worker transport contract, source audit, D1 migration replay, Pages release-ready transition, clean-extract verification and deterministic byte-identical ZIP construction.
