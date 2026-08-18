# Changelog
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
