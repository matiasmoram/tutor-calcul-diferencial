-- Initial schema of the DDD backend (snapshot of supabase/schema.sql when it was introduced).

CREATE TABLE llm_calls (
	id SERIAL NOT NULL, 
	session_id VARCHAR(64), 
	turn INTEGER, 
	created_at FLOAT NOT NULL, 
	stage VARCHAR(32) NOT NULL, 
	model VARCHAR(96) NOT NULL, 
	ok BOOLEAN NOT NULL, 
	latency_ms INTEGER, 
	input_tokens INTEGER, 
	output_tokens INTEGER, 
	cached_tokens INTEGER, 
	error VARCHAR, 
	response JSONB, 
	system VARCHAR, 
	prompt VARCHAR, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_llm_calls_created_at ON llm_calls (created_at);
CREATE INDEX ix_llm_calls_session_id ON llm_calls (session_id);
ALTER TABLE llm_calls ENABLE ROW LEVEL SECURITY;

CREATE TABLE mistake_exercises (
	id VARCHAR(16) NOT NULL, 
	source_kind VARCHAR(16) NOT NULL, 
	source_id VARCHAR(64) NOT NULL, 
	difficulty VARCHAR(16) NOT NULL, 
	created_at FLOAT NOT NULL, 
	data JSONB NOT NULL, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_mistake_exercises_source ON mistake_exercises (source_id, difficulty);
ALTER TABLE mistake_exercises ENABLE ROW LEVEL SECURITY;

CREATE TABLE problem_sheets (
	id VARCHAR(64) NOT NULL, 
	position INTEGER NOT NULL, 
	data JSONB NOT NULL, 
	PRIMARY KEY (id)
);
ALTER TABLE problem_sheets ENABLE ROW LEVEL SECURITY;

CREATE TABLE quizzes (
	id VARCHAR(32) NOT NULL, 
	source_id VARCHAR(64) NOT NULL, 
	difficulty VARCHAR(16) NOT NULL, 
	topic INTEGER NOT NULL, 
	created_at FLOAT NOT NULL, 
	data JSONB NOT NULL, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_quizzes_source_difficulty ON quizzes (source_id, difficulty);
ALTER TABLE quizzes ENABLE ROW LEVEL SECURITY;

CREATE TABLE theory_items (
	id VARCHAR(32) NOT NULL, 
	topic INTEGER NOT NULL, 
	kind VARCHAR(24) NOT NULL, 
	number INTEGER, 
	position INTEGER NOT NULL, 
	data JSONB NOT NULL, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_theory_items_topic ON theory_items (topic);
ALTER TABLE theory_items ENABLE ROW LEVEL SECURITY;

CREATE TABLE topics (
	number SERIAL NOT NULL, 
	title VARCHAR NOT NULL, 
	data JSONB NOT NULL, 
	PRIMARY KEY (number)
);
ALTER TABLE topics ENABLE ROW LEVEL SECURITY;

CREATE TABLE tutor_sessions (
	id VARCHAR(64) NOT NULL, 
	exercise_id VARCHAR(32) NOT NULL, 
	created_at FLOAT NOT NULL, 
	updated_at FLOAT NOT NULL, 
	closed BOOLEAN NOT NULL, 
	version INTEGER NOT NULL, 
	turn_started_at FLOAT, 
	state JSONB NOT NULL, 
	history JSONB NOT NULL, 
	PRIMARY KEY (id)
);
CREATE INDEX ix_tutor_sessions_exercise_id ON tutor_sessions (exercise_id);
CREATE INDEX ix_tutor_sessions_updated_at ON tutor_sessions (updated_at);
ALTER TABLE tutor_sessions ENABLE ROW LEVEL SECURITY;

CREATE TABLE exercises (
	id VARCHAR(32) NOT NULL, 
	sheet_id VARCHAR(64) NOT NULL, 
	problem INTEGER NOT NULL, 
	part VARCHAR(8), 
	position INTEGER NOT NULL, 
	data JSONB NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sheet_id) REFERENCES problem_sheets (id) ON DELETE CASCADE
);
CREATE INDEX ix_exercises_sheet_id ON exercises (sheet_id);
ALTER TABLE exercises ENABLE ROW LEVEL SECURITY;

CREATE TABLE mistake_sessions (
	id VARCHAR(64) NOT NULL, 
	source_kind VARCHAR(16) NOT NULL, 
	source_id VARCHAR(64) NOT NULL, 
	exercise_id VARCHAR(16) NOT NULL, 
	difficulty VARCHAR(16) NOT NULL, 
	created_at FLOAT NOT NULL, 
	grading_started_at FLOAT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(exercise_id) REFERENCES mistake_exercises (id)
);
CREATE INDEX ix_mistake_sessions_source_id ON mistake_sessions (source_id);
ALTER TABLE mistake_sessions ENABLE ROW LEVEL SECURITY;

CREATE TABLE quiz_sessions (
	id VARCHAR(64) NOT NULL, 
	source_id VARCHAR(64) NOT NULL, 
	difficulty VARCHAR(16) NOT NULL, 
	quiz_id VARCHAR(32) NOT NULL, 
	hints_used JSONB NOT NULL, 
	created_at FLOAT NOT NULL, 
	updated_at FLOAT NOT NULL, 
	version INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(quiz_id) REFERENCES quizzes (id)
);
ALTER TABLE quiz_sessions ENABLE ROW LEVEL SECURITY;

CREATE TABLE transcriptions (
	id SERIAL NOT NULL, 
	session_id VARCHAR(64), 
	created_at FLOAT NOT NULL, 
	result JSONB NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(session_id) REFERENCES tutor_sessions (id) ON DELETE CASCADE
);
CREATE INDEX ix_transcriptions_session_id ON transcriptions (session_id);
ALTER TABLE transcriptions ENABLE ROW LEVEL SECURITY;

CREATE TABLE tutor_turns (
	id SERIAL NOT NULL, 
	session_id VARCHAR(64) NOT NULL, 
	number INTEGER NOT NULL, 
	created_at FLOAT NOT NULL, 
	origin VARCHAR(16) NOT NULL, 
	student_text VARCHAR NOT NULL, 
	tutor_text VARCHAR NOT NULL, 
	action VARCHAR(32), 
	step VARCHAR(64), 
	level INTEGER, 
	fallback BOOLEAN NOT NULL, 
	latency_ms INTEGER, 
	trace JSONB NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(session_id) REFERENCES tutor_sessions (id) ON DELETE CASCADE
);
CREATE INDEX ix_tutor_turns_session_id_number ON tutor_turns (session_id, number);
ALTER TABLE tutor_turns ENABLE ROW LEVEL SECURITY;

CREATE TABLE mistake_gradings (
	id SERIAL NOT NULL, 
	session_id VARCHAR(64) NOT NULL, 
	created_at FLOAT NOT NULL, 
	annotations JSONB NOT NULL, 
	result JSONB NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (session_id), 
	FOREIGN KEY(session_id) REFERENCES mistake_sessions (id) ON DELETE CASCADE
);
ALTER TABLE mistake_gradings ENABLE ROW LEVEL SECURITY;

CREATE TABLE quiz_gradings (
	session_id VARCHAR(64) NOT NULL, 
	created_at FLOAT NOT NULL, 
	answers JSONB NOT NULL, 
	hints JSONB NOT NULL, 
	result JSONB NOT NULL, 
	PRIMARY KEY (session_id), 
	FOREIGN KEY(session_id) REFERENCES quiz_sessions (id) ON DELETE CASCADE
);
ALTER TABLE quiz_gradings ENABLE ROW LEVEL SECURITY;

