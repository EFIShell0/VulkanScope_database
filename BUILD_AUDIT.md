# VulkanScope Database 1.2.1 build / regression audit

- Database/frontend/Worker release identity: **1.2.1**.
- Frontend identity: `assets/app.v1201.js`, cache key **1201**; stylesheet cache key also **1201**.
- Immutable predecessor: VulkanScope Database **1.2.0**, ZIP SHA-256 `b3768a0997e87589ce4358df448018daf5befdd8932ec0363436120b72b2132c`.
- D1 schema/migration chain, report payload bytes/hashes, normalizer **16**, Vulkan registry **1.4.362/header 362** and historical report readability are unchanged.
- New report POST floor remains VulkanScope **1.2.5 / versionCode 1205**.
- Compare has a natural-top full workspace and a smooth compact sticky tracking state for long comparisons; selected reports/toggles/filters are not rewritten by the sticky state.
- Page scrolling uses a wider Database-styled vertical scrollbar and persistent endpoint-aware up/down controls with the unavailable direction disabled.
- `navigator.connection.effectiveType` is labelled only as a browser effective performance class; it is explicitly not treated as LTE/5G/FTTH/Wi-Fi physical-access evidence.
- Regional date/time settings remain presentation-only. Submission sorting and submission-age filtering consume the original server timestamp through `submissionEpoch()`.
- Removing a Favorite and clearing saved browser data require an accessible in-product destructive-action confirmation; adding Favorites remains immediate.
- Report-detail tab synchronization was restored by defining `syncDetailTabUi()`, keeping ARIA/tabindex state coherent and allowing the detail body to render/switch normally.
- Mandatory gates: immutable 1.2.0→1.2.1 regression contract, 1.2.1 verifier + negative mutations, Worker transport contract, source audit, D1 migration replay, Pages release-ready transition, clean-extract strict-tree audit and deterministic ZIP construction.
