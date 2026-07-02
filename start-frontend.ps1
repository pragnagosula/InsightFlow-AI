$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "  InsightFlow AI — Frontend" -ForegroundColor Cyan
Write-Host "  Vite dev server on http://localhost:5173" -ForegroundColor DarkGray
Write-Host "  Proxies /api and /storage to localhost:8000" -ForegroundColor DarkGray
Write-Host ""

Set-Location "$PSScriptRoot\frontend"

if (-not (Test-Path "node_modules")) {
    Write-Host "  node_modules not found — running npm install first..." -ForegroundColor Yellow
    npm install
}

npm run dev
