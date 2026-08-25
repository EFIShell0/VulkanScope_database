# VulkanScope Database 0.39.8

VulkanScope Database 0.39.8 is the companion release for VulkanScope 0.41.10. It consumes a complete, bounded Image Format Properties2 tuple-state ledger without mixing that ledger into normal Properties & Limits counts.

## Image Format Properties2 semantics
For every format actually scheduled by VulkanScope 0.41.10, the producer reports LINEAR and OPTIMAL states for the base query, OPAQUE_FD and ANDROID_HARDWARE_BUFFER. The Database keeps four exact states: Available, Unsupported, Unavailable and Not applicable.

Available means the exact query returned `VK_SUCCESS` and the successful full property payload remains normal detailed-property evidence. Unsupported is reserved for `VK_ERROR_FORMAT_NOT_SUPPORTED` (-11). Other non-zero Vulkan results are Unavailable. An external variant is Not applicable only when its prerequisite device extension was not enumerated; no GPU-name or driver-name inference is used.

The Worker requires canonical unique tuple names, six slots per scheduled format, exact prerequisite reasons and consistency with aggregate query diagnostics. This prevents a scheduled current-producer tuple from silently becoming `Unknown / Not reported` downstream.

## Compatibility
- Submission schema: 2
- technicalReport: 3
- Normalizer: 15
- Current producer: VulkanScope 0.41.10 / versionCode 420
- Vulkan producer/query baseline: 1.4.360
- Compatible producer floor: VulkanScope 0.32.4+
- D1 migration: none
- Existing stored-report rewrite: none

Historical 0.41.9 and 0.41.8 reports retain their original evidence semantics.
