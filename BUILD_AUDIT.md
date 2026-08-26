# VulkanScope Database 0.39.9 Build / Release Audit

- Database: 0.39.9.
- Current producer: VulkanScope 0.41.11 / versionCode 421.
- Vulkan producer/query baseline: 1.4.360.
- Submission schema: 2; technicalReport schema: 3; normalizer: 16.
- D1 schema and stored payload/hash contract are unchanged; no migration is required.
- Generic zero masks render as numeric 0 rather than an invented VK_NONE.
- Compare separates whole-format support from linear/optimal/buffer mask query values.
- Not applicable remains distinct from Unavailable and Unknown in normalization and Compare.
- Image Format Properties2 preserves exact tuple-state semantics and historical compatibility.
- Repository-state, source audit, audit-hygiene, frontend/Worker syntax, routes, Compare, Worker contract and staged Pages artifact gates passed.
