# Backend conventions

Rulebook for anyone, human or automated tool, changing the backend. The full text, with layout, layer rules, code
conventions and test conventions, is in [docs/architecture.md](../docs/architecture.md). The essentials:

- DDD with a clean architecture. Each bounded context under `core/<context>/` is `domain/` (entities, values,
  services, ports, repository interfaces) → `application/` (one use case per file) → `infra/` (LLM adapters, SQLModel
  repositories, file sources). Dependencies point inwards.
- The layer rules are tests: `uv run pytest backend/tests/test_import_restrictions.py`. Concrete classes are built
  only in composition roots (`apps/tutor_api`, `scripts/`, test fixtures). `settings.Config` is read only there.
- Identifiers are English. Student-facing text, prompts and authored YAML are Catalan. Values that are part of a
  contract (LLM schema keys and enum values, the JSON keys the frontend reads, stored documents) keep their Catalan
  spelling, modelled with `catalan_alias` (`core/shared/domain/contract.py`).
- A change visible to students (prompts, policy, JSON the frontend reads) needs a test that pins the new behaviour.
- Mock only what the project does not own: the LLM (`tests/fakes/llm.py`), the network, the clock. Repositories are
  tested against the real SQLite fixture.
- Before finishing: `uv run poe check` (ruff, pyright, pytest).
