# Ready2Code Unified Development Launcher (PowerShell / Windows)
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   ⚡ Starting Ready2Code Local Development Stack ⚡   " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

# 1. Environment files check
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "[Ready2Code] Created root .env from template." -ForegroundColor Green
}
if (!(Test-Path "api\.env")) {
    Copy-Item "api\.env.example" "api\.env"
    Write-Host "[Ready2Code] Created api\.env from template." -ForegroundColor Green
}
if (!(Test-Path "web\.env.local")) {
    Copy-Item "web\.env.example" "web\.env.local"
    Write-Host "[Ready2Code] Created web\.env.local from template." -ForegroundColor Green
}

# 2. Python environment check
$PythonExe = Join-Path $ProjectRoot "venv\Scripts\python.exe"
if (!(Test-Path $PythonExe)) {
    Write-Host "[Ready2Code] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    & $PythonExe -m pip install --upgrade pip
    & $PythonExe -m pip install -r api\requirements.txt pytest pytest-asyncio
}

# 3. Database initialization & seed (idempotent)
Write-Host "[Ready2Code] Initializing database and verifying 100-problem bank..." -ForegroundColor Yellow
& $PythonExe api\scripts\seed.py

# 4. Check for port conflicts
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($port8000) {
    Write-Host "[Ready2Code] Note: Port 8000 has an active connection (PID: $($port8000.OwningProcess[0]))." -ForegroundColor DarkGray
}
$port3000 = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($port3000) {
    Write-Host "[Ready2Code] Note: Port 3000 has an active connection (PID: $($port3000.OwningProcess[0]))." -ForegroundColor DarkGray
}

Write-Host "--------------------------------------------------------" -ForegroundColor Cyan
Write-Host " Launching services in separate processes:" -ForegroundColor Cyan
Write-Host " -> Backend API:  http://localhost:8000 (Swagger: /docs)" -ForegroundColor Green
Write-Host " -> Frontend Web: http://localhost:3000" -ForegroundColor Green
Write-Host "--------------------------------------------------------" -ForegroundColor Cyan

# Start API in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot'; .\venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --app-dir api --port 8000"

# Start Frontend in a new window
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$ProjectRoot\web'; npx next dev -p 3000"

Write-Host "[Ready2Code] Both services launched successfully! Press Ctrl+C in their respective windows to stop." -ForegroundColor Green
