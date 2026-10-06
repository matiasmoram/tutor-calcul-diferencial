# Tutor socràtic · Càlcul Diferencial — production image.
# Secrets are NOT baked in: pass them as environment variables at run time (see DEPLOY.md).
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Code, course content (sheets, theory) and the course PDFs served under /pdf.
COPY backend/ backend/
COPY frontend/ frontend/
COPY scripts/ scripts/
COPY sources/ sources/
COPY supabase/ supabase/

# Run as an unprivileged user.
RUN useradd --create-home tutor && chown -R tutor /app
USER tutor

WORKDIR /app/backend
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s CMD python -c "import urllib.request,os; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\",\"8000\")}/api/config')"
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips='*'"]
