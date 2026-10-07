# Architecture migration — DDD / Clean Architecture (Prosper house style)

Status 2026-10-06. Resume point for the backend restructure: read it whole before continuing.

Goal: same behaviour (the 1572 tests are the oracle), new structure following the conventions of
`Prosper-Technologies/prosper-agents` (studied read-only; nothing of it is copied):

- Feature packages (bounded contexts) under `backend/core/<context>/`, each a DDD triad
  `domain/ → application/ → infra/`. `infra/` only when the feature persists or talks to the outside.
- The HTTP API lives outside `core/`: `backend/apps/tutor_api/` (`server.py`, `endpoints/`, `schemas/`).
- English code. Student-facing text, prompts and the authored YAML content stay Catalan (they are data).
- Async everywhere for I/O: async LLM clients, async SQLModel repositories (asyncpg on Postgres, aiosqlite in tests).
- Tooling: uv + `pyproject.toml`, ruff, pyright (standard), pytest with `asyncio_mode = "auto"`, Makefile, loguru.

Decisions taken with Matías: English names; async SQLModel stack.

## Layer rules (enforced by `backend/tests/test_import_restrictions.py`)

| Layer | May import | Must not import |
|---|---|---|
| `core/<ctx>/domain` | stdlib, pydantic, `core.shared.domain`, other pure domain code | `application`, `infra`, `apps`, sqlmodel sessions, SDKs (openai, google, anthropic), `settings` |
| `core/<ctx>/application` | its own `domain`, other contexts' `application`/`domain` (ports), `core.shared.domain` | any `infra`, `apps`, concrete repositories, `settings` |
| `core/<ctx>/infra` | everything in `core` | `apps` |
| `core/shared` | itself | any feature context, `apps` |
| `apps/tutor_api` | everything | — (it is the composition root) |

Further rules:
1. Repository interfaces are `ABC`s in `domain/repository.py`; narrow ports onto other contexts or the outside
   world (LLM stages) are `Protocol`s in `domain/ports.py`.
2. One file per use case in `application/`, named `<Noun><Verb>er` (`TurnHandler`, `SessionStarter`), plain classes
   with constructor-injected ports, intention-revealing async methods. Input DTOs colocated as `<UseCase>Input`.
3. Failures are per-context exceptions `<Ctx>Exception(message, error_code)`; never `None`/`(ok, err)` returns.
4. Endpoints do four things: request → value objects, await one use case, translate domain exceptions
   (`domain_errors()` context manager), map the result to a response schema. Services are built in `_get_*`
   `Depends` providers, never in the handler body. No container library.
5. No `dict[str, Any]` carrying domain data between layers. IDs are value objects from the endpoint inward.
6. All imports at the top. Comments only where a reader would get the code wrong without them.
7. Tests: mock only what we don't own (LLM, network, clock). Repositories are tested against a real database
   (aiosqlite in-process; Postgres in CI). The scripted LLM (`ScriptedLLM`) is the LLM boundary fake.

## Target layout

```
backend/
  settings/settings.py            Config (env vars: DATABASE_URL, LLM_PROVIDER, TUTOR_MODEL, PROFESSOR_KEY, ...)
  core/
    shared/
      domain/                     DomainException base, Clock, value-object helpers
      llm/                        LLMClient ABC, CallMeta, Image, LLMError, repair_latex      (domain-level port)
        infra/                    openai_client, gemini_client, anthropic_client, openrouter_client,
                                  stage_router, logged_client (records LLMCall), factory (composition roots only)
      llm_calls/                  LLMCall entity + repository ABC + sqlmodel repo (the "log" of every model call)
      storage/                    async SQLModelSessionProvider, with_session, BaseSQLModelRepository, engine
      math/                       latex_cas (was tutor/cas.py), sympy_checks (was tutor/comprovacions.py): pure
    course/                       course content: topics, theory items, problem sheets, exercises
      domain/entities/            topic.py, theory_item.py, problem_sheet.py (ProblemSheet, Problem),
                                  exercise.py (Exercise, Step, CommonMistake, ExpectedResult)
      domain/values/              theory_ref.py (TheoryRef.parse), exercise_kind.py, ...
      domain/citations.py         cited_items (pure)
      domain/repository.py        CourseRepository (ABC)
      application/                course_catalog.py (CourseCatalog), course_importer.py (CourseImporter)
      infra/                      yaml_course_source.py (authored YAML → entities), sqlmodel_repository.py, records.py
    tutoring/                     the Socratic tutor
      domain/entities/            tutor_session.py (TutorSession aggregate: history, state, closed, version)
      domain/values/              diagnosis.py, plan.py (Plan, Action), session_state.py, guard_verdict.py
      domain/policy.py            TutorPolicy: decide / allowed_content / allowed_theory (was politica.py)
      domain/guard.py             deterministic checks (was guardia.py)
      domain/fallback.py          authored fallback messages
      domain/ports.py             Diagnoser, ReplyWriter, ReplyJudge, Transcriber (Protocols)
      domain/repository.py        TutorSessionRepository (ABC)
      application/                session_starter.py, turn_handler.py (was pipeline.Tutor), photo_transcriber.py,
                                  session_browser.py (professor panel)
      infra/                      prompts.py, llm_schemas.py, llm_diagnoser.py, llm_reply_writer.py,
                                  llm_reply_judge.py, llm_transcriber.py, sqlmodel_repository.py, records.py
    mistakes/                     "Troba l'error" (was errades.py): MistakeExercise, sources, grading rules;
                                  generator / grader use cases; LLM + sqlmodel infra
    quizzes/                      "Cert o fals" (was afirmacions.py): Quiz, Statement, grading;
                                  generator / grader use cases; LLM + sqlmodel infra
  apps/tutor_api/
    server.py                     FastAPI app, lifespan (content sync), static frontend, /pdf
    dependencies.py               session provider, LLM client, professor auth
    endpoints/                    config, course, theory, tutor_sessions, professor, mistakes, quizzes
    schemas/                      request/response models with from_entity()
  tests/                          mirrors core/ and apps/; test_import_restrictions.py
scripts/                          CLI tools, composition roots (simulate, model_study, fuzz, db, ...)
```

## Contracts kept stable during the migration

- **HTTP API**: same paths and same JSON keys as today, so `frontend/` keeps working untouched. Response schemas
  have English attributes and serialize to the current keys (`Field(serialization_alias=...)`). Renaming the wire
  format (and the frontend) is a separate, later phase.
- **Authored YAML** (`backend/exercicis`, `backend/teoria`, `backend/generats`): unchanged; the YAML loader maps
  Catalan keys to English entities. `scripts/check_fitxes.py` and `merge_fitxes.py` keep working on the files.
- **Database**: new English table names → new Supabase migration. Production holds only re-importable content
  (no student sessions yet), so the old tables are dropped by that migration (confirm with Matías before applying).

## Concurrency change

Today a `threading.Lock` per in-memory session serializes turns and `SESSIONS` is a hot cache. New design: the
database is the only state; `TutorSession` carries a `version`; the repository saves with optimistic concurrency
(`UPDATE … WHERE version = :v`), and a conflict raises `ConcurrentTurnException` (409). Works with several workers.

## Phases (tests green at the end of each; old code deleted only in phase 6)

| # | What | Who | Depends |
|---|---|---|---|
| 0 | Tooling: pyproject (uv), ruff, pyright, pytest-asyncio, Makefile, Dockerfile on uv | Claude | — |
| 1 | `core/shared`: settings, exceptions, clock, storage, async LLM clients + call log, math | Claude | 0 |
| 2 | `core/course` + tests (content parity: every YAML exercise loads to the same data) | agent | 1 |
| 3 | `core/tutoring` + port test_politica / test_harness / fuzz; parity test old `decide` vs new `TutorPolicy` | agent | 2 |
| 4 | `core/mistakes` + tests | agent | 2 |
| 5 | `core/quizzes` + tests | agent | 2 |
| 6 | `apps/tutor_api`, DI, server; API parity tests; switch Docker/CI; delete `backend/app.py`, `backend/tutor/` | Claude | 3–5 |
| 7 | Scripts ported, new migration, import-restriction test, `AGENTS.md`, deploy | Claude | 6 |

Phases 3, 4, 5 run in parallel (disjoint directories). At most 4 agents at a time.

## Progress

- [x] 0 · [x] 1 · [x] 2 · [x] 3 · [x] 4 · [x] 5 · [x] 6 · [x] 7 (pending: apply the Supabase migration + merge to main, with Matías)
