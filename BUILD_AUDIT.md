# VulkanScope Database 0.36.3 Build Audit

Release focus: Compare metadata-noise filtering without changing technical capability evidence.

Release gates:
- Static database audit
- Frontend JavaScript syntax
- Worker JavaScript syntax
- Worker contract tests
- Technical compare filter regression checks
- Static index build
- ZIP integrity

Expected semantics:
- applicationVersion/applicationVersionCode/submittedAt are non-technical Compare metadata
- Vulkan/driver/Android/ABI/device/memory/queue/Surface/format/extension/capability/Display-HDR/profile data remain technical
- no stored report mutation or D1 migration
