# Deploy

Architecture: one Docker web service (FastAPI + static frontend) + a Supabase Postgres database.
Everything persistent (course content, sessions, every tutor turn, the log of every model call, generated
"troba l'error" / quiz content, gradings, photo transcriptions) lives in the database. Tables are the SQLModel records in each context's `infra/` (`backend/core/*/infra/sqlmodel_repository.py`).

## Secrets

Never commit them. `.env` is git-ignored; `.env.example` lists every variable.

| Variable | Required | What |
|---|---|---|
| `OPENAI_API_KEY` | yes (with `LLM_PROVIDER=openai`) | Model provider key. Alternatives: `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENROUTER_API_KEY` |
| `LLM_PROVIDER` | yes | `openai` (recommended), `gemini`, `anthropic`, `openrouter` |
| `TUTOR_MODEL_<STAGE>` / `TUTOR_EFFORT_<STAGE>` | recommended | Per-stage model/effort. Production: `gpt-5.6-luna` for `diagnosis`, `reply`, `guard` (effort `none`), `transcription`, `mistakes_grading`, `quiz_grading`; generation/verification stages keep their defaults. Set in `render.yaml` |
| `TUTOR_MODEL` | no | One model for **every** stage, generation included. Leave unset in production (see Models below) |
| `DATABASE_URL` | yes in production | Supabase connection string (below). Without it: local SQLite at `data/tutor.db` |
| `TUTOR_CLAU_PROFESSOR` | yes in production | Professor key. Students never see solutions/traces; professors open the app once with `?prof=<key>`. Unset: nobody sees them (unless `TUTOR_DEMO=1`) |
| `TUTOR_DEMO` | no | `1` = demo mode without a key: everyone sees solutions and traces. Local development only |
| `TUTOR_MODEL_REQUESTS_PER_MINUTE` | no | Per-client limit on the endpoints that call a model (default 20) |
| `TUTOR_MODEL_REQUESTS_PER_MINUTE_GLOBAL` | no | Limit for all clients together on those endpoints, on top of the per-client one (default 150) |
| `TUTOR_GENERACIO` | no | Who may trigger live (paid) generation of "Troba l'error" documents / "Cert o fals" quizzes: `professor` (default) or `tothom`. Otherwise students get pre-generated content only (409 when none is ready) |
| `TUTOR_QUIZ_GENERATION_DEADLINE_S` | no | Deadline for generating one quiz, seconds (default 420) |
| `TUTOR_MISTAKES_GENERATION_DEADLINE_S` | no | Deadline for generating one "Troba l'error" document, seconds (default 300) |
| `TUTOR_LOG_PROMPTS` | no | `1` also stores full prompts in `llm_calls` (large) |
| `TUTOR_SYMPY_WORKER_MEMORY_MB` | no | Address-space cap per sympy worker process, POSIX only (default 256; `0` = none). A runaway check fails in its worker instead of OOM-killing the server |
| `TUTOR_SYMPY_WORKERS` | no | sympy worker processes (default 1: server ~170 MB + one capped worker fits 512 MB) |
| `TUTOR_SYMPY_WARM_CACHE` | no | `1` decides every authored counterexample at start-up so its verdict is cached (default `0`: on the free plan it costs minutes of CPU on every wake) |
| `FORWARDED_ALLOW_IPS` | no | Proxies whose `X-Forwarded-For` uvicorn trusts. The image sets the private ranges (Render's proxies); never `*`, which lets a client pick its own IP and dodge the rate limit |

Client address: the rate limits key on the rightmost `X-Forwarded-For` hop, the one Render's proxy appends
(everything to its left is client-written). That is only trustworthy behind such a proxy: a host that exposes the
container directly lets a client choose its key. uvicorn (`--proxy-headers`, `FORWARDED_ALLOW_IPS` = private ranges)
resolves `request.client` to the same hop.

Where they live:
- **Local**: `.env` (copy `.env.example`).
- **Hosting** (Render/Fly/Railway): the service's environment/secret settings. `render.yaml` declares them with
  `sync: false`, so Render asks for the values and never stores them in the repo.
- **GitHub**: CI needs no secrets (tests use scripted LLMs and SQLite). Add repository secrets only if you add a
  deploy workflow (`Settings → Secrets and variables → Actions`).

## Supabase

1. Create a project at https://supabase.com (region: EU, e.g. Frankfurt).
2. Create the schema: either `supabase db push` with the CLI (linked to the project), or run the files of
   `supabase/migrations/` in order in **SQL Editor → Run**. RLS is enabled on every table with no policies and the
   public roles have no grants: the `anon` key can read nothing; only the server, connecting as the owner, can.
3. **Project Settings → Database → Connection string → URI**, "Transaction pooler" (port 6543). Turn it into a
   SQLAlchemy URL by changing the scheme:
   `postgresql+psycopg://postgres.<ref>:<password>@aws-0-<region>.pooler.supabase.com:6543/postgres`
   That is `DATABASE_URL`.
4. Nothing to load by hand: the course (sheets + theory) is read from the YAML in the image on every start, and the
   pre-generated "troba l'error" documents / quizzes are imported on the first start (and when a deploy adds files).
   `uv run python scripts/db.py import-generats` / `stats` do it from your machine.

### Changing the schema

Migrations are append-only: an applied file is never edited.
1. Change the SQLModel records (`backend/core/*/infra/sqlmodel_repository.py`).
2. `make db-schema` refreshes the snapshot `supabase/schema.sql` (the full DDL the code expects).
3. Add `supabase/migrations/<timestamp>_<what>.sql` with the `ALTER`/`CREATE` statements.
4. CI applies every migration to an empty Postgres and fails if the result differs from the code
   (`scripts/db.py check-migrations`), and diffs the snapshot.

## Hosting (Render, via the blueprint)

1. Push the repo to GitHub (private).
2. Render → **New → Blueprint** → pick the repo. It reads `render.yaml`, builds the `Dockerfile`, and asks for
   `OPENAI_API_KEY`, `DATABASE_URL`, `TUTOR_CLAU_PROFESSOR`.
3. Every push to `main` redeploys (`autoDeploy`). Health check: `/health`.

Plan: **free** (512 MB, one instance, sleeps when idle; `plan: free` in `render.yaml`, so a blueprint sync never
upgrades it). Memory: the server is ~170 MB, each idle sympy worker ~70 MB, each capped at
`TUTOR_SYMPY_WORKER_MEMORY_MB`. A blueprint sync adds/updates the variables it declares but does not delete others:
remove a stale global `TUTOR_MODEL` in the dashboard by hand.

### Models

Measured (2026-10, `scripts/model_study.py`), price per 1M tokens in/out: `gpt-5.6-luna` 0.20/1.20,
`gpt-5.4-mini` 0.75/4.5, `gpt-5.5` 5/30. `gpt-5.6-luna` does well on the tutor stages and on grading
(`mistakes_grading`, `quiz_grading`) at ~1/5 the cost of `gpt-5.4-mini`. `gpt-5.4-mini` for every stage broke quiz
generation (output truncated at `max_tokens=20000`, NUL bytes in the JSON), so the generation/verification stages
(`quiz_generation`, `quiz_verification`, `quiz_audit`, `quiz_extraction`, `mistakes_generation`,
`mistakes_verification`) keep their defaults (`backend/core/shared/llm/infra/stage_configs.py`).
Costs measured with `gpt-5.6-luna`: a tutor turn ~$0.0037 (effort `none`). Generating with it (not the production
setting): a "Troba l'error" document ~$0.003–0.009 (3 of 4 succeeded), a "Cert o fals" quiz ~$0.034–0.047 in 2–4 min
(3 of 4; one truncated), mathematically correct 24/24 but with LaTeX corruption that the generation gates now reject.

Any Docker host works the same way (`docker build .`, set the env vars, expose `$PORT`). One server process: the
rate limiter and the start-up import assume it (scale with bigger instances, or move both out before adding workers).
Fly.io: `fly launch --no-deploy`, `fly secrets set OPENAI_API_KEY=… DATABASE_URL=… TUTOR_CLAU_PROFESSOR=…`, `fly deploy`.

## Local, production-like

```
docker compose up --build      # app + Postgres with the Supabase schema, http://localhost:8000
```

## Logs and data

- Every model call: table `llm_calls` (stage, model, tokens, latency, raw response, error).
- Every tutor turn: table `tutor_turns` (student message, reply, plan, full trace). Professors browse them at `#/professor`.
- Supabase **Table editor** or SQL editor to inspect; `python scripts/db.py stats` for counts.
- Backups: Supabase daily backups (Pro plan) or `pg_dump "$DATABASE_URL"`.
