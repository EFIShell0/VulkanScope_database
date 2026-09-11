# VulkanScope Database 1.0.17

- Fixes the inconsistent high-percentage coverage glow across every aggregate tab. Coverage bars at 80% or higher now use a valid percentage-valued endpoint anchored to a positioned bar, plus a persistent semantic halo and animated particle spray; 100% bars no longer lose the endpoint effect.
- Preserves dominant/subordinate ranking, lower-share hatching, zero-percent hatched-empty tracks and all Supported / Unsupported / Available / Unavailable / Not applicable / Unknown semantics.
- Extends the Versions report-count table with the same GPU identity treatment used by Devices: bold GPU name, vendor logo and canonical vendor/family/raw-ID text, while retaining the Statistics-style circular GPU/version chart and keeping coverage bars out of Versions.
- Adds shared bounded pagination to Coverage Reports and Distinct/value modals: 10 / 25 / 50 rows per page, maximum 50 visible rows, explicit range/page text, Previous/Next controls and a visible vertical scrollbar inside the modal.
- Preserves live report synchronization, database-version refresh notification, Submitted/Vendor/Type disclosures, Developer Info, raw vendor-ID provenance, HDR10+ artwork, Display/HDR chips, loading accents, soft motion and reduced-motion behavior.
- Advances release/browser identity to 1.0.17 / `assets/app.v1017.js` / cache key 1017. No D1 migration or report rewrite is required.
