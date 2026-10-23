CREATE TABLE IF NOT EXISTS reports (
 id TEXT PRIMARY KEY,
 submitted_at TEXT NOT NULL,
 schema_version INTEGER NOT NULL,
 gpu_name TEXT NOT NULL,
 vendor_id TEXT NOT NULL,
 device_id TEXT NOT NULL,
 driver_mode TEXT NOT NULL,
 driver_version TEXT NOT NULL,
 device_api_version TEXT NOT NULL,
 manufacturer TEXT NOT NULL,
 model TEXT NOT NULL,
 payload_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_reports_gpu ON reports(gpu_name);
CREATE INDEX IF NOT EXISTS idx_reports_driver ON reports(driver_mode, driver_version);
CREATE INDEX IF NOT EXISTS idx_reports_api ON reports(device_api_version);
