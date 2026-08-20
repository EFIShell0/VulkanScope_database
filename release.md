# VulkanScope Database 0.35.0

## Full database audit
- Corrected Compare field mapping for VulkanScope schema-v2 GPU device type and loader/instance API version.
- Corrected property/limit state normalization so queried scalar values such as `false` and `0` remain Available instead of being mislabeled Unsupported. Feature booleans keep Supported/Unsupported semantics.
- Expanded TXT fallback normalization for queue video codec operations and registry coverage.
- Corrected fallback memory flag rendering.
- Added streaming 2 MiB Worker request-body enforcement and stronger nested schema checks; Worker normalizer is version 8.
- Made report de-duplication stable across JSON object key ordering and bounded canonicalization depth.
- Added a visible report-load-failure metric when individual report detail fetches fail.
- Clarified Android Display preferred wide-gamut color-space labeling.
- Re-checked canonical Vulkan color-space/queue/memory/format flag presentation against the current published Khronos specification while keeping VulkanScope's independent producer/query baseline labeled separately.
- Preserved all 0.34.9 Compare/Portability density and 0.34.8 filter/HDR ordering behavior.
