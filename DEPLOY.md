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
| `TUTOR_MODEL` | recommended | `gpt-5.4-mini` for every stage (see `work/research/INFORME.md`) |
| `DATABASE_URL` | yes in production | Supabase connection string (below). Without it: local SQLite at `data/tutor.db` |
| `TUTOR_CLAU_PROFESSOR` | yes in production | Professor key. Students never see solutions/traces; professors open the app once with `?prof=<key>`. Unset: nobody sees them (unless `TUTOR_DEMO=1`) |
| `TUTOR_DEMO` | no | `1` = demo mode without a key: everyone sees solutions and traces. Local development only |
| `TUTOR_MODEL_REQUESTS_PER_MINUTE` | no | Per-client limit on the endpoints that call a model (default 20) |
| `TUTOR_LOG_PROMPTS` | no | `1` also stores full prompts in `llm_calls` (large) |

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
