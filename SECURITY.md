# Security and data policy

The public database contains technical Vulkan capability information only.

Do not publish IMEI, Android ID, device serial numbers, MAC addresses, user/account identifiers, private file paths, authentication tokens or IP addresses as report fields.

The site has no third-party JavaScript, analytics, remote fonts or advertising dependencies. Its Content Security Policy permits same-origin resources and the configured VulkanScope Worker API only.

Unknown, unsupported and unavailable capability states remain distinct. Missing query data is never inferred as unsupported without direct evidence.

## 0.33.8 submission hardening

The Worker accepts report submissions only as `application/json`. The outer schema must identify the producer as VulkanScope (`com.efishell.vulkanscope`) and `collection.status` must be `available`; incomplete collection submissions are rejected. Existing payload-size, forbidden-field, D1 parameter binding and no-request-IP-storage controls remain in force.

## 0.34.0 audit

No new network permission or third-party dependency was added. The UI-only transition and GPU-name styling changes retain the existing CSP, JSON submission validation, D1 parameterization, payload limits and no-IP-storage rules.
