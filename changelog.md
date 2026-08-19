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
