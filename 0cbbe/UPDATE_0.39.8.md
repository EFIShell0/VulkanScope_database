# Updating to VulkanScope Database 0.39.8

Update the repository from the 0.39.8 source ZIP at repository root, then run:

```text
python tools/repair_repository.py --apply
python tools/audit_database.py --source-tree .
node tools/test_compare_contract.mjs
node worker/tests/contract.mjs
```

0.39.8 uses `assets/app.v0398.js` and `config.js?v=0398`. The repair tool removes stale versioned app JavaScript and restores the canonical Pages workflow.

No D1 migration or stored-report rewrite is required. The Worker remains schema 2 / technicalReport 3 / normalizer 15 and adds fail-closed VulkanScope 0.41.10 complete Image Format Properties2 tuple-state validation.
