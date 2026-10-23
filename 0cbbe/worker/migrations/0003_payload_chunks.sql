CREATE TABLE IF NOT EXISTS report_payload_chunks (
 report_id TEXT NOT NULL,
 chunk_index INTEGER NOT NULL,
 payload_chunk TEXT NOT NULL CHECK (length(CAST(payload_chunk AS BLOB)) <= 1000000),
 PRIMARY KEY (report_id, chunk_index),
 FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_report_payload_chunks_report ON report_payload_chunks(report_id, chunk_index);
