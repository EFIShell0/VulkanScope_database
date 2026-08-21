# 0.36.0

- Matched luminance unit typography to OpenGLESScope: `cd/m²` now uses muted 0.92em presentation while the numeric value remains primary.
- Applied the same luminance presentation in Display & HDR aggregate and report-detail views.
- Added cache-busted `app.v0360.js` and `site.v0360.css`; no D1 migration.

# 0.35.9

- Renamed Display / HDR presentation to Display & HDR.
- Added supported-device ABI listing beneath Platform / ABI in Reports.
- Added cd/m² presentation for numeric Android minimum/average/maximum luminance values.
- Added separate Producer/query baseline and Compatible producers home metrics.
- Preserved report schema, evidence semantics, raw report data and D1 storage.
- Active frontend JavaScript bumped to `app.v0359.js`; no D1 migration.

# 0.35.8

- Fixed Properties count/classification to use schema-v3 `detailedProperties` instead of the broad normalized capability collection.
- Fixed Limits count/classification to use schema-v3 `limits` instead of section-name heuristics.
- Prevented DEVICE/SURFACE metadata from inflating Properties and prevented `Sparse Properties` from being counted as Limits.
- Added separate legacy TXT fallback arrays for bracketed non-feature properties and the literal LIMITS section.
- Updated aggregate and report-detail views to use the exact separated datasets.
- Added regression tests for structured-array authority and metadata contamination.
- Worker normalizer bumped to 11; no D1 migration.
- Active frontend JavaScript bumped to `app.v0358.js`.

# 0.35.7

- Audited VulkanScope 0.33.7 producer compatibility end-to-end.
- Added schema-v3/top-level cross-validation for primary GPU, driver, API and registry metadata.
- Added current TXT report identity/section validation.
- Added 20 s / 4 MiB bounded frontend API reads, repeated-cursor protection and four-way detail-fetch concurrency.
- Fixed property, limit and feature coverage denominators so absent fields count as Unknown.
- Fixed format coverage to retain Unknown for loaded reports missing a format row.
- Fixed Display/HDR missing-vs-empty semantics and expanded semantic state filtering.
- Added CORP/COOP and restrictive API CSP headers.
- Updated published Khronos specification reference to Vulkan 1.4.359 (2026-08-07), separate from the 1.4.360 producer/query baseline.
- Worker normalizer bumped to 10. No D1 migration.

# 0.35.6

- Reworked the database background and interactive chrome to the OpenGLESScope-quality chromatic shell using Vulkan official red `#A41E22`.
- Vulkan-red-derived styling now covers the page glow, hero, navigation/detail tabs, filters, search focus, cards, scroll controls, pagination and action surfaces.
- Preserved supported/unsupported/available/unavailable/unknown semantic colors and 0.35.3 dominant-coverage rules unchanged.
- Versioned frontend assets to `site.v0357.css` and `app.v0357.js` for cache-safe GitHub Pages deployment.

# 0.35.5

- Fixed Windows false-negative Cloudflare account verification after a valid project-local `vulkanscope` profile was activated.
- The verifier now executes the pinned local Wrangler CLI through Node when available, avoiding unreliable direct `npx.cmd` execution from `child_process`.
- `wrangler whoami --json` remains the primary check; a plain-text fallback is accepted only when the pinned VulkanScope account ID is present.
- Wrangler debug-log environment variables are stripped from verifier subprocesses so JSON output remains parseable.
- Fail-closed behavior is preserved: unreadable, missing or mismatched account identity still blocks deploy, migrations and D1 diagnostics.
- No report schema, D1 migration, frontend behavior or production binding changed.

# 0.35.4

- Added project-local Wrangler auth-profile commands for the `vulkanscope` profile.
- Pinned `account_id` to the production VulkanScope Cloudflare account and preserved the existing production D1 UUID.
- Added fail-closed active-account verification before npm deploy, migration, migration-list and D1 count operations.
- Added a root `.gitignore` for dependencies, Wrangler local state, environment/secret files, logs, caches and build outputs.
- Pinned Wrangler to 4.124.0 for reproducible project-local CLI behavior.
- No report schema, D1 migration, frontend capability semantics or API endpoint behavior changed.

# 0.35.3

- Fixed coverage status backgrounds leaking across the full percentage cell for non-dominant states.
- Non-dominant states now retain semantic color only in the progress-bar fill; percentage text and surrounding coverage area remain neutral.
- The unique dominant state may retain the wider semantic emphasis introduced by 0.35.1.
- Equal top percentages remain neutral and state-count badges are unchanged.

# 0.35.2

- Full rules/security/specification regression audit of 0.35.1.
- Added stable `(submitted_at,id)` cursor pagination for `/v1/reports`; the frontend now walks every index page instead of silently stopping at 500 reports.
- Fixed TXT fallback loss of Surface color-space extension and format-query diagnostics.
- Fixed Compare memory heap/type flags showing escaped HTML presentation markup instead of canonical flag text.
- Fixed Compare empty `hdrTypes` state to Unavailable, matching Display/HDR rules.
- Generic Surface capability scalars now remain Available even when their value is false/zero; query diagnostic booleans are displayed as reported values rather than reinterpreted as unsupported.
- Replaced raw-text sensitive-token scanning with recursive sensitive-key validation, preventing personal/account identifier fields while avoiding false rejection of harmless technical report text.
- Stored malformed payload JSON now returns an explicit 500 JSON error instead of throwing through the request path.
- Worker normalizer bumped to 9.

# 0.35.1

- Coverage percentage labels now color only the unique dominant state in each distribution.
- Non-dominant percentage labels remain neutral while progress-bar fills keep their semantic state colors.
- Equal top percentages remain neutral; state-count badges are unchanged.
- The rule applies consistently to feature, format, memory, extension, instance/layer, profile and generic aggregate coverage rows.

# 0.35.0
- Full rules/security/data-semantics/specification audit.
- Fixed Compare to use current VulkanScope schema fields `gpu.deviceType` and `vulkan.loaderInstanceApiVersion`.
- Fixed scalar property/limit false or zero values being misclassified as Unsupported in compatibility/structured normalization; queried properties remain Available while feature booleans retain Supported/Unsupported semantics.
- Extended TXT compatibility parsing for current queue `videoCodecOperations` and Vulkan Registry Coverage data.
- Fixed fallback memory flag text rendering in detail/Compare paths.
- Hardened Worker POST body handling with a streaming 2 MiB byte limit and stronger nested submission-shape validation; normalizer version is now 8.
- Clarified Android Display preferred wide-gamut labeling so it is not presented as measured physical-panel gamut.
- Corrected active release/footer asset/version metadata.
- Made submission de-duplication key-order independent with bounded stable JSON canonicalization.
- Surfaced individual report-detail fetch failures so incomplete loaded sets are never silently presented as complete.

# 0.34.9
- Made Compare controls, summary metrics and section framing more compact on desktop and mobile.
- Made Portability summary/coverage metrics and table density more compact without changing data semantics.
- Added main-view scoping for these presentation-only density rules so other database sections remain unchanged.

# 0.34.8
- Reduced filter selector footprint across desktop and mobile without changing native select state or keyboard behavior.
- Added semantic local SVG icons to filter controls and options.
- Added Display/HDR newest-first / oldest-first submission ordering; Vendor/GPU/Vulkan filters remain excluded from Display/HDR.

# 0.34.7

- Removed the Vulkan API-version filter from the Android Display / HDR view because that view describes Android display capability rather than Vulkan API capability.
- Display / HDR now ignores any previously selected Vulkan API filter state, matching the existing device/GPU filter isolation for this view.
- Preserved all 0.34.6 HDR artwork, security, VulkanScope 0.32.7 schema compatibility and data-state semantics.

# 0.34.6

- Replaced the synthetic/cropped HDR10 presentation with the dedicated HDR10 SVG supplied by the project owner.
- Added an opaque white background to the HDR10 asset for dark-theme legibility while preserving the original black logo artwork.
- Added conditional browser Origin validation to the Worker without blocking native VulkanScope submissions that do not send Origin.
- Updated Worker package metadata to 0.34.6 and re-audited frontend/Worker security, data semantics and VulkanScope 0.32.7 compatibility.

# 0.34.5
- Restored smooth primary-section navigation transitions.
- Fixed Vulkan API-version numeric sorting.
- Re-audited app 0.32.6 compatibility, CapsViewer parity, security and performance.
- Added Display/HDR aggregate/detail views and layer-extension visibility.
- Clarified producer/query baseline metadata.

# 0.34.3

- Styled Device API, Loader API, Vulkan API and Max API values as consistent high-contrast VulkanScope version chips across aggregate tables, report overview and Compare.
- Raw version strings remain unchanged; presentation-only update.

# 0.34.2

- Refined the Compare `Differences only` control into a touch/mouse/keyboard-friendly VulkanScope-styled checkbox.
- Preserved the existing Compare filter state and data semantics.
- Added focus-visible and reduced-motion behavior.

# 0.34.2

- Fixed System Vulkan driver custom-listbox contrast: GPU model is now explicitly white and bold, while the driver suffix remains muted and normal-weight in all interaction states.
- Preserved Turnip / third-party red-accent styling and native select state semantics.

# 0.34.0

- Bold GPU model presentation across report-backed lists.
- Smooth, reduced-motion-aware main navigation view transitions.
- Re-ran Vulkan/CapsViewer parity, security, performance and data-integrity audits.

# 0.33.8

- Added local GPU vendor logo assets sourced from the VulkanScope Android application and an explicit **Logo** column beside GPU names in device/report-backed technical tables.
- Added canonical vendor-logo fallback logic; unknown/unmapped vendors use the bundled unknown GPU mark instead of a guessed identity.
- Styled only explicit **Turnip / third-party driver** labels with the VulkanScope red accent while preserving all raw driver text and report data.
- Web-optimized the local vendor logo assets to 128×128 PNGs for lower transfer/decode cost without introducing any third-party requests.
- Preserved Vulkan 1.4.360 canonical/raw decoding, schema-v3 structured-report precedence, exact U64 handling, report-state semantics, IPv4/IPv6 transport neutrality and the 0.33.7 interaction fixes.
- Re-audited CapsViewer/Vulkan Hardware Database category parity, frontend CSP/CORS assumptions, table overflow usability, parser boundaries and Worker request handling.

# 0.33.7

- Added smooth, race-safe report-detail tab transitions with reduced-motion support and keyboard tab navigation.
- Replaced abrupt native distinct-value/coverage details with touch/mouse/keyboard-friendly animated accordions and synchronized chevrons.
- Added per-queue presentation support to report Queue detail and presentation queue/query diagnostics to Surface detail.
- Re-audited Vulkan Hardware Database report/category parity; no state is inferred when data is absent.

# 0.33.6

- Replaced visible native table scrollbars with VulkanScope-styled horizontal scroll controls: arrows, draggable/clickable track, edge fades, touch panning and keyboard support.
- Smoothed custom filter opening animation so chevron and listbox animate symmetrically on open and close.
- Fixed long Surface present-mode tokens overflowing their cards.
- Added polished static error pages for common HTTP errors and a styled frontend API-load failure state with Reports/GitHub/retry actions.
- Improved Worker HTTP method semantics (405 + Allow) and added defensive response headers.
- Full UI/usability/security regression audit; Vulkan 1.4.360 data semantics remain unchanged.

## 0.33.6

- Added design-integrated custom filter/listbox controls with keyboard, mouse and touch support.
- Replaced the visible primary-navigation scrollbar with left/right arrow controls, edge fades and direct gesture/trackpad/wheel scrolling.
- Added an official VulkanScope GitHub repository action to the database hero.
- Expanded report comparison to Devices, normalized capabilities, Extensions, Formats, Queue families, Memory, Surface/WSI and Profiles for closer Vulkan Hardware Database parity.
- Re-audited overflow, active-state, canonical value, status-color and structured-report behavior.

# VulkanScope Database 0.33.6

- Synchronize browser titles with active main and report-detail sections.
- Update VulkanScope application compatibility to 0.32.4 and validated query baseline to Vulkan 1.4.360.
- Prefer schema-v3 structured features, detailed properties, limits, profiles and exact-width U64 fields while preserving TXT/raw fallback.
- Audit Worker/frontend for IPv6 safety: no client-IP parsing, persistence, report identity or IPv4-only address assumptions.
- Bump Worker normalizer version to 6.

# VulkanScope Database 0.33.4

- Decode and display canonical VkMemoryPropertyFlags/VkMemoryHeapFlags names while retaining raw masks.
- Prefer VulkanScope 0.32.2 schema-v3 technicalReport structured data when present.
- Distinguish Vulkan-Headers 1.4.360 compile baseline from validated Vulkan 1.4.357/CapsViewer 4.12 query coverage.
- Compact top navigation, add controlled logo-to-nav spacing, and collapse earlier to prevent the final tab clipping.
- Tighten portrait/mobile header geometry and preserve horizontal scrolling inside wide technical tables.

# VulkanScope Database 0.33.0

- Full UI parity audit against the public Vulkan Hardware Database navigation and listing structure, while preserving VulkanScope state semantics and design language.
- Added local inline SVG icons to every primary navigation tab.
- Added Portability view for explicit VK_KHR_portability_subset reports without inferring unsupported from absence.
- Queue families now expose every normalized boolean capability as an explicit Supported/Unsupported/Unknown state instead of hiding false values.
- Surface/WSI now has dedicated Capabilities, Formats/Color spaces, Present modes, Transform modes, Composite alpha modes, Usage flags and Presentation queues subviews.
- Properties, limits, features, formats, memory, extensions, instance data and profiles use state-semantic counts/percentages consistently; Unavailable is amber everywhere and Unknown is gray.
- Report-detail Surface and Instance views now preserve state colors and expose parsed device layers.
- Core/extension property and feature aggregates now expose value distributions and per-capability report drill-downs, matching the useful device-coverage detail of the reference site without copying its unsupported inference.
- Instance aggregate view now exposes parsed device layers separately instead of leaving them only in raw report text.
- No third-party UI assets or runtime dependencies were added.

# VulkanScope Database 0.32.1

- Memory aggregate view now mirrors the useful part of Vulkan Hardware Database memory coverage: exact VkMemoryPropertyFlags combinations with availability and non-availability percentages across loaded reports.
- Memory heaps and per-report memory type-to-heap mappings remain separately accessible.
- Added state-semantic percentage colors; unavailable percentages are amber, never green.
- State filters now cover all applicable aggregate sections without conflating unsupported, unavailable and unknown.
- Surface state filtering now includes capability/presentation states, present-mode availability and presentation queues where explicit state exists.
- Device/instance extension absence is kept Unknown/not listed unless direct unsupported evidence exists.

# VulkanScope Database 0.32.0

- CapsViewer-detail parity navigation for core properties/features, limits, formats, WSI and instance data.
- No report fields are synthesized; missing query state stays distinct from unsupported.

# Changelog
## 0.31.2
- Reworked Reports into a dense, CapsViewer-style technical table without discarding VulkanScope design language.
- Added exact submitted date/time including seconds and the browser timezone, backed by the immutable server-side D1 submitted_at value.
- Added driver mode, decoded driver version, raw driver version when distinct, physical-device API, loader/instance API, vendor/family/raw vendor ID, Vulkan device type, Android release, SDK, security patch, VulkanScope version/versionCode, application ABI and report ID.
- Added Report sorting for newest/oldest submission, ascending/descending driver version, Vulkan API, GPU name, vendor, Android version and VulkanScope version.
- Added pagination with 10, 25 or 50 reports per page and Previous/Next navigation; 50 is the hard UI maximum per page.
- Added submission timestamp, driver version and device API metrics to report detail headers and full Overview metadata.
- Fixed duplicate submissions so the API returns the original persisted D1 submission time instead of a newly generated request time.
- Versioned the changed JavaScript and CSS assets as v0312 to prevent stale GitHub Pages/browser caches.

## 0.31.1
- Added dedicated Devices, Versions, Properties, Features, Formats, Memory, Queues, Surface, Extensions, Instance and Profiles aggregate views.
- Added detailed per-report tabs for overview, properties, features, formats, memory, queues, surface, extensions, instance, profiles and raw report.
- Added complete parsing for memory heaps/types, queue families, formats, WSI/surface formats, present modes, presentation queues, instance layers/extensions, device layers and Vulkan Profile results.
- Kept supported, unsupported, available, unavailable and unknown distinct.
- Added bounded concurrent report loading and coverage summaries based only on loaded reports.
- Preserved original reportText for complete raw inspection and future parser improvements.


## 0.31.1
- Fingerprinted favicon, CSS and JavaScript assets to prevent stale GitHub Pages/browser cache from retaining 0.31.0 UI.
- Favicon regenerated directly from the application Vulkan tab icon on a black background.
- Vendor filter now canonicalizes decimal/hex vendor IDs and maps Qualcomm to Adreno, Arm to Mali, Imagination to PowerVR, Samsung to Xclipse, NVIDIA to GeForce, AMD to Radeon and Broadcom to VideoCore where vendor identity makes the family unambiguous.
- Added a separate GPU-model filter using the exact submitted GPU name.
- Added frontend report-text normalization fallback so detailed views remain populated even when the Worker normalizer has not yet been redeployed.
- Fixed profile parsing so Device # lines inside VULKAN PROFILE EVALUATION no longer terminate the profile section.
- Added Registry detail tab and per-tab counts.


## 0.33.4
- Fixed report-detail tab active-state regression where Overview remained visually selected after changing tabs.
- Centralized detail-tab UI synchronization from `state.detailTab`.
- Added `aria-selected`/tab focus semantics and automatic visibility scrolling for the active tab on narrow layouts.
- Audited similar stale-active-state paths without changing Vulkan data semantics.


## 0.34.0
- Custom selector System-driver choices now bold only the GPU model name for consistency with report/device tables.
- Preserved Turnip / third-party red emphasis and native-select accessibility/state semantics.
- Re-ran frontend, Worker, security, performance and Vulkan-data regression audits.

## 0.34.5
- Display/HDR now identifies Android device models instead of GPUs and never renders GPU logos in that view.
- Empty HDR capability lists render as Unavailable.
- Added local HDR logo chips for explicitly reported Dolby Vision, Dolby Vision 2, HDR10, HDR10+, HDR10+ Advanced and HDR Vivid types.
