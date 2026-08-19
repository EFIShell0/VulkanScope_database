# VulkanScope Database 0.34.1

## Fixed

- Custom selection menus now render System Vulkan driver GPU model names in explicit strong white text.
- Driver mode/version suffixes remain muted and normal-weight.
- Hover, focus and selected row styles no longer flatten the GPU-name emphasis.
- Turnip / third-party styling is unchanged.

# VulkanScope Database 0.34.0

## UI consistency
- GPU model names in report-backed tables now use the same strong emphasis as the Reports view.
- Main navigation switches use a short compositor-friendly opacity/translate transition with a stale-transition token gate and reduced-motion support.

## Audit and fixes
- Re-audited normalized Vulkan semantics, canonical/raw flag presentation, structured-report compatibility, Worker input validation and frontend CSP/security posture.
- Rechecked the current Vulkan Hardware Database category tree; no additional technical category was copied by inference.
- Preserved the 104 px mobile report-detail sticky-tab offset required by the two-row header.


### 0.34.0
Custom-listbox GPU-name emphasis consistency and full regression/security audit.
