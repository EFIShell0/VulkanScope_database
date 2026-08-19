# VulkanScope Database 0.33.9

## UI consistency
- GPU model names in report-backed tables now use the same strong emphasis as the Reports view.
- Main navigation switches use a short compositor-friendly opacity/translate transition with a stale-transition token gate and reduced-motion support.

## Audit and fixes
- Re-audited normalized Vulkan semantics, canonical/raw flag presentation, structured-report compatibility, Worker input validation and frontend CSP/security posture.
- Rechecked the current Vulkan Hardware Database category tree; no additional technical category was copied by inference.
- Preserved the 104 px mobile report-detail sticky-tab offset required by the two-row header.
