# Backend conventions

DDD + Clean Architecture. This file is the standing rulebook; `tests/test_import_restrictions.py` enforces its layer
rules. Reference implementations to copy: `core/tutoring/` (a full context) and `core/shared/`.

## Layout

- `core/<context>/` is a bounded context, a triad `domain/ → application/ → infra/` (`infra/` only when the
  context persists something or talks to the outside). Contexts: `course`, `tutoring`, `mistakes`, `quizzes`, `counterexamples`.
- `course` is read-only authored content: `domain/` and `infra/` (the YAML loader), no use cases. The endpoints read
  the `Course` aggregate directly, and the other contexts' domains build on it.
- `core/shared/`: shared kernel. `domain/` (ids, exceptions, clock, contract aliases, model usage, claim timeouts),
  `llm/` (the port, its call scope and `infra/` clients), `llm_calls/` (call log), `storage/` (async SQLModel session
  provider), `math/` (the `latex_cas` package, LaTeX vocabulary, sympy checks, and the sympy worker pool in `infra/`).
- `apps/tutor_api/`: the FastAPI app (composition root): `server.py`, `endpoints/`, `schemas/`, `dependencies.py`.
- `settings/`: `Config` (environment). Read only in composition roots and in the infra factories they hand it to
  (`core/shared/llm/infra/factory.py`, `stage_configs.py`).
- `tests/` mirrors `core/` and `apps/`. `tests/fakes/llm.py` (`ScriptedLLMClient`) is the LLM boundary fake;
  `tests/fixtures/course.py` gives the authored course; `conftest.py` gives a real SQLite database per test.

## Layer rules

1. `domain/` imports only the standard library, `pydantic`, `sympy` (the maths is the domain), its own `domain/`,
   `core.course.domain`, `core.shared.domain` and `core.shared.math` (not `math.infra`). Never `application/`,
   `infra/`, the LLM port, `apps`, `settings`, SDKs or SQLModel sessions.
2. `application/` imports its `domain/`, other contexts' `domain/`, `core.shared.domain`, and from the LLM port only
   `core.shared.llm.call_scope` and the error types `LLMError`, `LLMProviderError`, `TruncatedOutputError`
   (`core.shared.llm.client`). Never any `infra/`, never a concrete repository, never `settings`.
3. Repository interfaces are `ABC`s in `domain/repository.py`. Narrow ports onto the outside (LLM stages,
   other contexts, content sources) are `Protocol`s in `domain/ports.py`, implemented in `infra/`.
4. A context's `infra/` is private: only its own `infra/` imports it. The shared kernel's `infra/` and `storage/` are
   imported only from `infra/` modules. Outside `infra/` and `storage/`, the shared kernel imports no SDK.
5. Concretes are built only in composition roots: `apps/tutor_api` `_get_*` `Depends` providers, `scripts/`,
   test fixtures. No container library.
6. Absolute imports only.

## Code

- English identifiers. Student-facing text, prompts and authored YAML stay Catalan. Values that are part of a
  contract (LLM JSON schema keys and enum values, the HTTP JSON keys the frontend reads, stored documents) keep their
  current spelling: model them with English attributes, `validation_alias=catalan_alias(<catalan>, <english>)` and
  `serialization_alias=<catalan>` (`core.shared.domain.contract`; see `core/shared/math/sympy_checks.py`).
- Exception: the request and response models in `apps/tutor_api/schemas/` are wire DTOs, named in the wire language
  (their attributes are the JSON keys); they only map to and from the domain.
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
- A change of behaviour visible to students (prompts, policy, JSON the frontend reads) needs a test that pins the
  new behaviour; prompts and LLM schemas are contracts, change them deliberately.
- `uv run poe check` (ruff, pyright, pytest) is clean before a change is done.
