# VulkanScope Database 1.0.11 build / regression audit

## Release identity
- Database version: 1.0.11
- Immutable predecessor: VulkanScope Database 1.0.10
- Predecessor ZIP SHA-256: `6d18b5378235a5ff556576ff9d2d91ff5608dcea8076bc17ef0f32d12ec08aa4`
- Current producer/query baseline: VulkanScope 1.0.19 / versionCode 1019 / Vulkan 1.4.362
- New-submission floor: VulkanScope 1.0.19
- Submission schema 2 / technicalReport 3 / normalizer 16
- D1 migration: none

## Failure and correction
The 1.0.10 GitHub Actions build failed in `Reverify generated index metadata` because a second Python line was indented beneath a scalar `run:` value instead of being contained in `run: |`. The runner therefore passed the second command text as arguments to the verifier and exited with argparse code 2.

1.0.11 makes the command boundary explicit in both workflow copies, preserves byte equality between the canonical template and deployed workflow, and adds a negative mutation that reproduces and rejects the exact malformed form.

## Retained behavior
The 1.0.10 Reports Array/table contract and all 1.0.9 live consistency, stacked server-time, full Report ID copy, low-percentage visualization and VulkanScope 1.0.19 floor behavior are retained. No D1 migration, stored-report rewrite, report-hash rewrite, schema/normalizer change or Vulkan registry change is introduced.

## Required evidence
- `tools/verify_1_0_11_workflow_command_boundary.py`
- `tools/test_1_0_11_workflow_command_boundary_negative_mutations.py`
- aggregate `tools/quality_gate.py`
- immutable 1.0.10 -> 1.0.11 source-overlay and strict-package regression verification
- clean-extract current verifier + negative mutation
- deterministic release ZIP construction

Live Cloudflare deployment and remote production D1 smoke testing are not executed by this packaging environment.
