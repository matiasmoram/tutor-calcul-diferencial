-- The pre-DDD schema (Catalan table names) is replaced by 20261007000001_schema.sql.
-- Checked empty before dropping (2026-10-07): the sessions/turns/LLM-call tables had no rows; the rest is content
-- that now comes from the repository (sheets, theory) or is re-imported (pre-generated documents).
DROP TABLE IF EXISTS correccions, transcripcions, torns, exercicis, sessions, llistes, items_teoria, temes,
    contingut_generat, crides_llm CASCADE;
