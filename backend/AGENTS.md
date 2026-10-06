# Backend conventions

DDD + Clean Architecture. The migration plan and target layout are in `work/ARQUITECTURA.md`; this file is the
standing rulebook. Reference implementations to copy: `core/course/` (a full context) and `core/shared/`.

## Layout

- `core/<context>/` is a bounded context, a triad `domain/ → application/ → infra/` (`infra/` only when the
  context persists something or talks to the outside). Contexts: `course`, `tutoring`, `mistakes`, `quizzes`.
- `core/shared/`: shared kernel (`domain/` ids + exceptions + clock, `llm/` port + clients, `llm_calls/` call log,
  `storage/` async SQLModel session provider, `math/` CAS + sympy checks).
- `apps/tutor_api/`: the FastAPI app (composition root): `server.py`, `endpoints/`, `schemas/`, `dependencies.py`.
- `settings/`: `Config` (environment). Read only in composition roots.
- `tests/` mirrors `core/` and `apps/`. `tests/fakes/llm.py` (`ScriptedLLMClient`) is the LLM boundary fake;
  `tests/fixtures/course.py` gives the authored course; `conftest.py` gives a real SQLite database per test.

## Layer rules

1. `domain/` imports only stdlib, pydantic, `core.shared.domain`, `core.shared.math`, and other contexts' `domain/`.
   Never `application/`, `infra/`, `apps`, `settings`, SDKs or SQLModel sessions.
2. `application/` imports its `domain/`, other contexts' `domain/`/`application/`, `core.shared.domain`,
   `core.shared.llm.call_scope`. Never any `infra/`, never a concrete repository, never `settings`.
3. Repository interfaces are `ABC`s in `domain/repository.py`. Narrow ports onto the outside (LLM stages,
   other contexts, content sources) are `Protocol`s in `domain/ports.py`, implemented in `infra/`.
4. Concretes are built only in composition roots: `apps/tutor_api` `_get_*` `Depends` providers, `scripts/`,
   test fixtures. No container library.

## Code

- English identifiers. Student-facing text, prompts and authored YAML stay Catalan. Values that are part of a
  contract (LLM JSON schema keys and enum values, the HTTP JSON keys the frontend reads, stored documents) keep their
  current spelling: model them with English attributes and `validation_alias=AliasChoices(<catalan>, <english>)`
  + `serialization_alias=<catalan>` (see `core/shared/math/sympy_checks.py`).
- One file per use case in `application/`, class `<Noun><Verb>er` (`TurnHandler`, `QuizGenerator`), plain class,
  ports injected in `__init__`, intention-revealing `async` methods. Input DTOs colocated as `<UseCase>Input`.
- Failures raise `<Context>Exception(message, error_code)` subclasses (`domain/exceptions.py`, base
  `core.shared.domain.exceptions.DomainException`); `error_code` is the HTTP status. No `None`/`(ok, err)` returns
  for failures.
- No `dict[str, Any]` carrying domain data across layers: typed pydantic models. IDs are value objects
  (`core.shared.domain.ids`).
- Async for all I/O (LLM calls, repositories). CPU-heavy pure code (sympy) stays sync; call it with
  `asyncio.to_thread` from application code when it can take long.
- Repositories: SQLModel records in the context's `infra/`, subclass the domain ABC + `BaseSQLModelRepository`,
  methods decorated `@with_session`. Tables in English, snake_case, plural. JSON documents via `JsonColumn`.
- All imports at the top. Comments only when a reader would otherwise get the code wrong; never narrate changes.
- loguru for logging. Python 3.13, `X | None`, PEP 695 generics where useful.

## Tests

- Mock only what we do not own (the LLM via `ScriptedLLMClient`, the network, the clock). Repositories are tested
  against the real SQLite fixture (`session_provider`). No new in-memory repository fakes.
- Keep behaviour identical to the legacy `backend/tutor/` during the migration: every legacy test has a ported
  equivalent, plus `test_legacy_parity.py` per context comparing old and new outputs (deleted in phase 6).
- `make check` = ruff + pyright + pytest; all clean before a phase is done.
