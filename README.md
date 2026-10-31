# Socratic tutor for Càlcul Diferencial

A web application for the course Càlcul Diferencial (FME-UPC). It covers the whole problem collection (Temes 1–6,
333 exercises) and the course notes (188 numbered definitions, theorems and other items). A student picks an exercise and explains their work, and the
tutor guides them with questions and graded hints, citing the notes, without giving the solution away. Four further
practice modes reuse the same content. The interface is in Catalan; code and documentation are in English.

## Modes

| Mode | Route | What the student does | Model use | Status | Spec |
|---|---|---|---|---|---|
| Tutor socràtic | `#/exercicis` | Explains their work on one exercise, typed or as a photo of the notebook | Diagnosis, reply and guard on every turn | Available | [docs/tutor.md](docs/tutor.md) |
| Troba l'error | `#/errades` | Highlights and explains the errors planted in a worked solution or in a result of the notes | Documents generated and verified in advance; one grading call per submission | Available | [docs/troba-l-error.md](docs/troba-l-error.md) |
| Cert o fals | `#/afirmacions` | Decides whether 6–10 statements are true or false and justifies each one | Quizzes generated and verified in advance; grading plus sympy | Available | [docs/cert-o-fals.md](docs/cert-o-fals.md) |
| Construeix el contraexemple | `#/contraexemples` | Writes a function whose properties at the origin look incompatible, with certificates | None: sympy only | Beta | [docs/contraexemples.md](docs/contraexemples.md) |
| Visualitzador | `#/visual` | Plots and analyses functions of two variables, opened from an exercise statement | None: runs in the browser | Beta | [docs/visualitzador.md](docs/visualitzador.md) |

`#/teoria` lists the notes item by item, each linked to its page in the PDF. `#/professor` is the professors' review
of tutor sessions.

## Design principles

- **The LLM proposes, deterministic code decides.** A model returns a structured reading (JSON with closed enums built
  from the content) or a draft. The pedagogical action, the hint level, the acceptance of generated content and every
  score are computed in code, and are unit-tested.
- **The student never receives the solution.** The hidden solution sheet stays on the server. The stage that writes
  the tutor's reply only sees the content the policy releases for that turn. Every draft passes code checks (leak
  patterns, sympy equivalence against forbidden formulas, citations) and an LLM judge; failing that, the student gets
  an authored fallback. Checks fail closed: a judge error or a CAS timeout rejects the draft. In Troba l'error and
  Cert o fals the declared errors and verdicts are revealed only by the correction, and a challenge's authored
  counterexample only once the student's own one passes.
- **Every model call is logged.** The `llm_calls` table records stage, model, tokens (cached included), latency,
  outcome and raw response for every call, failures included, attributed to its session and turn. Each tutor turn
  stores its full trace (diagnosis, plan, released content, every draft with its verdicts) in `tutor_turns`.
- **Professor access is closed by default.** Solutions, traces and the model configuration are returned only to
  requests carrying the professor key (`X-Clau-Professor`). With no key configured nobody sees them, unless local
  demo mode (`TUTOR_DEMO=1`) is on, and the server refuses to start on Render without a key. Live generation of
  content, which costs money, is professor-only by default (`TUTOR_GENERACIO`).

## How a tutor turn works

```
student message
   │
   ▼
1. DIAGNOSIS   LLM, structured output        sees: full solution sheet + its theory + conversation
   JSON schema with closed enums built from the sheet: state of each step, current step, common
   mistakes detected, proposed result (correct / incorrect), disorientation, intent, literal evidence.
   │
   ▼
2. POLICY      plain Python, deterministic state machine
   Decides the action (pista, questionar_error, validar_i_avancar, mostrar_pas, …), the target step
   and the hint level 1–4, and derives what the reply may use and what it must not reveal.
   │
   ▼
3. REPLY       LLM, plain text                sees: ONLY the content the plan releases
   Level 1 = step objective, 2 = + strategy idea and the step's theory, 3 = + worked detail,
   4 = the full step (only after an attempt, at the top of the ladder). Later steps and the
   result are not in its prompt.
   │
   ▼
4. GUARD       a) code: leak regexes, sympy equivalence with forbidden formulas, unknown LaTeX,
                  closing question, length, citations outside the allowed items
               b) LLM judge with the full solution (only when a passes)
   Rejected: rewrite with the reasons (3 drafts at most), then an authored fallback.
   │
   ▼
turn stored atomically (session state + trace) → reply + cited theory items to the student
```

Details, including the solution sheet format and the professor view: [docs/tutor.md](docs/tutor.md).

## Architecture

Python 3.13, FastAPI, SQLModel (async), sympy. Domain-driven design with a clean architecture: each bounded context
under `backend/core/` is split into `domain/` (pure rules), `application/` (one use case per file) and `infra/` (LLM
adapters, SQLModel repositories, file sources).

| Context | Responsibility | Use cases |
|---|---|---|
| `course` | Authored content: topics, theory items, problem sheets, exercises with their hidden solution sheets | none (read-only aggregate loaded from YAML) |
| `tutoring` | The Socratic tutor | `SessionStarter`, `TurnHandler`, `PhotoTranscriber`, `SessionBrowser` |
| `mistakes` | Troba l'error | `MistakeSessionStarter`, `MistakeExerciseProvider`, `MistakeExerciseGenerator`, `AnnotationsGrader`, `AvailabilityLister`, `PregeneratedImporter` |
| `quizzes` | Cert o fals | `QuizSessionStarter`, `QuizProvider`, `QuizGenerator`, `HintRevealer`, `AnswersGrader`, `SourceLister`, `PregeneratedImporter` |
| `counterexamples` | Construeix el contraexemple | `SubmissionGrader` |
| `shared` | Kernel: ids, exceptions, clock, contract aliases; the LLM port, provider clients and call log; async storage; the LaTeX-to-sympy CAS, sympy checks and worker pool | — |

Dependencies point inwards: `domain` imports no framework, SDK or database code; `application` sees only domain types
and ports; only `infra` touches the outside. Concrete classes are built only in composition roots: the FastAPI app
(`backend/apps/tutor_api`), the scripts and the test fixtures. `backend/tests/test_import_restrictions.py` enforces
these rules on every module. Conventions, layer rules and how to add a context or a use case:
[docs/architecture.md](docs/architecture.md).

Persistence: SQLite at `data/tutor.db` locally, Postgres (Supabase) in production. The course content is read from
the YAML shipped with the code on every start. Pre-generated documents and quizzes (`backend/generats/`) are imported
into the database on start. Everything the app produces (sessions, turns, gradings, transcriptions, the call log)
lives in the database.

## Integration surface

The backend is a JSON-over-HTTP API; the bundled frontend is one client of it. The frontend is static files (vanilla
JavaScript, KaTeX) with no build step, and the server holds all session state, so another client that speaks the same
JSON can replace it. JSON keys are Catalan, as the frontend reads them.

| Area | Endpoints |
|---|---|
| Course and config | `GET /api/llistes`, `GET /api/llistes/{sheet_id}`, `GET /api/teoria`, `GET /api/teoria/{item_id}`, `GET /api/config` |
| Tutor | `POST /api/sessions` `{exercici_id}`; `POST /api/sessions/{id}/missatges` `{text, origen}` → `{missatge, referencies, trace}`; `POST /api/sessions/{id}/transcripcio` `{imatge}` |
| Tutor, professors | `GET /api/professor/sessions`, `GET /api/professor/sessions/{id}` |
| Troba l'error | `GET /api/errades/teoria`, `GET /api/errades/disponibles`, `POST /api/errades/sessions`, `POST /api/errades/sessions/{id}/correccio` |
| Cert o fals | `GET /api/afirmacions/fonts`, `POST /api/afirmacions/sessions`, `POST /api/afirmacions/sessions/{id}/pista/{statement_id}`, `POST /api/afirmacions/sessions/{id}/correccio` |
| Contraexemples | `GET /api/contraexemples`, `GET /api/contraexemples/{id}`, `POST /api/contraexemples/{id}/comprova` |
| Operations | `GET /health`; `/pdf/...` serves the course PDFs |

- Students need no credentials. The professor key travels in the `X-Clau-Professor` header; the same endpoints then
  also return solutions and full traces.
- Errors are `{"detail": ...}` with the status the domain exception carries, for example 404 unknown id, 409
  concurrent request or nothing ready, 422 invalid input, 429 rate limit, 502 model failure, 503 missing provider key
  and 504 deadline.
- Endpoints that call a model are rate-limited per client and globally (`TUTOR_MODEL_REQUESTS_PER_MINUTE`,
  `TUTOR_MODEL_REQUESTS_PER_MINUTE_GLOBAL`).
- The OpenAPI schema (`/docs`, `/openapi.json`) is served only in demo mode.

Below HTTP, the application use cases are the seam for other front ends or protocols. Each takes its ports in the
constructor and exposes typed `async` methods, for example
`TurnHandler.handle(TurnHandlerInput(session_id, text, origin))`, which returns the reply, the cited theory items and
the turn trace. The endpoints are thin adapters over them, and `scripts/eval/harness.py` drives the same tutor use
cases with no HTTP at all.

## Quick start

Prerequisites: [uv](https://docs.astral.sh/uv/) (it installs Python 3.13) and an API key for a model provider.

```
uv sync
cp .env.example .env      # then set OPENAI_API_KEY (or another provider's key, see below)
uv run poe run            # http://127.0.0.1:8000
```

Locally the database is SQLite at `data/tutor.db`, created on first start. `.env.example` sets `TUTOR_DEMO=1`, so
solutions, traces and `/docs` are visible without a key. For a production-like stack on Postgres with demo mode off,
run `docker compose up --build` (see [docs/deploy.md](docs/deploy.md)).

## Checks

```
uv run poe check          # ruff (lint + format check), pyright, pytest
```

The suite has 2856 tests. It makes no network calls: the LLM is a scripted fake (`backend/tests/fakes/llm.py`), and
each storage test gets its own real SQLite database. Other tasks: `uv run poe lint`, `format`, `types`, `test`,
`schema` (regenerate `supabase/schema.sql`). CI (`.github/workflows/ci.yml`) also validates the solution sheets
(`scripts/check_fitxes.py`), checks the schema snapshot (`scripts/db.py schema --check`), applies every migration to
Postgres 17 and compares the result with the code, reruns the storage tests on Postgres, and smoke-tests the Docker
image.

Content and live-model tools (the last three need an API key):

- `scripts/check_fitxes.py`: structure, theory references and leak patterns of the solution sheets.
- `scripts/check_cas.py`: self-test of the sympy leak checker over every sheet.
- `scripts/eval/smoke_turn.py`: one real tutor turn against the configured provider, with its trace.
- `scripts/eval/simulate.py`: simulated students (personas) against the real tutor, with a separate leak judge.
- `scripts/eval/model_study.py`: the same scripted conversations under several model configurations.

## Configuration

All settings are environment variables; [.env.example](.env.example) lists and explains every one.

- `LLM_PROVIDER`: `openai` (default), `anthropic`, `gemini` or `openrouter`, with that provider's API key.
- `TUTOR_MODEL_<STAGE>` / `TUTOR_EFFORT_<STAGE>`: model and reasoning effort per stage. There are 12 stages, from
  `diagnosis`, `reply`, `guard` and `transcription` to the generation, verification and grading stages of each mode;
  defaults per provider are in `backend/core/shared/llm/infra/stage_configs.py`. Production uses a small model for the
  tutor stages and the gradings and a larger one for generation and verification.
- `DATABASE_URL` (unset: SQLite), `TUTOR_CLAU_PROFESSOR`, `TUTOR_DEMO`, `TUTOR_GENERACIO`, rate limits, generation
  deadlines and the sympy worker pool.

## Deploy

One Docker web service on Render plus a Supabase Postgres database, both described in the repository (`Dockerfile`,
`render.yaml`, `supabase/migrations/`). Steps, secrets and schema changes: [docs/deploy.md](docs/deploy.md).

## Repository layout

```
backend/
  apps/tutor_api/       FastAPI app (composition root): server, endpoints, wire schemas, dependencies
  core/<context>/       bounded contexts: domain/, application/, infra/
  core/shared/          shared kernel
  settings/             configuration from the environment
  exercicis/            solution sheets, one YAML file per tema
  teoria/               the course notes as numbered items, one YAML file per tema
  contraexemples/       counterexample challenges (reptes.yaml)
  generats/             pre-generated "Troba l'error" documents and "Cert o fals" quizzes
  tests/                mirrors core/, apps/ and scripts/
frontend/               static UI: index.html, app.js and the scripts of each mode
scripts/                content checks, pre-generation, offline authoring, database utilities, eval/
sources/                course notes and problem collection (PDF), served under /pdf
supabase/               migrations and the schema snapshot
docs/                   one spec per mode, architecture, deploy
```

## Course material

The course notes and the problem collection (the PDFs in `sources/`, transcribed into `backend/teoria/` and into the
statements of `backend/exercicis/`) belong to their authors at FME-UPC. They are included so that the application can
cite them and link each citation to its page.
