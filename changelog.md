# VulkanScope Database 0.39.1

- Updated the current producer identity to VulkanScope 0.41.5 / versionCode 415.
- Made the strict 0.41.4 query-diagnostic and queue/Vulkan Video validation contract version-range aware so it also applies to 0.41.5 and future compatible producers.
- Kept unavailable/not-applicable/unknown Vulkan Video numeric masks fail-closed as null while preserving genuine queried zero masks.
- Kept device-extension, extended-query and Vulkan 1.4 diagnostic states fail-closed to the existing allow-listed evidence vocabulary.
- Preserved VulkanScope 0.32.4+ compatibility, schema 2, technicalReport 3, normalizer 15, report hashes and existing D1 rows.
- Preserved the 0.39.0 filter/statistics/hash-routing frontend; only producer metadata was cache-busted to `app.v0391.js` / `config.js?v=0391`.
