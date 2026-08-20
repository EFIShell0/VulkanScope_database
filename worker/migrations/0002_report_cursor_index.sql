CREATE INDEX IF NOT EXISTS idx_reports_submitted_id ON reports(submitted_at DESC, id DESC);
