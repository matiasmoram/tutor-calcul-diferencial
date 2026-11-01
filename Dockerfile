# Tutor socràtic · Càlcul Diferencial — production image.
# Secrets are NOT baked in: pass them as environment variables at run time.
FROM ghcr.io/astral-sh/uv:0.11.15-python3.13-trixie-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH=/opt/venv/bin:$PATH \
    PORT=8000

WORKDIR /app

COPY pyproject.toml uv.lock ./
# Dependencies first (cached layer), then the project itself once its code is in.
RUN uv sync --locked --no-dev --no-install-project

# Code, course content (sheets, theory) and the course PDFs served under /pdf.
COPY backend/ backend/
COPY frontend/ frontend/
COPY sources/ sources/
# The project must stay an editable install: settings.ROOT_DIR resolves to /app through it, and frontend/, sources/
# and the course YAML are found from there. No --no-editable, no stage that copies only the venv.
# UV_COMPILE_BYTECODE covers site-packages only; backend/ is compiled here so a cold start does not do it.
RUN uv sync --locked --no-dev && python -m compileall -q backend

# Unprivileged user. /app stays owned by root: the server only reads it.
RUN useradd --create-home tutor
USER tutor

# uvicorn reads X-Forwarded-For only from these peers (Render's proxies use private addresses) and takes the rightmost
# untrusted hop, the one Render appends. '*' would make it take the leftmost entry, which the client writes, and so
# bypass the per-IP rate limit. If a CDN sits in front, add its ranges.
ENV FORWARDED_ALLOW_IPS=127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s CMD python -c "import urllib.request,os; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\",\"8000\")}/health')"
# exec: uvicorn is PID 1 and receives SIGTERM, so the shutdown hooks run. One worker: the rate limiter, the
# generation locks and the start-up seeding assume a single process (an explicit flag ignores WEB_CONCURRENCY).
CMD ["sh", "-c", "exec uvicorn apps.tutor_api.server:app --host 0.0.0.0 --port ${PORT} --workers 1 --proxy-headers --no-server-header"]
