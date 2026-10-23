# Updating to VulkanScope Database 0.39.7

Deploy this repo-root package over the repository, then run `python tools/repair_repository.py --apply` and `python tools/audit_database.py --source-tree .`. The repair step removes stale versioned frontend assets/workflows without touching `.git`. Stage deletions with `git add -A`.
