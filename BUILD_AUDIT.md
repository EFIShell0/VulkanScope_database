# VulkanScope Database 0.39.17 build / regression audit

Immutable predecessor: VulkanScope Database 0.39.16 ZIP SHA-256 `0428aff0568bf4124f9cce94c18c951a788b6c0e19a2757d5f172067d1228aed`. Current producer/query baseline: VulkanScope 0.41.42 / versionCode 452; Vulkan registry 1.4.361; schema 2 / technicalReport 3; normalizer 16.

The supplied real report comparison demonstrated a presentation-only Surface state defect: generic diagnostic false/NO values and failed Surface presentation evidence could be rendered Unsupported. 0.39.17 preserves Surface query status/reason, uses availability semantics for generic Surface values, and requires successful query evidence before negative presentation capability becomes Unsupported.

No D1 migration, stored report rewrite, report-hash rewrite, normalizer bump or Worker validation weakening is introduced.

Local source/package gates are recorded only after execution. Cloudflare Worker deployment and production runtime smoke tests remain separate evidence classes and are NOT EXECUTED by the packaging environment.
