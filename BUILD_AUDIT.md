# VulkanScope Database 1.0.23 build / regression audit

## Release identity
- Database/frontend release: **1.0.23**.
- Frontend identity: `assets/app.v1023.js`, cache key `1023`.
- Worker identity: `1.0.23`; D1 schema and migration chain are unchanged from 1.0.22.
- Immutable predecessor: VulkanScope Database 1.0.22, SHA-256 `2779cbc0fd42e1114727fbd95dc2fb3145a24234f2f1a01e65197f2ba36e3811`.

## 1.0.23 requested behavior
- Browser online/offline events update a top-of-page network status surface immediately. Offline/unreachable states remain visible; successful recovery changes to a restored state and collapses after 3 seconds.
- The status surface participates in layout and the sticky application/report navigation offsets follow it, so the page moves smoothly rather than being overlaid.
- Live report synchronization remains a 3-second current-set check; successful connectivity also resumes the 10-second published Database release check.
- Settings are separated into exactly three categories: Internet, Favorites, Preferences. IPv4 is orange and IPv6 is green; unobserved address families and DNS are explicitly not fabricated.
- Favorite/report-column persistence is opt-in through “Remember on this device”. Without opt-in, these values remain session-only. Clear saved browser data removes persistent favorites/preferences and resets their session state.
- Network observations are request-scoped, are not attached to reports, and `/v1/network-info` performs no D1 write.
- Report detail Favorite / Share / Copy link actions use one integrated action surface matching the Database design system.
- Report row hover/press feedback and report-detail open/close transitions are eased; text-drag selection still suppresses accidental report navigation; reduced-motion users receive non-animated behavior.

## Release gates
- `tools/verify_regression_contract.py` protects the immutable 1.0.22 predecessor and the explicit 1.0.22 → 1.0.23 successor allow-list.
- `tools/verify_1_0_23_connectivity_settings_motion.py` verifies the connectivity, Settings privacy/storage, network coloring, report-action, motion, live-sync and immutable-data requirements.
- `tools/test_1_0_23_connectivity_settings_motion_negative_mutations.py` proves the 1.0.23 verifier rejects targeted regressions while allowing a harmless changelog-only control mutation.
- Worker transport contract, source audit, syntax checks, UTF-8/route/compare contracts, Pages artifact validation, strict clean-extract verification and deterministic packaging remain mandatory.
