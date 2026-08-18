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
