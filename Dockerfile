# Tutor socràtic · Càlcul Diferencial — production image.
# Secrets are NOT baked in: pass them as environment variables at run time (see DEPLOY.md).
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     UV_COMPILE_BYTECODE=1     UV_LINK_MODE=copy     UV_PROJECT_ENVIRONMENT=/opt/venv     PATH=/opt/venv/bin:$PATH     PORT=8000

WORKDIR /app

COPY pyproject.toml uv.lock ./
# Dependencies first (cached layer), then the project itself once its code is in.
RUN uv sync --locked --no-dev --no-install-project

# Code, course content (sheets, theory) and the course PDFs served under /pdf.
COPY backend/ backend/
COPY frontend/ frontend/
COPY scripts/ scripts/
COPY sources/ sources/
COPY supabase/ supabase/
RUN uv sync --locked --no-dev

# Run as an unprivileged user.
RUN useradd --create-home tutor && chown -R tutor /app
USER tutor

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s CMD python -c "import urllib.request,os; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\",\"8000\")}/health')"
CMD ["sh", "-c", "uvicorn apps.tutor_api.server:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips='*'"]
