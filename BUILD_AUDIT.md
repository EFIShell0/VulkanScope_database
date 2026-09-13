# VulkanScope Database 1.0.24 build / regression audit

## Release identity
- Database/frontend release: **1.0.24**.
- Frontend identity: `assets/app.v1024.js`, cache key `1024`.
- Worker identity: `1.0.24`; D1 schema and migration chain are unchanged from 1.0.23.
- Immutable predecessor: VulkanScope Database 1.0.23, SHA-256 `f3940d1e5fafc28bffb3690b40ffcd513d692e57077849e0655440a55968a66d`.

## 1.0.24 requested behavior
- Database-unavailable state keeps its explanatory top banner but no longer shows a redundant right-side `UNAVAILABLE` chip.
- Successful recovery remains visibly in “Connection restored” for the complete 3-second interval; subsequent successful probes during that window cannot collapse it early.
- Preferences adds regional country, date layout, clock mode, time zone, and automatic/standard/daylight seasonal presentation controls. All are session-only until Remember on this device is enabled.
- Report-list timestamps, report detail, Compare report metadata, Settings clock, and Internet server time share the same regional formatter. Stored UTC/ISO instants, sorting, filtering, payloads, hashes, and D1 values are unchanged.
- Country code in Internet information expands to a localized full country name plus the corresponding regional-indicator country flag without a third-party runtime request.
- Compare is rebuilt as a dedicated A/B workspace with baseline/candidate identity cards, Swap, grouped comparison modes, dedicated evidence filtering, visible-difference overview, section counts, and differentiated A/B table lanes while keeping existing compare evidence semantics and warnings.

## Release gates
- `tools/verify_regression_contract.py` protects immutable 1.0.23 and the explicit 1.0.23 → 1.0.24 successor allow-list.
- `tools/verify_1_0_24_regional_compare_country.py` verifies recovery timing, regional preference validation/storage, centralized date/time presentation, country name/flag expansion, Compare workspace semantics, and release identity.
- `tools/test_1_0_24_regional_compare_country_negative_mutations.py` proves targeted 1.0.24 regressions are rejected while a harmless changelog-only mutation remains accepted.
- Worker transport contract, source audit, JS syntax, UTF-8/route/compare contracts, D1 migration chain, Pages artifact/release-ready boundary, strict clean-extract validation, and deterministic packaging remain mandatory.
