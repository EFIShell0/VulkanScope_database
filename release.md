# VulkanScope Database 0.34.7

## Display / HDR filter correction

The Display / HDR view no longer exposes or applies the Vulkan API-version filter. Android display/HDR capability is device/display metadata and must not be hidden by an unrelated Vulkan physical-device API filter. Vendor and GPU filters remain disabled there as before; the meaningful state filter remains available/unavailable.

All 0.34.6 HDR logo, security and schema-compatibility behavior is preserved.
