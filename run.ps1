# Starts the tutor at http://127.0.0.1:8000
Set-Location $PSScriptRoot\backend
..\.venv\Scripts\python.exe -m uvicorn app:app --reload --port 8000
