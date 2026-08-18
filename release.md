# VulkanScope Database 0.33.5

UI refinement, report-comparison parity and regression-audit release.

- Database filters now use a VulkanScope-styled custom listbox layer instead of exposing browser-native option UI. The underlying native select remains authoritative and keyboard, mouse and touch interaction are preserved.
- The primary navigation no longer exposes a horizontal scrollbar. Dedicated left/right controls, subtle edge fades, touch/trackpad scrolling and mouse-wheel scrolling keep every tab reachable without covering labels.
- Added a compact link to the official VulkanScope GitHub repository in the Vulkan Hardware Database hero.
- Expanded Compare to include device metadata, normalized properties/features, device and instance extensions, formats, queue families, memory, Surface/WSI and Vulkan Profiles when those categories exist in the selected reports.
- Re-audited the current Vulkan Hardware Database category structure and preserved Core 1.0–1.4, extension, format, memory, queue, Surface, instance, portability and profile detail coverage.
- Fixed a stale footer version label and a custom-status-filter visibility regression found during the 0.33.5 audit.
- VulkanScope 0.32.4/0.32.5 schema-v3 compatibility, Vulkan 1.4.360 canonical decoding, exact-width masks and Supported/Unsupported/Available/Unavailable/Unknown semantics are unchanged.
