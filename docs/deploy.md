# Deploy and operations

One Docker web service (FastAPI and the static frontend) and one Postgres database. Production runs the service on
Render from `render.yaml` and the database on Supabase. Everything the app produces (sessions, tutor turns, gradings,
generated documents and quizzes, photo transcriptions, the log of every model call) lives in the database. The
course content (sheets, notes, challenges) and the PDFs ship in the image.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) for local development (it installs Python 3.13).
- Docker with Compose 2.24 or later for the production-like stack (it reads `.env` only if the file exists).
- An API key for the model provider.

## Local development

```
uv sync
cp .env.example .env      # set OPENAI_API_KEY
uv run poe run            # http://127.0.0.1:8000
```

- The database is SQLite at `data/tutor.db`, created on first start. Delete the file to start over.
- `.env.example` sets `TUTOR_DEMO=1`: solutions, traces, the model setup and `/docs` are visible to everyone. Local use
  only.
- Tasks: `uv run poe check` (all of the below but `format` and `schema`), `lint`, `format`, `types`, `test`, `schema`.
- CI (`.github/workflows/ci.yml`) needs no secrets. It runs lint and types, `scripts/check_fitxes.py` and
  `scripts/db.py schema --check`, the test suite on SQLite, every migration applied in order to an empty Postgres 17
  and compared with the code (`scripts/db.py check-migrations`), the storage tests again on Postgres 17, and a smoke
  test that builds the image, starts it on Postgres with 512 MB and waits for `/health`.

## Production-like stack

```
docker compose up --build   # http://localhost:8000
```

- The app runs from the production image on Postgres 17, built from `supabase/migrations/`, with demo mode off.
- The professor key is `prof-local` unless `TUTOR_CLAU_PROFESSOR` is set: open `http://localhost:8000/?prof=prof-local`
  once and the browser keeps the key.
- API keys come from `.env` when it exists. `DATABASE_URL` and `TUTOR_DEMO` from `docker-compose.yml` win over
  `.env`.
- The migrations run only on an empty volume. After pulling a new migration, run `docker compose down -v`; local
  data is lost.

## Render

`render.yaml` is a Blueprint for one Docker web service.

1. Render → New → Blueprint, and pick the repository. Render reads `render.yaml` and builds the `Dockerfile`.
2. It asks once for the secrets (`sync: false`):
   - `OPENAI_API_KEY`;
   - `DATABASE_URL` (see Supabase below);
   - `TUTOR_CLAU_PROFESSOR`. Generate it with `uv run python -c "import secrets; print(secrets.token_urlsafe(32))"`.
     It is not `generateValue`, because Render's base64 values may contain `+`, which arrives as a space in
     `?prof=<key>`.
3. Fixed in `render.yaml`: `LLM_PROVIDER=openai`, the per-stage models and efforts, `TUTOR_GENERACIO=professor` and
   `TUTOR_DEMO=0`. Production uses a small model for the tutor stages, the photo transcription and the two gradings;
   generation and verification keep the larger provider defaults (`backend/core/shared/llm/infra/stage_configs.py`).
   Never set `TUTOR_DEMO=1` or a global `TUTOR_MODEL` in production: the first publishes solutions and the model
   setup, the second also overrides the generation and verification stages. A Blueprint sync adds and updates the
   variables it declares but does not delete others, so remove a stale one in the dashboard.

Behaviour of the service:

- **Region** Frankfurt, the same as the database. It is fixed at creation: changing it means a new service.
- **Deploys** happen only after the CI checks on `main` pass (`autoDeployTrigger: checksPass`). The `buildFilter`
  skips pushes that touch only documentation or tests.
- **Health check** `/health`. It answers once start-up (course, database, seeding) has finished.
- **One worker.** The rate limiter, the generation single-flights and the start-up import of pre-generated content
  live in process memory and assume one process. Scale with a bigger instance, or move them out before adding
  workers.
- **Start-up guard.** With `RENDER` set (Render sets it), the server refuses to start if the provider key,
  `DATABASE_URL` or `TUTOR_CLAU_PROFESSOR` is missing, or if `TUTOR_DEMO=1`. It logs one line with the effective
  configuration (provider, model per stage, database host, demo, professor key set or not, generation policy), never
  a secret.
- `LLM_PROVIDER` defaults to `openai`. `GET /api/config` returns the provider and models only to professors (and in
  demo mode); students get only their permissions.
- **Client addresses.** The rate limits key on the rightmost `X-Forwarded-For` hop, the one Render's proxy appends.
  The image trusts forwarded headers only from private ranges (`FORWARDED_ALLOW_IPS`). Never set it to `*`: a client
  could then choose its own address and bypass the limit. Behind a CDN, add its ranges.
- The image runs as an unprivileged user, and uvicorn is PID 1, so `SIGTERM` runs the shutdown hooks.

## Supabase

1. Create a project in an EU region (Frankfurt, as the web service).
2. Create the schema: `supabase db push` with the CLI linked to the project, or run the files of
   `supabase/migrations/` in order in the SQL editor. Every table has row level security enabled with no policies, and
   the public roles (`anon`, `authenticated`) have no grants: the public API keys can read nothing, only the server,
   connecting as the owner, can.
3. `DATABASE_URL` is the **transaction pooler** URI (port 6543), as Supabase shows it. A `postgresql://` URL is
   accepted as is. URL-encode special characters in the password (`@ : / #`). The engine disables prepared
   statements, which the transaction pooler does not support.
4. Nothing needs loading by hand. The course is read from the YAML in the image on every start, and the pre-generated
   documents and quizzes are imported on start when the database lacks them. `uv run python scripts/db.py
   import-generats` and `stats` do the same from a workstation.

### Schema changes

Migrations are append-only. Change the SQLModel records, run `uv run poe schema`, and add a new
`supabase/migrations/<timestamp>_<what>.sql` (see [architecture.md](architecture.md#persistence-and-schema-changes)).
**Apply each migration to Supabase before merging**: the free Render plan has no pre-deploy command, so the new code
would otherwise start against the old schema.

## Configuration reference

`.env.example` lists every variable with its default.

| Variable | Default | What |
|---|---|---|
| `LLM_PROVIDER` | `openai` | `openai`, `anthropic`, `gemini` or `openrouter` |
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` / `GEMINI_API_KEY` / `OPENROUTER_API_KEY` | — | Only the chosen provider's key is needed |
| `TUTOR_MODEL_<STAGE>`, `TUTOR_EFFORT_<STAGE>` | per provider | Model and effort of one stage |
| `TUTOR_MODEL` | — | One model for every stage, generation included; leave unset in production |
| `DATABASE_URL` | SQLite `data/tutor.db` | Required in production |
| `TUTOR_CLAU_PROFESSOR` | — | Professor key; required in production. Unset and no demo: nobody sees solutions |
| `TUTOR_DEMO` | `0` | `1` shows solutions, traces, model setup and `/docs` to everyone; local only |
| `TUTOR_GENERACIO` | `professor` | Who may start a live generation: `professor` or `tothom` |
| `TUTOR_MODEL_REQUESTS_PER_MINUTE` | 20 | Per client, on the endpoints that call a model |
| `TUTOR_MODEL_REQUESTS_PER_MINUTE_GLOBAL` | 150 | All clients together, on the same endpoints |
| `TUTOR_QUIZ_GENERATION_DEADLINE_S` | 420 | Deadline of one quiz generation |
| `TUTOR_MISTAKES_GENERATION_DEADLINE_S` | 300 | Deadline of one "Troba l'error" generation |
| `TUTOR_LOG_PROMPTS` | `0` | `1` also stores full prompts in `llm_calls` (large) |
| `TUTOR_SYMPY_WORKERS` | 1 | sympy worker processes; one fits a 512 MB instance |
| `TUTOR_SYMPY_WORKER_MEMORY_MB` | 256 | Address-space cap per worker, POSIX only; `0` = none |
| `TUTOR_SYMPY_WARM_CACHE` | `0` | `1` decides every authored counterexample at start-up (minutes of CPU on a small instance) |
| `FORWARDED_ALLOW_IPS` | private ranges (image) | Proxies whose `X-Forwarded-For` uvicorn trusts |

## Logs and data

- Every model call: table `llm_calls` (stage, model, tokens, cached tokens, latency, outcome, error, raw response).
- Every tutor turn: table `tutor_turns` (student message, reply, origin, full trace). Professors browse them at
  `#/professor`.
- Inspect with the Supabase table or SQL editor, or `uv run python scripts/db.py stats` for row counts.
- Backups: Supabase's backups (paid plans) or `pg_dump "$DATABASE_URL"`.

## Free-tier limits

- The Render free instance (512 MB, one instance) sleeps when idle; the first request after a pause waits for a cold
  start.
- A Supabase free project pauses after a period of inactivity and must be resumed from its dashboard.
- Live generation takes minutes per document or quiz. Keep the ready pool stocked with the pre-generation scripts, so
  that students are never the ones waiting.
