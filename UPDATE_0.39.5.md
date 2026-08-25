# Updating to VulkanScope Database 0.39.5

Replace the repository contents with the 0.39.5 release, run `python tools/repair_repository.py --apply`, audit with `python tools/audit_database.py --source-tree .`, then commit deletions with `git add -A`. Do not retain an older `assets/app.v*.js` or an extra Pages workflow.
