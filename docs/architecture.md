# Architecture and conventions

The backend follows domain-driven design with a clean architecture. This page is the standing rulebook.
`backend/tests/test_import_restrictions.py` enforces its layer rules on every module, and the rest is checked in
review. All paths below are relative to `backend/`, which is the import root (`core`, `apps` and `settings` are
importable from the server, the scripts and the tests). The reference implementations to copy are `core/tutoring/`
(a full context) and `core/shared/`.

## Layout

- `core/<context>/` is a bounded context: `course`, `tutoring`, `mistakes`, `quizzes`, `counterexamples`. Each is a
  triad `domain/ → application/ → infra/`; `infra/` exists only when the context persists something or talks to the
  outside.
- Inside `domain/`:
  - `entities/`: objects with identity and lifecycle (`TutorSession`, `Quiz`, `MistakeExercise`).
  - `values/`: immutable value objects and the literal types of the contracts (`Plan`, `Diagnosis`, `Difficulty`).
  - `services/`: the rule modules, pure functions that decide (`policy.py`, `guard.py`, `grading.py`,
    `scoring.py`, `generation_checks.py`).
  - `exceptions.py`, `ports.py` and `repository.py`.
- `course` is read-only authored content: `domain/` and `infra/` (the YAML loader), no use cases. The endpoints read
  the `Course` aggregate directly, and the other contexts' domains build on it.
- `core/shared/` is the shared kernel:
  - `domain/`: ids, exceptions, clock, contract aliases, model usage, claim timeouts, single-flight.
  - `llm/`: the port (`client.py`), its call scope (`call_scope.py`), and in `infra/` the provider clients, the
    per-stage configuration, the call-logging and retrying wrappers and the factory.
  - `llm_calls/`: the call log.
  - `storage/`: the async SQLModel session provider and table registry.
  - `math/`: the `latex_cas` package, the LaTeX vocabulary and the sympy checks, plus the sympy worker pool in
    `infra/`.
- `apps/tutor_api/` is the FastAPI app and composition root. `server.py`'s lifespan builds the process-wide objects
  (course, challenge catalogue, LLM client stack, sympy pool, rate limiters, generation single-flights).
  `endpoints/` has one module per context, `schemas/` the wire DTOs, and `dependencies.py` the shared providers,
  professor check, rate limits and domain-error translation.
- `settings/` holds `Config`, read from the environment. It is read only in composition roots and in the infra
  factories they hand it to (`core/shared/llm/infra/factory.py`, `stage_configs.py`).

## Layer rules

Each rule below is a test in `tests/test_import_restrictions.py` (imports under `TYPE_CHECKING` are exempt):

1. **No relative imports** anywhere in `core`, `apps` or `settings`.
2. **`domain/`** imports only the standard library, `pydantic`, `sympy` (in this course the mathematics is the
   domain), its own `domain`, `core.course.domain`, `core.shared.domain` and `core.shared.math` (not
   `core.shared.math.infra`). It never imports `application/`, `infra/`, the LLM port, `apps`, `settings`, an SDK or
   a database session.
3. **`application/`** never imports an SDK or framework (`anthropic`, `openai`, `google`, `httpx`, `sqlmodel`,
   `sqlalchemy`, `fastapi`, `yaml`), `settings`, `apps`, any `infra` module or `core.shared.storage`.
4. From the LLM port, **`application/`** may import only `core.shared.llm.call_scope` and the error types `LLMError`,
   `LLMProviderError` and `TruncatedOutputError` (`core.shared.llm.client`).
5. **The shared kernel outside `infra/` and `storage/`** imports no SDK.
6. **`infra/` is private.** A context's `infra` is imported only by its own `infra`. The shared kernel's `infra` and
   `storage` are imported only from `infra` modules.
7. **The shared kernel knows no feature context.**
8. **`core` never imports `apps`.**

Two further rules are conventions:

- Repository interfaces are `ABC`s in `domain/repository.py`. Narrow ports onto the outside (LLM stages, content
  sources, the property checker) are `Protocol`s in `domain/ports.py`. Their adapters live in `infra/` and subclass
  the port explicitly (`class LLMReplyWriter(ReplyWriter)`).
- Concrete classes are built only in composition roots: the `_get_*` `Depends` providers of `apps/tutor_api`, the
  scripts, and the test fixtures. There is no container library.

## Code conventions

- **Language.** Identifiers are English. Student-facing text, prompts and the authored YAML stay Catalan.
- **Contracts keep their spelling.** Values that are part of a contract (LLM JSON schema keys and enum values, stored
  documents) are modelled with English attributes and their Catalan key:
  `validation_alias=catalan_alias("<catalan>", "<english>")` and `serialization_alias="<catalan>"`
  (`core.shared.domain.contract`; example: `core/shared/math/sympy_checks.py`).
- **Wire DTOs.** The request and response models in `apps/tutor_api/schemas/` keep the Catalan wire names as their
  attributes (`exercici_id`, `missatge`, `referencies`): they are the JSON the frontend reads, and they only map to
  and from domain types (`from_entity`, `to_domain`).
- **Use cases.** One file per use case in `application/`, one plain class named `<Noun><Verb>er` (`TurnHandler`,
  `QuizGenerator`, `AnswersGrader`). Ports and repositories are injected in `__init__`, and the methods are
  intention-revealing and `async`. An input DTO, when needed, is colocated as `<UseCase>Input` (`TurnHandlerInput`).
- **Failures** raise a `<Context>Exception(message, error_code)` subclass (`domain/exceptions.py`, base
  `core.shared.domain.exceptions.DomainException`), where `error_code` is the HTTP status. The API translates them in
  one place (`domain_errors`). No `None` or `(ok, err)` returns for failures.
- **Types.** No `dict[str, Any]` carries domain data across layers: typed pydantic models. Ids are value objects
  (`core.shared.domain.ids`).
- **Async** for all I/O (model calls, repositories). CPU-heavy pure code (sympy) stays synchronous. Application code
  calls it with `asyncio.to_thread` when it can take long, and untrusted expressions go to the `SympyCheckPool`
  worker processes under a deadline.
- **Time** comes from an injected `Clock`, so use cases are deterministic under test.
- **Long operations** run under `asyncio.timeout` deadlines. A turn or a grading first claims its session, with a claim
  timeout strictly above the deadline (`core.shared.domain.claims`). Concurrent generations of the same content share
  one run (`SingleFlight`).
- **Repositories** are SQLModel records in the context's `infra/`. Each repository subclasses the domain `ABC` and
  `BaseSQLModelRepository`, with methods decorated `@with_session`. Table names are English, snake_case and plural.
  JSON documents use `JsonColumn`.
- All imports at the top. Comments only where a reader would otherwise get the code wrong; they never narrate
  changes. `loguru` for logging. Python 3.13: `X | None`, PEP 695 generics where useful.

## The LLM layer

- The port is `LLMClient.structured(stage, request)` (`core/shared/llm/client.py`). A request has a system prompt, a
  user prompt, an optional JSON schema (none means plain text, returned as `{"text": ...}`), an optional image, and an
  optional static `context` sent first so providers can cache it.
- `Stage` enumerates the 12 stages. `stage_configs()` resolves each stage's model, effort and token cap from the
  provider defaults and the `TUTOR_MODEL_<STAGE>` / `TUTOR_EFFORT_<STAGE>` overrides.
- The server stacks `RetryingLLMClient(LoggedLLMClient(provider client))`. The logging layer writes every call,
  failures included, to `llm_calls`, attributed to the session and turn set by the use case's `call_scope`; a failure
  to write the log never breaks a request. The retrying layer asks once more when the output is malformed. Provider
  errors propagate.
- Adapters (`infra/llm_*.py`) build the prompts and schemas, validate the output into domain values, and raise the
  context's typed exception when the output is unusable.

## Persistence and schema changes

`register_all_tables()` imports every `infra` module so that `SQLModel.metadata` holds the whole schema. SQLite
databases are created on start; Postgres is migrated with SQL files. Migrations are append-only, so an applied file is
never edited:

1. Change the SQLModel records (`core/*/infra/sqlmodel_repository.py`).
2. `uv run poe schema` refreshes the snapshot `supabase/schema.sql`.
3. Add `supabase/migrations/<timestamp>_<what>.sql` with the `ALTER` / `CREATE` statements, enabling row level
   security on any new table.
4. CI fails if the snapshot differs from the code (`scripts/db.py schema --check`) or if the migrations, applied in
   order to an empty Postgres, differ from the code (`scripts/db.py check-migrations`).

## Tests

- `tests/` mirrors `core/`, `apps/` and `scripts/`. Shared helpers live in a `builders.py` next to the tests that use
  them, never in test modules.
- `tests/fakes/llm.py` (`ScriptedLLMClient`) is the LLM boundary fake. `tests/fixtures/course.py` and
  `tests/fixtures/counterexamples.py` load the real authored content.
- `tests/conftest.py` gives each test a real, empty database: SQLite in a temporary directory, or the Postgres of
  `TEST_DATABASE_URL` (CI runs the storage tests on both).
- Mock only what we do not own: the LLM, the network, the clock. Repositories are tested against the real database
  fixture (`session_provider`). There are no in-memory repository fakes.
- A change of behaviour visible to students (prompts, policy, the JSON the frontend reads) needs a test that pins the
  new behaviour. Prompts and LLM schemas are contracts, changed deliberately.
- Every test has a 300 s timeout (`pytest-timeout`), so a sympy computation that hangs fails its test instead of
  holding CI.
- `uv run poe check` (ruff, pyright, pytest) is clean before a change is done.

## Adding a use case

1. Define what it needs from the outside as ports in `domain/ports.py` (or a repository `ABC` in
   `domain/repository.py`), and the rules as pure functions in `domain/services/`, with unit tests.
2. Write `application/<noun>_<verb>er.py` with one class taking those ports in `__init__`, plus a `<UseCase>Input`
   model if the input has more than a couple of fields. Test it with `ScriptedLLMClient` and the database fixture.
3. Implement the ports in `infra/` (an `LLM*` adapter with its prompt and schema, a SQLModel repository), subclassing
   the port.
4. Wire it in `apps/tutor_api/endpoints/<context>.py`: a `_get_<use case>` provider that builds the concretes, an
   endpoint that maps the wire DTO (`schemas/<context>.py`) to the input and the result back, wrapped in
   `domain_errors()`. Add `Depends(model_rate_limited)` if it calls a model and `ensure_api_key(config)` before the
   first model call. Add an endpoint test under `tests/apps/tutor_api/`.

## Adding a context

1. Create `core/<context>/` with `domain/` (`entities/`, `values/`, `services/`, `exceptions.py` with a
   `<Context>Exception(DomainException)` base, `ports.py`), `application/` and, if needed, `infra/`. Use
   `core.course.domain` for anything about the course content, and the shared kernel for ids, contracts, the LLM
   port and sympy.
2. If it calls a model, add its stages to `Stage` and their defaults to `stage_configs.py`.
3. If it persists data, add its records in `infra/sqlmodel_repository.py` (they are registered automatically) and a
   migration as above.
4. Add `apps/tutor_api/endpoints/<context>.py` and `schemas/<context>.py`, and include the router in `server.py`.
5. Mirror it under `tests/core/<context>/`. `test_import_restrictions.py` covers the new modules with no change.
