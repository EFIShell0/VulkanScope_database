# VulkanScope Database 4.0.13 — Microsoft Edge Add-ons setup

- Replaced the owner-provided Google Drive PC extension ZIP link with the official JXL-RS Edge listing: 
  https://microsoftedge.microsoft.com/addons/detail/jxlrs-edge/fnbbljgfpgabbhjjmhjjpkphpmfaheph
- Desktop Edge installation uses Get → Add extension, then verifies the extension is enabled and reloads the Database. No developer mode, unpacked ZIP or CRX required.
- Android Edge instructions now use the in-app Extensions catalog *if* the extension is presented as installable. Store listing does not imply mobile compatibility; no Android sideload is promised.
- Updated both the conditional browser warning and standalone JPEG XL warning. Retained first-party native 2x2 JXL decoded-image / extension released visible canvas proof and 1.8–4.8 s bounded startup behavior.
- Advanced versioned frontend assets, release/bootstrap handshake, Worker metadata, deterministic distribution, CI, and audited install script to 4.0.13, with unmodified v4012 JS bridge and original report/registry/D1 identity contracts.
- Source QA is not live browser, mobile extension, or deployment certification. No Worker/D1 deployment or report mutation performed.
