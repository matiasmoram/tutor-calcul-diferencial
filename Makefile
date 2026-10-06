# Dev entry points. Everything runs through uv with backend/ on the import path (see pyproject.toml).
.PHONY: install test lint types check run db-schema

install:
	uv sync

test:
	uv run pytest -q $(ARGS)

lint:
	uv run ruff check backend scripts tests
	uv run ruff format --check backend/core backend/apps backend/settings

types:
	uv run pyright

check: lint types test

run:
	cd backend && uv run --env-file ../.env uvicorn app:app --reload --port 8000

db-schema:
	uv run python scripts/db.py schema > supabase/migrations/20261006000000_init.sql
