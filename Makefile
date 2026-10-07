# Dev entry points. Everything runs through uv with backend/ on the import path (see pyproject.toml).
.PHONY: install test lint types check run db-schema

install:
	uv sync

test:
	uv run pytest -q $(ARGS)

lint:
	uv run ruff check backend scripts
	uv run ruff format --check backend scripts

types:
	uv run pyright

check: lint types test

run:
	uv run uvicorn apps.tutor_api.server:app --reload --port 8000

db-schema:
	uv run python scripts/db.py schema > supabase/schema.sql
