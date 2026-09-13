## 1.2.2

- Hardened the GitHub Release publication boundary against transient GitHub API `5xx` / `429` failures with bounded exponential retry and state re-checks between attempts.
- Release creation remains fail-closed: an existing `v1.2.2` tag or release must resolve to the validated `GITHUB_SHA`; published tags are never retargeted.
- Database/Worker/frontend identity advances to 1.2.2 / `app.v1202.js` / cache key 1202. D1 schema, report payload bytes/hashes, normalizer, Vulkan registry baseline and the VulkanScope 1.2.5 submission floor are unchanged.

# VulkanScope Database changelog

## 1.2.0
- New report submissions now require VulkanScope 1.2.5+ at the Worker/API boundary; historical stored reports remain readable.
- Internet observation refreshes silently in the background after initial data, while errors remain explicit.
- Regional country selection uses readable English names plus bundled same-origin flags for every supported country code.
- Compare emphasizes VulkanScope producer versions in bold white to make cross-producer differences immediately visible.
- Surface, Compare, Encyclopedia and every other non-Reports view receive purpose-specific workspace hierarchy and coherent applicable-filter grouping without changing evidence semantics.
- Settings informational and warning messages use distinct icon-backed blue/amber semantic callouts.
- Release identity advances to Database 1.2.1 / app.v1200 / cache 1200; D1 schema, stored payloads, report IDs/hashes, normalizer and Vulkan registry baseline remain unchanged.

## 1.0.25
- Replaced the Internet panel's manual Refresh action with automatic request-scoped network observations every 3 seconds while the Internet Settings category is open and online.
- Made disconnect handling event-first and first-failure decisive: browser offline events surface immediately, live API reachability uses a bounded probe, and reconnect/network-interface changes force an immediate recheck.
- Removed the recovered-state Online badge/text and extended the successful “Connection restored” status to a stable 5-second window before smooth collapse.
- Replaced platform-dependent regional-indicator flag glyphs with bundled same-origin country flag images for all accepted country codes, while keeping the observed code/localized country name and avoiding runtime flag CDNs.
- Applied Database-styled scrollbars and accessible enhanced select option menus across the site.
- Redesigned Encyclopedia as a focused local Vulkan-reference workspace with registry summary, search/category navigation, structured reference cards and explicit reference-vs-evidence guidance.
- Redesigned Surface as a WSI evidence workspace with canonical Surface/query summaries, focused explorer controls, clearer evidence sections and strict unavailable/unsupported/not-applicable/unknown semantics.
- Release identity advances to Database 1.0.25 / app.v1025 / cache 1025; report payload semantics, D1 schema/migrations, normalizer, Vulkan baseline and report evidence remain unchanged.

## 1.0.24
- Removed the redundant right-side UNAVAILABLE chip from the Database-API-unavailable banner and fixed successful reconnect status so “Connection restored” remains visible for the full 3-second interval before smooth collapse.
- Added regional presentation preferences for country/region, date layout, 12/24-hour clock, browser/UTC/GMT/IANA time zone, and automatic/standard/daylight seasonal offset handling.
- Routed report submission dates, report detail, Compare metadata, Settings clock, and observed server time through one presentation formatter without changing stored timestamps, sorting instants, report hashes, or D1 data.
- Expanded Internet country information from the request country code to a localized full country name plus country flag, with no third-party flag/CDN request.
- Redesigned Compare as a distinct A/B workspace with baseline/candidate identity cards, Swap, grouped comparison modes, focused evidence filters, difference overview, section counts, and visually distinct A/B table columns.
- Release identity advances to Database 1.0.24 / app.v1024 / cache 1024; report payload semantics, D1 schema/migrations, normalizer, Vulkan baseline, and VulkanScope submission floor are unchanged.

## 1.0.23
- Added live network-state monitoring: browser offline/reconnect events update a layout-aware status banner immediately; offline/unreachable states stay visible and a restored state collapses smoothly after 3 seconds.
- Preserved 3-second live report synchronization and 10-second published-release checks, with reconnect paths resuming both without requiring a manual page refresh.
- Reorganized Settings into Internet, Favorites and Preferences. Internet details remain request-scoped; IPv4 is orange, IPv6 is green, and unavailable address families/DNS are not inferred.
- Made persistent Favorites and report-column defaults opt-in with “Remember on this device”, added clear-saved-data control and explicit local-storage/privacy disclosure.
- Redesigned report-detail Favorite / Share / Copy link controls into one integrated action surface.
- Smoothed report-row hover/press and report-detail open/close interactions while preserving drag-to-select click suppression and reduced-motion behavior.
- Release identity advances to Database 1.0.23 / app.v1023 / cache 1023; report payload semantics, D1 schema/migrations, normalizer and Vulkan producer contract are unchanged.

## 1.0.22
- Initial preload/live reconciliation now builds one authoritative current report set and commits it atomically; the UI no longer presents snapshot + incremental/new payload counts.
- Added per-report Favorites with browser-local persistence and a Favorites list in Settings.
- Added a left-sliding Settings drawer beside the VulkanScope logo with local clock/time zone, current network observations, and persistent defaults for Submitted, GPU Vendor, and GPU Type column expansion.
- Added GET-only/no-store `/v1/network-info`; observed IP family, Cloudflare country/region/city/ASN/edge and transport details are shown without D1 persistence. Unobserved IPv4/IPv6 and client DNS are explicitly not fabricated.
- Fixed report navigation firing after primary-pointer drag text selection.
- Release identity advances to Database 1.0.22 / app.v1022 / cache 1022; report schema, payload hashes, D1 schema, normalizer and Vulkan producer contract are unchanged.


## 1.0.21

- Replaces the fragile full-index-only background refresh with a lightweight `/v1/sync` freshness head polled every 3 seconds while the page is active.
- Adds cache-resistant no-store + nonce live requests, forced reconciliation on focus/visibility/pageshow/online, and atomic report/index replacement so newly accepted reports update the active page, counters, statistics and filters without F5.
- Fetches only newly missing compact report payloads after the sync token changes; failed reconciliations keep the last committed token and retry instead of silently advancing stale state.
- Preserves exact-report de-duplication: resubmitting the same canonical report ID does not create a second statistical sample.
- Keeps the 1.0.20 Pages release-ready handshake independent from live report synchronization.

## 1.0.20
- Breaks the refresh-loop dependency between cached 1.0.18 frontends and Worker rollout by removing the legacy Worker `databaseVersion` refresh signal; Worker release identity is informational only.
- Replaces the source-ready marker with a schema-2 non-ready marker. Only the post-Release staged Pages artifact can be transitioned to `releaseReady:true`.
- Requires no-store agreement between release marker, published `index.html`, and the exact cache-busted app asset before offering Refresh, and suppresses immediate repeat prompts after a failed/stale navigation.
- Moves production publication back to the validated `main` ref, creates the GitHub Release/tag from that validated commit first, then rebuilds/marks/audits/uploads/deploys Pages in the deploy job.
- Pins the documented Pages action chain (`configure-pages@v5`, `upload-pages-artifact@v4`, `deploy-pages@v4`) and keeps live report synchronization independent from frontend release state.
## 1.0.19
- Makes glow/spray follow the greatest non-zero coverage state in each grouped row rather than an arbitrary 80% cutoff; lower non-zero states remain hatched and zero remains empty.
- Stops treating a newly deployed Worker version as proof that a frontend release is ready. Update prompts now come only from the published same-origin release marker.
- Changes release publication ordering so main pushes verify/build only; tag workflows create/refresh the GitHub Release first and publish GitHub Pages only after that release succeeds.
- Refresh now uses a cache-busting navigation to prevent stale-page refresh loops.

## 1.0.18
- Fixes the Coverage Reports / Distinct modal page-size control so its 10/25/50 custom option menu opens upward and remains usable within the bounded dialog rather than being clipped below the footer.
- Restores Android robot artwork to the official online green `#3DDC84` with neutral dark details and prevents generic UI tinting from replacing the intrinsic colors.
- Adds a Statistics/Versions-style circular GPU/report distribution to Devices, plus a separate exact table with bold GPU name, vendor logo, vendor/family/raw ID, maximum device API, driver variants, report count and share.
- Replaces the stale historical Database audit implementation with a current 1.0.18 source + staged-Pages audit covering release identity, package hygiene, current Vulkan/schema locks, security/resource ceilings, syntax/contracts and D1 migration replay.
- Preserves 1.0.17 coverage glow/hatching, paged evidence modals, live synchronization/version refresh, report disclosure layout, vendor-ID provenance, HDR/display presentation, schema 2 / technicalReport 3 / normalizer 16 and the existing D1 storage model.

## 1.0.17
- Stabilizes >=80% semantic coverage glow/spray positioning across aggregate tabs, including exactly 100%.
- Adds Devices-parity GPU identity to the Versions exact-count table.
- Adds bounded scrollbar + 10/25/50 pagination to Coverage Reports and Distinct/value dialogs.

## 1.2.1
- Added compact sticky Compare tracking while scrolling long comparisons.
- Clarified browser effective network class so `4g` is never presented as LTE/physical access technology.
- Locked submission sorting/age filtering to raw server timestamps regardless of regional display preferences.
- Added confirmation dialogs for favorite removal and clearing saved browser data.
- Restored report-detail tab synchronization and interaction.
- Increased page scrollbar width and added disabled endpoint states to page scroll controls.
