# VulkanScope Database changelog

## 1.3.6

- Redesigns every per-report detail tab except **Overview**—Registry, Properties, Limits, Features, Formats, Memory, Queues, Surface, Display & HDR, Extensions, Instance, Profiles and Raw report—into a consistent evidence workspace with clearer section identity, compact summary metrics, separated evidence panels and explicit empty states.
- Keeps canonical Vulkan tokens/raw values, query availability versus returned values, support/availability semantics and all existing technical evidence intact; the redesign is presentation-only and preserves the established Overview layout.
- Keeps wide technical tables on the existing first-party horizontal table scroller and adds responsive containment for new detail headers/panels on desktop and mobile, including reduced-motion behavior.
- Adds a Raw report explanation describing `reportText` versus normalized/structured evidence and a **Download raw report** action that saves the exact stored `reportText` locally as UTF-8 TXT without reformatting or a Worker export endpoint.
- Replaces Raw report's old native scrollbar presentation with the same demand-driven custom surface scrollbar used elsewhere; the rail appears only when the raw text actually overflows.
- Preserves the 1.3.5 Submitted time-zone wrapping and the 1.3.4 filter-scrollbar / Compare-chevron contracts.
- Advances Database/frontend/Worker identity to 1.3.6 / `app.v1306.js` / `browser-compat.v1306.js` / `release-bootstrap.v1306.js` / cache key 1306. No D1 migration, report payload/hash, normalizer, Vulkan baseline, producer-floor or browser-floor change is introduced.

## 1.3.5

- Fixes the expanded Reports **Submitted → Time zone** value being kept on one line by an inherited `white-space: nowrap`, which could clip seasonal text at the Device-column boundary.
- Keeps the IANA zone and GMT offset complete and wrap-safe; when a forced seasonal mode is present, **Daylight / summer offset** or **Standard / winter offset** is rendered on a dedicated second line.
- Preserves Date and Time as single-line values, server-authored `submitted_at` semantics, sorting/age filters, Compare metadata, Submitted disclosure animation and table scrolling.
- Preserves the 1.3.4 demand-driven filter scrollbar and Compare chevron behavior.
- Advances Database/frontend/Worker identity to 1.3.5 / `app.v1305.js` / `browser-compat.v1305.js` / `release-bootstrap.v1305.js` / cache key 1305. No D1 migration, report payload/hash, normalizer, Vulkan baseline, producer-floor or browser-floor change is introduced.

## 1.3.4

- Fixes searchable filter menus showing the custom vertical scrollbar when the option list does not actually overflow. Opening a menu no longer forces the rail visible; the existing `is-scrollable` state derived from real `scrollHeight - clientHeight` overflow is now authoritative.
- Keeps genuine long filter lists fully scrollable with the existing arrows, track, thumb, drag, wheel/touch, keyboard and reduced-motion behavior.
- Reverses the Compare state chevrons to the requested semantics: expanded/full **Minimize** points up; minimized/closed **Expand** points down. Label, ARIA state and reset/unpin behavior remain synchronized through one JavaScript state owner.
- Preserves the 1.3.3 License viewer and filter/modal pagination motion behavior, including `prefers-reduced-motion`.
- Advances Database/frontend/Worker identity to 1.3.4 / `app.v1304.js` / `browser-compat.v1304.js` / `release-bootstrap.v1304.js` / cache key 1304. No D1 migration, report payload/hash, normalizer, Vulkan baseline, producer-floor or browser-floor change is introduced.

## 1.3.3

- Fixes Compare Minimize/Expand chevron direction by removing the duplicate CSS rotation that cancelled the state-specific SVG path change. Full/Minimize now points down and minimized/Expand points up, including reset/unpin behavior.
- Keeps the upper Compare workspace on its existing smooth collapse/expand path while preserving A/B identity, evidence, filters and routing semantics.
- Adds symmetric smooth open/close motion to the local License viewer with stale-close protection and correct focus restoration.
- Adds short direction-aware page transitions to searchable filter pagination and bounded modal pagination for Previous, Next and direct page jumps.
- Honors reduced-motion preferences by skipping decorative transitions while preserving the same authoritative state changes and accessibility behavior.
- Advances Database/frontend/Worker identity to 1.3.3 / `app.v1303.js` / `browser-compat.v1303.js` / `release-bootstrap.v1303.js` / cache key 1303. No D1 migration, report payload/hash, normalizer, Vulkan baseline or browser-floor change is introduced.

## 1.3.1

- Keeps all first-party Database UI copy in English and replaces the Khronos independence disclosure with the English wording in both the footer and Settings → Information.
- Disables direct-page **Go** whenever the entered page is already active, invalid/empty, or the result set has only one page.
- Repairs enhanced filter menus by separating search, scrollable options and pagination into stable layout regions; every searchable filter keeps 50-option paging and direct numeric page entry, even for a single page.
- Adds a bounded same-origin startup release-freshness bootstrap so stale cached frontend documents verify the published Pages marker/HTML/app asset before the UI is revealed, then navigate cache-busted only when a newer release is fully ready.
- Opens bundled Markdown license documents inside a responsive in-site modal instead of a new browser tab.
- Shows a green count-bearing popup when live synchronization actually adds new reports to the Database.
- Fixes a stale schema-footer Database version literal and adds focused positive/negative gates for freshness, filter containment, inline licenses and live-report notifications.
- Database/frontend/Worker identity advances to 1.3.1 / `app.v1301.js` / `browser-compat.v1301.js` / `release-bootstrap.v1301.js` / cache key 1301. No D1 migration, report payload/hash, normalizer or Vulkan evidence semantic change is introduced.

## 1.3.0

- Presents every standalone user-facing **Vulkan** label as **Vulkan®** while keeping `VulkanScope` unchanged and preserving canonical/raw evidence, API/schema/token names, filenames and stored report bytes. Dynamic UI text and accessible labels are covered by the same presentation-only rule.
- Adds the requested red Turkish Khronos independence notice below the footer brand and at the top of **Settings → Information**.
- Extends **Information** with local **Read license (.md)** actions for the officially sourced Wrangler, sharp, esbuild, workerd, Node.js and Python license texts/notices; component purpose, version/resolution status, license and source remain visible in each card.
- Keeps the 1.2.15 stored-report **Download JSON** action and the existing pagination, Compare, browser-information and Settings-overlay behavior intact.
- Adds release-specific positive/negative checks for trademark presentation, canonical/raw preservation, disclosures, local license files, Pages staging and dependency truthfulness, plus a full source/Pages/Worker/D1/responsive regression audit.
- Database/frontend/Worker identity advances to 1.3.0 / `app.v1300.js` / `browser-compat.v1300.js` / cache key 1300. No D1 migration, report payload/hash, normalizer or VulkanScope 1.2.5 submission-floor change is introduced.

## 1.2.14

- Added direct bounded page entry to every user-visible pagination family: searchable filter selectors, Reports, bounded aggregate tables and paged Coverage/Distinct/value dialogs. Previous/Next remain available; Enter/Go commit, Escape restores, Arrow Up/Down stays in range, and non-digit or out-of-range keyboard/paste/input values are rejected.
- Searchable filter selectors retain complete-set local search and deterministic 50-option pagination; direct page entry automatically follows the filtered page count and new searches reset to page 1.
- Added a dedicated Browser information section below My internet information with local best-effort browser/version/engine identity, Client Hints when exposed, UA/platform/language/privacy/runtime/display details and Web Platform capability availability. Browser details are not attached to VulkanScope reports, sent to the Database Worker or stored in D1.
- Added responsive containment for the new page-jump and Browser information surfaces across desktop and mobile, plus focused positive/negative release gates.
- Database/frontend/Worker identity advances to 1.2.14 / `app.v1214.js` / `browser-compat.v1214.js` / cache key 1214. D1 schema, report bytes/hashes, normalizer 16, Vulkan 1.4.362 and the VulkanScope 1.2.5 new-submission floor are unchanged.

## 1.2.13

- Searchable filters now paginate matching options in deterministic 50-item pages with Previous/Next and Page X of Y controls; local search still scans the complete authoritative native option set.
- Compare Minimize/Expand chevrons now reflect state: down while full, up while minimized.
- Full UI regression hardening caps enhanced selectors to their containers, removes the inherited mobile 190 px minimum, contains long option labels, and keeps pagination controls narrow-safe.
- Database/frontend/Worker identity advances to 1.2.13 / `app.v1213.js` / `browser-compat.v1213.js` / cache key 1213. D1 schema, report bytes/hashes, normalizer 16, Vulkan 1.4.362 and the VulkanScope 1.2.5 new-submission floor are unchanged.

## 1.2.12
- Added local search to every main/detail workspace custom filter/select listbox on desktop and mobile. Search always runs against the complete authoritative native select option set while the enhanced DOM is bounded to at most 50 visible choices at once.
- Fixed pinned Compare report selectors so the centered Minimize/Expand dock hides while a listbox is open instead of painting over or intercepting report options.
- Fixed Settings overlay ownership: pinned Compare and viewport chrome now sit beneath the Settings backdrop, the full underlying page receives the dim/blur treatment, and destructive confirmation remains above Settings.
- Database/frontend/Worker identity advances to 1.2.12 / `app.v1212.js` / `browser-compat.v1212.js` / cache key 1212. D1 schema, report bytes/hashes, normalizer 16, Vulkan 1.4.362 and the VulkanScope 1.2.5 new-submission floor are unchanged.

## 1.2.11
- Fixed the narrow/mobile Compare report identity collision where a wrapped `System Vulkan driver …` identity row could overlap the Baseline/Candidate metadata chips. The full report-identity block now expands to its content in the normal workspace and narrow layouts stack GPU, vendor and driver identity rows intrinsically.
- The compact pinned Compare state still collapses the identity rows to zero height and restores them when the full workspace returns; report selection, A/B identity, evidence filters and comparison semantics are unchanged.
- Database/frontend/Worker identity advances to 1.2.11 / `app.v1211.js` / `browser-compat.v1211.js` / cache key 1211. D1 schema, stored report bytes/hashes, normalizer 16, Vulkan 1.4.362 and the VulkanScope 1.2.5 new-submission floor are unchanged.

## 1.2.10
- Fixed mobile/portrait filter containment across every non-Reports Database workspace. Global filter families and view-specific subfilters now collapse to intrinsic single-column controls at <=900 px with `min-width:0`/100% containment, preventing the narrow multi-column squeeze shown on Compare and aggregate views. Reports keeps its already-correct 1.2.9 layout.
- Cross-producer Compare warnings now render both VulkanScope version identities, including versionCode when present, in bold white while keeping the warning text and evidence semantics unchanged.
- Database/frontend/Worker identity advances to 1.2.10 / `app.v1210.js` / `browser-compat.v1210.js` / cache key 1210. D1 schema, report payload/hash semantics, normalizer 16, Vulkan 1.4.362 and the VulkanScope 1.2.5 submission floor are unchanged.

## 1.2.9
- The browser compatibility warning is hidden at parse time and is revealed only after the local compatibility check actually fails, removing the false unsupported-browser flash on supported browsers.
- Reports global filters now use the same filter-family cards and custom-select hierarchy as the other workspaces; Sort/Per page use the same grouped control language, and narrow screens collapse filters to one non-overflowing column.
- The pinned Compare shell gains a centered minimize/expand control. Minimized follow mode shows only A/B GPU identities in their baseline/candidate colors with a center divider; returning above the Compare sentinel restores the full workspace automatically. Pinned width no longer enforces a 260 px mobile minimum.
- Settings, custom select menus (including Reports filters), coverage-dialog bodies and paged evidence lists use an in-panel scrollbar rail that reuses the authoritative viewport scrollbar arrow/track/thumb design and endpoint/keyboard/drag behavior.
- Database/frontend/Worker identity advances to 1.2.9 / `app.v1209.js` / `browser-compat.v1209.js` / cache key 1209. D1 schema, report payload/hash semantics, normalizer 16, Vulkan 1.4.362 and the VulkanScope 1.2.5 submission floor are unchanged.

## 1.2.8

- Fixed Compare follow behavior by replacing ancestor-sensitive CSS sticky ownership with a JS-synchronized viewport-fixed shell and a flow placeholder. The selected Baseline/Candidate reports and comparison mode now remain visible while scrolling long comparison tables.
- Compare custom report selectors remain above the pinned workspace and are not clipped when opened.
- Database/frontend/Worker identity advances to 1.2.8 / `app.v1208.js` / `browser-compat.v1208.js` / cache key 1208. D1 schema, report payload/hash semantics, normalizer 16, Vulkan 1.4.362 and the VulkanScope 1.2.5 submission floor are unchanged.

## 1.2.7
- Compare now uses a dedicated overflow-visible sticky shell so Baseline/Candidate controls follow the viewport correctly and report-selector menus are not clipped by the comparison workspace.
- The authoritative DOM viewport rail now marks the lower endpoint gray/disabled using `document.scrollingElement` range metrics; the draggable thumb keeps the normal cursor instead of grab/grabbing cursors.
- The persistent Vulkan Hardware Database hero is redesigned as a workspace-aware command deck for every primary tab while retaining global search, dataset metrics, repository/developer identity and report-backed evidence semantics.
- Reports row hover is synchronized across every cell so the Submitted/date-time cell eases smoothly even when pointer entry begins over Report ID, Favorite or another distant column.
- Database/frontend/Worker identity advances to 1.2.7 / `app.v1207.js` / `browser-compat.v1207.js` / cache key 1207. D1 schema, report payload/hash semantics, normalizer 16, Vulkan 1.4.362 and the VulkanScope 1.2.5 submission floor are unchanged.

## 1.2.6
- Replace browser-specific viewport scrollbar-button endpoint painting with an accessible same-origin DOM viewport rail so endpoint arrow state is deterministic across supported Chromium, Firefox and Safari/WebKit families.
- Keep the top UP arrow gray/disabled at absolute top and the bottom DOWN arrow Vulkan red at absolute bottom while preventing out-of-range movement.
- Redesign report detail hero and Overview as a structured evidence workspace; show the complete canonical 64-character report ID and provide a local copy-ID affordance.
- Enlarge and restyle the report Back control across every detail tab; preserve smooth/reduced-motion behavior and mobile containment.
- Database/frontend/Worker identity advances to 1.2.6 / `app.v1206.js` / cache key 1206; D1, report hashes, Vulkan evidence and the VulkanScope 1.2.5 submission floor are unchanged.

## 1.2.5

- Fix the Database-themed far-right viewport scrollbar so endpoint state is applied to the real root scrollbar across Chromium/WebKit ownership differences: the UP arrow becomes gray at the absolute top and the DOWN arrow remains Vulkan red at the absolute bottom as requested.
- Repair accidental literal `\n` serialization in the 1.2.3 CSS append; this had prevented the endpoint-state, broad motion and mobile containment layer from parsing correctly in the browser.
- Mirror page-top/page-bottom state to both `html` and `body` and keep application page-scroll controls independently boundary-aware.
- Extend the shared smooth interaction language across all primary tabs/workspaces, table rows, controls, settings, filters, cards and dialogs, and add a smooth destructive-confirmation close transition while preserving `prefers-reduced-motion`.
- Preserve 1.2.4 bounded report-identity table paging, GitHub Release retry/tag immutability, browser floors, English UI, mobile containment, D1/report semantics and the VulkanScope 1.2.5 submission floor.
- Database/frontend/Worker identity advances to 1.2.5 / `app.v1205.js` / cache key 1205.

## 1.2.4

- Fix GitHub Actions generated-index re-verification so the current 1.2.4 verifier runs after `build_index.py`; predecessor 1.2.2 identity checks are no longer applied to a current release checkout.
- Bound every GPU/device/report-identity table outside Reports to the same 10/25/50 per-page model, range indicator and Previous/Next semantics used by Reports.
- Pagination slices only final presentation rows; full filtered sets continue to drive statistics, coverage and evidence semantics.
- Retain the 1.2.2 GitHub Release retry/tag-immutability hardening and all 1.2.3 browser/English/motion/mobile protections.
- Database/frontend/Worker identity advances to 1.2.4 / `app.v1204.js` / cache key 1204; D1 schema, payload hashes, normalizer, Vulkan registry baseline and VulkanScope 1.2.5 submission floor are unchanged.

## 1.2.3

- Hardened the GitHub Release publication boundary against transient GitHub API `5xx` / `429` failures with bounded exponential retry and state re-checks between attempts.
- Release creation remains fail-closed: an existing `v1.2.3` tag or release must resolve to the validated `GITHUB_SHA`; published tags are never retargeted.
- Database/Worker/frontend identity advances to 1.2.3 / `app.v1203.js` / cache key 1203. D1 schema, report payload bytes/hashes, normalizer, Vulkan registry baseline and the VulkanScope 1.2.5 submission floor are unchanged.

# VulkanScope Database changelog

## 1.3.2

- Reworks frontend release freshness around publication-generation convergence: startup and post-reveal no-store checks verify the release marker, index, app, compatibility gate and bootstrap together, then automatically navigate to the fully published release without requiring a Refresh button.
- Retains the immutable 1.3.1 frontend triplet for one transition release so stale CDN HTML cannot reference removed assets while GitHub Pages edges converge.
- Prevents blank custom-scrollbar rail/gutter regions from accepting pointer input; only the intended arrows, track and thumb remain interactive.
- Prevents custom filter menus from closing when a scrollbar drag/click ends inside the menu.
- Compacts filter Previous/Next pagination into fixed icon cells with a flexible bounded page-jump control so mobile and desktop layouts do not overflow.
- Restyles the Khronos independence notice as a modern blue information card with an information icon while keeping the exact English wording unchanged.
- Database/frontend/Worker identity advances to 1.3.2 / `app.v1302.js` / `browser-compat.v1302.js` / `release-bootstrap.v1302.js` / cache key 1302. No D1 migration, report payload/hash, normalizer, Vulkan baseline or browser-information-content change is introduced.

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

## 1.3.7
- Replaced the generic Browser information globe with local original-color browser marks for explicitly identified Chrome, Chromium, Edge, Firefox, Safari, Opera, Brave, Vivaldi and Samsung Browser sessions.
- Updated the Samsung product label from Samsung Internet to Samsung Browser while preserving the existing `SamsungBrowser/` detection token.
- Added best-effort Brave and Vivaldi identification without adding fingerprinting probes; ambiguous Chromium-family sessions intentionally retain the neutral browser icon instead of being misbranded.
- Bundled browser marks locally with no logo CDN or third-party runtime request and added vendor provenance/trademark notes in `licenses/browser-marks.md`.
- Preserved Database storage/report semantics, D1 schema/migrations, Vulkan evidence behavior, browser compatibility floors and all 1.3.6 report-detail/Raw-report behavior.

## 1.3.8

- Removed browser logo/icon rendering and bundled browser-mark assets from Browser information; identity remains local text-only runtime information.
- Reworked regional date/time presentation into Automatic, Country, and Manual modes. Automatic uses browser/system locale and time zone; Country derives locale conventions and a representative IANA time zone from the selected country; Manual enables granular overrides. Stored/server timestamps remain unchanged.
- Fixed custom-filter labels so long values wrap instead of being clipped, and made one-page page-jump controls completely non-interactive/focusable.
- Added disabled-state synchronization between native selects and custom select controls so locked regional controls cannot be opened.
