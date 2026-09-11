# VulkanScope Database changelog

## 1.0.19
- Makes glow/spray follow the greatest non-zero coverage state in each grouped row rather than an arbitrary 80% cutoff; lower non-zero states remain hatched and zero remains empty.
- Stops treating a newly deployed Worker version as proof that a frontend release is ready. Update prompts now come only from the published same-origin release marker.
- Changes release publication ordering so main pushes verify/build only; tag workflows create/refresh the GitHub Release first and publish GitHub Pages only after that release succeeds.
- Refresh now uses a cache-busting navigation to prevent stale-page refresh loops.

## 1.0.18
- Fixes the Coverage Reports / Distinct modal page-size control so its 10/25/50 custom option menu opens upward and remains usable within the bounded dialog rather than being clipped below the footer.
- Restores Android robot artwork to the official online green `#3DDC84` with neutral dark details and prevents generic UI tinting from replacing the intrinsic colors.
- Adds a Statistics/Versions-style circular GPU/report distribution to Devices, plus a separate exact table with bold GPU name, vendor logo, vendor/family/raw ID, maximum device API, driver variants, report count and share.
- Replaces the stale historical Database audit implementation with a current 1.0.18 source + staged-Pages audit covering release identity, package hygiene, current Vulkan/schema locks, security/resource ceilings, syntax/contracts and D1 migration replay.
- Preserves 1.0.17 coverage glow/hatching, paged evidence modals, live synchronization/version refresh, report disclosure layout, vendor-ID provenance, HDR/display presentation, schema 2 / technicalReport 3 / normalizer 16 and the existing D1 storage model.

## 1.0.17
- Stabilizes >=80% semantic coverage glow/spray positioning across aggregate tabs, including exactly 100%.
- Adds Devices-parity GPU identity to the Versions exact-count table.
- Adds bounded scrollbar + 10/25/50 pagination to Coverage Reports and Distinct/value dialogs.
