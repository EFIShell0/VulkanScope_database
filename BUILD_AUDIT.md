# VulkanScope Database 1.0.22 build / regression audit

## Release scope
- Immutable predecessor: VulkanScope Database 1.0.21, SHA-256 `0f1619965c0b3bb6eaf2f81a17c4436312c2d71801c82484a75b1d0f23eb9aa1`.
- Frontend identity: `assets/app.v1022.js`, cache key 1022.
- Worker identity: 1.0.22; D1 migrations unchanged.
- Producer/query baseline remains VulkanScope 1.0.19 / Vulkan 1.4.362.

## Mandatory release gates
- 1.0.21 -> 1.0.22 immutable predecessor regression contract.
- 1.0.22 atomic-current-set / Settings / Favorites / selection-safety verifier and negative mutations.
- Worker transport contract including `/v1/network-info`.
- Source audit, Vulkan registry/producer compatibility tests and deterministic strict-package clean-extract verification.
- Pages allow-list plus release-ready marker transition audit.

## Privacy / data integrity
Favorites and UI preferences are local browser state. `/v1/network-info` is request-scoped/no-store and never touches D1. Report payloads, hashes, schema and statistics are not modified by these features.
