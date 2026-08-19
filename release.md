# VulkanScope Database 0.34.4

- Restores smooth, compositor-only transitions between primary database sections.
- Uses token-gated Web Animations API transitions so rapid mouse/touch navigation cannot commit stale views.
- Honors `prefers-reduced-motion`.
- Fixes numeric Vulkan API-version ordering in filters, Devices and Versions.
- Re-audited VulkanScope 0.32.6 structured-report compatibility, canonical/raw Vulkan presentation, CapsViewer category parity, security and performance.

- Adds a Display / HDR aggregate view and report-detail tab for VulkanScope 0.32.6 schema-v3 display data.
- Preserves and displays instance/device layer extension lists.
- Clarifies global Vulkan baseline metadata as a VulkanScope producer/query baseline rather than an assertion about the latest Khronos publication.
