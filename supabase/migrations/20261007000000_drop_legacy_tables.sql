-- The pre-DDD schema (Catalan table names) is replaced by 20261007000001_schema.sql.
-- It held only content that is re-imported from the repository (sheets, theory, pre-generated documents).
DROP TABLE IF EXISTS correccions, transcripcions, torns, exercicis, sessions, llistes, items_teoria, temes,
    contingut_generat, crides_llm CASCADE;
