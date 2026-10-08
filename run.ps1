# Starts the tutor at http://127.0.0.1:8000
Set-Location $PSScriptRoot
.\.venv\Scripts\python.exe -m uvicorn apps.tutor_api.server:app --reload --port 8000
