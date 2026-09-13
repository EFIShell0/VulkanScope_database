# VulkanScope Database 1.2.6 build / regression audit

- Database/frontend/Worker release identity: **1.2.6**.
- Immutable predecessor: **1.2.5**, ZIP SHA-256 `3e0655b53840a7385979ae8f8bfb2473058dbbef8ef062d624438eabbf28f260`.
- Frontend identity: `assets/app.v1206.js`, browser gate `assets/browser-compat.v1206.js`, cache key **1206**.
- Cross-browser viewport scrollbar uses a local DOM rail; native endpoint-arrow pseudo-element state is no longer authoritative.
- Report detail exposes full 64-hex report identity and grouped Overview metadata.
- D1 schema/migrations, stored report payload bytes/hashes, normalizer 16, Vulkan 1.4.362 baseline and VulkanScope 1.2.5 new-submission floor remain unchanged.
- Mandatory gates: current 1.2.6 verifier + negative mutations, immutable 1.2.5 regression contract, Worker transport contract, source audit, D1 migration replay, Pages release-ready transition, clean-extract verification and deterministic byte-identical ZIP construction.
