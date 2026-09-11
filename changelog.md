# VulkanScope Database 1.0.16

- Widens the Reports Submitted, Vendor and Type right-growing disclosures so complete time-zone, vendor/family/raw-ID and canonical physical-device-type values fit without clipping; compact three-line controls remain physically pinned to the left.
- Converts aggregate `distinct`/value drill-downs from inline downward accordions to the same right-arrow, centered dark-backdrop modal language used by Coverage reports.
- Reworks Versions into the Statistics donut-chart language. Each slice represents a GPU + selected Vulkan version cohort, while the table below lists GPU, version, exact report count and share; no coverage bars are used.
- Adds bounded live database synchronization every 10 seconds plus immediate checks when the page regains visibility, focus or connectivity. New report payloads are fetched only when missing, then the report universe is swapped atomically and all visible statistics/views are refreshed.
- Adds `databaseVersion` to Worker health/report-index metadata. When a newer Database frontend release is detected, the current page shows a centered dark update dialog with a `Refresh now` button instead of silently hot-swapping code.
- Preserves 1.0.15 coverage-state ranking/hatching, zero-state tracks, Developer Info, vendor-ID provenance, Coverage reports modal, HDR10+ asset fidelity, Display/HDR chips, loading accents, soft interaction motion and reduced-motion behavior.
- Advances release/browser identity to 1.0.16 / `assets/app.v1016.js` / cache key 1016. No D1 migration or report rewrite is required.
