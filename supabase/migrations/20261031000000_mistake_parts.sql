-- "Troba l'error" pas a pas: documents and sessions have a layout ('sencer', every existing row, or 'per_parts');
-- a per-parts session is graded part by part, each part once, and records the parts whose hint was used.
ALTER TABLE mistake_exercises ADD COLUMN layout VARCHAR(16) NOT NULL DEFAULT 'sencer';
ALTER TABLE mistake_sessions ADD COLUMN layout VARCHAR(16) NOT NULL DEFAULT 'sencer';

CREATE TABLE mistake_part_gradings (
	id SERIAL NOT NULL,
	session_id VARCHAR(64) NOT NULL,
	part INTEGER NOT NULL,
	hint_used BOOLEAN NOT NULL,
	created_at FLOAT NOT NULL,
	annotations JSONB NOT NULL,
	result JSONB NOT NULL,
	PRIMARY KEY (id),
	UNIQUE (session_id, part),
	FOREIGN KEY(session_id) REFERENCES mistake_sessions (id) ON DELETE CASCADE
);
ALTER TABLE mistake_part_gradings ENABLE ROW LEVEL SECURITY;

CREATE TABLE mistake_part_hints (
	session_id VARCHAR(64) NOT NULL,
	part INTEGER NOT NULL,
	created_at FLOAT NOT NULL,
	PRIMARY KEY (session_id, part),
	FOREIGN KEY(session_id) REFERENCES mistake_sessions (id) ON DELETE CASCADE
);
ALTER TABLE mistake_part_hints ENABLE ROW LEVEL SECURITY;
