$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "  InsightFlow AI — Backend" -ForegroundColor Cyan
Write-Host "  FastAPI on http://localhost:8000" -ForegroundColor DarkGray
Write-Host "  API docs: http://localhost:8000/docs" -ForegroundColor DarkGray
Write-Host ""

Set-Location "$PSScriptRoot\backend"

if (-not (Test-Path ".env")) {
    Write-Host "  ERROR: backend/.env not found." -ForegroundColor Red
    Write-Host "  Copy backend/.env.example to backend/.env and fill in your credentials." -ForegroundColor Yellow
    exit 1
}

python run.py
