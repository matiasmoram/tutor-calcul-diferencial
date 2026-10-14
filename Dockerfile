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

# Client IP behind Render's proxy. uvicorn's ProxyHeadersMiddleware only reads X-Forwarded-For when the TCP peer is
# trusted, then walks the list from the right and takes the first untrusted address: the one Render's proxy appended.
# Trusting '*' instead makes it take the leftmost entry, which the client writes itself (and so dodges the per-IP rate
# limit on the paid endpoints). Render's proxies reach the container from private addresses; if another hop (e.g. a
# CDN) shows up as the client, add its ranges here or in the service environment. The rate limiter's key
# (dependencies.client_key, the rightmost X-Forwarded-For hop) is the same address on Render.
ENV FORWARDED_ALLOW_IPS=127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s CMD python -c "import urllib.request,os; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\",\"8000\")}/health')"
CMD ["sh", "-c", "uvicorn apps.tutor_api.server:app --host 0.0.0.0 --port ${PORT} --proxy-headers"]
