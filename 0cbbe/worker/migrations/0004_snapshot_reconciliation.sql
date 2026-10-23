-- Durable snapshot refresh cursor: stays independent from report admission.
CREATE TABLE IF NOT EXISTS snapshot_refresh_control (
 id INTEGER PRIMARY KEY CHECK(id=1),
 queued_report_id TEXT NOT NULL DEFAULT '',
 queued_at TEXT NOT NULL DEFAULT '',
 last_dispatched_report_id TEXT NOT NULL DEFAULT '',
 last_dispatched_at TEXT NOT NULL DEFAULT '',
 last_published_report_id TEXT NOT NULL DEFAULT '',
 last_published_at TEXT NOT NULL DEFAULT '',
 last_error_code TEXT NOT NULL DEFAULT ''
);
INSERT OR IGNORE INTO snapshot_refresh_control(id) VALUES(1);
