# VulkanScope Database 0.39.24 final source audit

## Release identity
- Database version: 0.39.24
- Immutable predecessor: VulkanScope Database 0.39.23
- Predecessor ZIP SHA-256: `d53b6f971d73f6f1ebe6a9ea7ae9ad7dee387c8321c5c5bf5dfb2704b06cfeab`
- Predecessor census: 191 files
- Current producer/query baseline: VulkanScope 0.80.10 / Vulkan 1.4.362
- New-submission floor: VulkanScope 0.80.3
- Submission schema: 2
- technicalReport schema: 3
- normalizer: 16
- D1 migration: none

## Vulkan 1.4.362 / Encyclopedia
The Database uses the same supplied locked Vulkan 1.4.362 `vk.xml` as the application, SHA-256 `cf31c965cf6e788697139601da0c7e02a75a9b6c7ac764e7641f5521ffd9da06`, with header provenance 362 and Vulkan-Headers commit `ee2ec5fd83dafce291024683b50dc89219333076`.

The offline Database Encyclopedia is regenerated deterministically to 842 commands, 6248 `VK_*` tokens, 2461 `Vk*` types, 476 extensions and 50 VkResult entries. Visible Encyclopedia copy now identifies Vulkan 1.4.362 rather than retaining stale 1.4.361 wording.

## Producer compatibility correction
Historical new-submission compatibility remains VulkanScope 0.80.3 through 0.80.9 with their locked 1.4.361 registry/header contract. VulkanScope 0.80.10 and later compatible producers are validated against the 1.4.362 registry/header identity. This prevents a valid 0.80.10 report from being rejected merely because the previous Database validator still required the 1.4.361 collector baseline for every 0.80.3+ producer.

The 0.80.3 floor remains fail-closed. 0.80.2 and older new submissions are rejected. Historical stored reports remain readable and are not rewritten or rehashed.

## Regression evidence
The 1.4.362 verifier fails against immutable Database 0.39.23 with version checking disabled and passes on 0.39.24. Its negative-mutation suite rejects registry provenance drift, the 0.80.10 registry-contract branch being forced back to 1.4.361, Encyclopedia corpus drift and generator census drift; an unrelated changelog wording change is accepted as the false-positive control.

The Worker contract includes both a positive VulkanScope 0.80.10 / Vulkan 1.4.362 submission and a negative 0.80.10 payload that falsely claims the older 1.4.361 collector baseline. Historical 0.80.9 / 1.4.361 and minimum 0.80.3 submissions remain accepted under their existing contract.

The complete source `tools/quality_gate.py` is required before packaging and includes UTF-8/tooling checks, immutable regression, source audit/hygiene, route/Compare/Surface contracts, loading/scroll/floor behavior, Database Encyclopedia, 1.4.362 verifier and negative mutations, Worker contract, D1 migration replay and Pages artifact audit.

## Deployment boundary
Live Cloudflare Pages/Worker/D1 deployment is NOT EXECUTED in this packaging environment. The release package is deploy-ready source only.
