# VulkanScope Database 0.33.3

- Decode and display canonical VkMemoryPropertyFlags/VkMemoryHeapFlags names while retaining raw masks.
- Prefer VulkanScope 0.32.2 schema-v3 technicalReport structured data when present.
- Distinguish Vulkan-Headers 1.4.360 compile baseline from validated Vulkan 1.4.357/CapsViewer 4.12 query coverage.
- Compact top navigation, add controlled logo-to-nav spacing, and collapse earlier to prevent the final tab clipping.
- Tighten portrait/mobile header geometry and preserve horizontal scrolling inside wide technical tables.

# VulkanScope Database 0.33.3

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


## 0.33.3
- Fixed report-detail tab active-state regression where Overview remained visually selected after changing tabs.
- Centralized detail-tab UI synchronization from `state.detailTab`.
- Added `aria-selected`/tab focus semantics and automatic visibility scrolling for the active tab on narrow layouts.
- Audited similar stale-active-state paths without changing Vulkan data semantics.
