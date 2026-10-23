# VulkanScope Database 0.33.1 audit

- Memory rendering decodes VkMemoryPropertyFlags and VkMemoryHeapFlags from VulkanScope 0.32.2 structured numeric masks and keeps raw masks visible.
- The bit-name mapping follows current Khronos VkMemoryPropertyFlagBits and VkMemoryHeapFlagBits; unknown future bits are retained in hex.
- Schema-v3 technicalReport is used as the lossless source for memory, queues, formats, extensions, instance data, Surface diagnostics and registry coverage where present; TXT remains fallback compatibility.
- Database header metadata now distinguishes Vulkan-Headers 1.4.360 compile baseline from the validated Vulkan 1.4.357 / CapsViewer 4.12 runtime query catalog.
- Top navigation buttons are smaller, start with a controlled gap after the VulkanScope logo, and collapse to the menu at 1420 px to prevent the final tab from clipping. Mobile/portrait geometry was tightened without changing content architecture.
- Status semantic colors remain supported=green, unsupported=red, available=blue, unavailable=amber, unknown=gray.
