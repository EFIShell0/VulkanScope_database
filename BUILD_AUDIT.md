# VulkanScope Database 1.0.25 build / regression audit

## Release identity
- Database/frontend release: **1.0.25**.
- Frontend identity: `assets/app.v1025.js`, cache key `1025`.
- Worker identity: `1.0.25`; D1 schema and migration chain are unchanged from 1.0.24.
- Immutable predecessor: VulkanScope Database 1.0.24, SHA-256 `d2cfde68221dbab5ceb461e14e4afcef1171de4747798a264d4db7ca2a575e27`.

## 1.0.25 requested behavior
- Internet Settings no longer has a manual Refresh action. While the Internet category is open and the page is online, request-scoped `/v1/network-info` observations refresh automatically every 3 seconds and stop when the category/drawer is no longer active.
- Browser `offline` remains event-first and immediate. API reachability is now first-failure decisive with a bounded 2.2-second live-sync probe instead of a two-failure debounce; reconnect/network-interface changes force an immediate recheck.
- Successful reconnect uses only the `Connection restored` presentation, has no `Online` badge, remains visible for the complete 5-second recovery window, and cannot be collapsed early by concurrent successful probes.
- Internet country presentation uses the observed two-letter request country code to resolve a localized country name and a bundled same-origin flag image for every accepted code. Missing/unknown network data is not inferred and no runtime flag CDN is used.
- Site-wide scrollbars and enhanced select option menus use the Database visual system while the native `<select>` remains authoritative for accessibility and keyboard semantics.
- Encyclopedia is rebuilt as a local Vulkan-reference workspace with registry summary, focused search/category navigation, structured result cards and explicit reference-vs-runtime-evidence guidance.
- Surface is rebuilt as a WSI-evidence workspace with canonical Surface/query state summaries, focused explorer controls, semantically distinct evidence sections, and explicit unavailable/unsupported/not-applicable/unknown guidance.

## Release gates
- `tools/verify_regression_contract.py` protects immutable 1.0.24 and the explicit 1.0.24 → 1.0.25 successor allow-list.
- `tools/verify_1_0_25_connectivity_surface_encyclopedia.py` verifies network timing/detection, automatic Internet observations, local country flags, coherent scroll/select presentation, Surface/Encyclopedia workspaces, and release identity.
- `tools/test_1_0_25_connectivity_surface_encyclopedia_negative_mutations.py` proves targeted 1.0.25 regressions are rejected.
- Worker transport contract, source audit, JS syntax, UTF-8/route/compare contracts, D1 migration chain, Pages artifact/release-ready boundary, strict clean-extract validation, and deterministic packaging remain mandatory.
