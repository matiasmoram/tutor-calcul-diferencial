-- A quiz grading in progress is claimed, so a double submit is refused before any model call.
ALTER TABLE quiz_sessions ADD COLUMN grading_started_at FLOAT;
