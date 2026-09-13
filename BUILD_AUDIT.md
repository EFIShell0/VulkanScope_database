# VulkanScope Database 1.2.8 build / regression audit

- Immutable predecessor: VulkanScope Database **1.2.7** (`dd18283170e04a6db697e7ad8816fb08376204d0814c1ffe26e0c86c72ea01fb`).
- Database/frontend/Worker release identity: **1.2.8**.
- Frontend identity: `assets/app.v1208.js`, browser gate `assets/browser-compat.v1208.js`, cache key **1208**.
- Compare follow control uses an explicit viewport-fixed pin with a flow placeholder once its sentinel passes the navigation boundary; it does not depend on ancestor-sensitive CSS sticky behavior.
- Baseline/Candidate custom selector menus remain overflow-visible and elevated above the fixed comparison workspace.
- D1 schema, stored payload bytes/hashes, report IDs, normalizer 16, Vulkan 1.4.362 and VulkanScope 1.2.5 new-submission floor are unchanged.
- Mandatory gates: current 1.2.8 verifier + negative mutations, immutable 1.2.7 regression contract, Worker transport contract, source audit, D1 migration replay, Pages release-ready transition, clean-extract verification and deterministic byte-identical ZIP construction.
