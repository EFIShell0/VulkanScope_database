# VulkanScope Database 0.39.7

VulkanScope Database 0.39.7 is the companion release for VulkanScope 0.41.9. It keeps successful Image Format Properties2 properties in normal property/query evidence while consuming non-success tuple outcomes from a separate bounded dataset, so exact Unsupported/Unavailable comparison remains possible without inflating Properties & Limits totals. Schema 2, technicalReport 3, normalizer 15, Vulkan 1.4.360 and existing D1 storage remain unchanged.

## 0.39.7 Image Format Properties2 outcome separation

VulkanScope 0.41.9 keeps successful Image Format Properties2 property payloads in normal detailed-property evidence but moves non-success tuple results into a dedicated bounded `imageFormatQueryResults` array. Database 0.39.7 consumes that array for report detail and Compare without treating hundreds of negative tuple outcomes as Vulkan property rows.

