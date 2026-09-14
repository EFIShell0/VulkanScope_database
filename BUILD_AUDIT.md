# VulkanScope Database 1.3.6 build / regression audit

## Scope

Database 1.3.6 is a presentation/export-only successor to immutable Database 1.3.5 (ZIP SHA-256 `92c86c9013f4bab4ea8376e5db07c965b035843313c893561b047957e5189e97`). D1 schema/migrations, stored report payload bytes/hashes, canonical report IDs, normalizer 16, Vulkan 1.4.362/header 362, VulkanScope 1.2.5 submission floor and validated browser floors are unchanged.

## Report-detail workspace redesign

The established Overview tab is intentionally retained. Registry, Properties, Limits, Features, Formats, Memory, Queues, Surface, Display & HDR, Extensions, Instance, Profiles and Raw report now use a common evidence-workspace visual language with section identity surfaces, bounded summary metrics, clear evidence cards and explicit empty states. Each category still renders its own native evidence and canonical Vulkan/raw values; the redesign does not collapse query availability into returned values or infer unsupported state from missing evidence.

Existing local table-scroll controls remain authoritative for wide technical tables. Responsive rules constrain the new headers, statistics, panel headings, raw values and controls on desktop/mobile without introducing document-level horizontal scrolling. Decorative transitions remain short and are disabled by `prefers-reduced-motion`.

## Raw report

Raw report now explains that `reportText` is the preserved human-readable source evidence beside normalized/structured data. **Download raw report** builds a local `text/plain;charset=utf-8` Blob directly from the stored `reportText` string and downloads it without newline insertion, line-ending normalization, network export, D1 mutation or report-identity changes.

The Raw report text host is registered with the same first-party demand-driven surface-scrollbar system used by Settings, listboxes and dialogs. Native scrollbar chrome is hidden only after enhancement and the themed rail appears only for real overflow.

## Release identities

- Database / frontend / Worker: 1.3.6
- Current app: `assets/app.v1306.js`
- Current browser gate: `assets/browser-compat.v1306.js`
- Current release bootstrap: `assets/release-bootstrap.v1306.js`
- Cache key: 1306
- Immediate CDN transition bridge: immutable 1.3.5 app/browser/bootstrap triplet only
- Immutable predecessor ZIP: Database 1.3.5, SHA-256 `92c86c9013f4bab4ea8376e5db07c965b035843313c893561b047957e5189e97`

## Mandatory release gates

`tools/quality_gate.py` runs repository repair/check, immutable 1.3.5 regression verification, the 1.3.6 focused verifier and negative mutations, source audit, JavaScript syntax/Worker contract checks, D1 migration replay, Pages allow-list staging and the release-ready transition audit. The packaging tool creates a deterministic ZIP and reruns strict regression/source/1.3.6 verification against a clean extraction.
