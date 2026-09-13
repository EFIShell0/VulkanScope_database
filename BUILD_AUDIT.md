# VulkanScope Database 1.2.5 build / regression audit

- Database/frontend/Worker release identity: **1.2.5**.
- Immutable predecessor: **VulkanScope Database 1.2.4**, ZIP SHA-256 `123938b1b2517f7939b58350ab12963c6807cef7d0fbab38ba67e9c1e420a606`.
- Frontend identity: `assets/app.v1205.js`, browser gate `assets/browser-compat.v1205.js`, cache key **1205**.
- Fixed the far-right viewport scrollbar endpoint styling at the actual root-scrollbar layer. Endpoint state is mirrored to both `html` and `body`; at the document top the UP arrow is gray, while at the document bottom the DOWN arrow retains the requested Vulkan red presentation.
- Repaired the 1.2.3 CSS serialization defect where literal `\n` tokens caused the endpoint/motion/mobile block to parse as an invalid qualified rule. The stylesheet now contains real newlines and is regression-guarded against recurrence.
- Motion audit: primary navigation, tabs, buttons, links, options, cards, report rows, table controls, filters, Settings surfaces, modals, Compare, Surface, Encyclopedia, detail transitions and destructive confirmation close paths use the shared short opacity/transform/color/border/shadow language, with reduced-motion fallbacks.
- 1.2.4 bounded identity-table paging remains unchanged.
- D1 schema/migrations, stored report payload bytes/hashes, report IDs, schema 2, technical report 3, normalizer 16, Vulkan 1.4.362 baseline and VulkanScope 1.2.5 new-submission floor remain unchanged.
- Mandatory gates: current 1.2.5 verifier + negative mutations, immutable 1.2.4 regression contract, Worker transport contract, source audit, D1 migration replay, Pages release-ready transition, clean-extract verification and deterministic byte-identical ZIP construction.
