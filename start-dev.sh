#!/bin/bash
set -e

echo "========================================================"
echo "   ⚡ Starting Ready2Code Local Development Stack ⚡   "
echo "========================================================"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# 1. Environment files check
[ ! -f ".env" ] && cp .env.example .env && echo "[Ready2Code] Created root .env"
[ ! -f "api/.env" ] && cp api/.env.example api/.env && echo "[Ready2Code] Created api/.env"
[ ! -f "web/.env.local" ] && cp web/.env.example web/.env.local && echo "[Ready2Code] Created web/.env.local"

# 2. Python environment check
if [ ! -d "venv" ]; then
    echo "[Ready2Code] Creating Python virtual environment..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r api/requirements.txt pytest pytest-asyncio
fi

# 3. Database initialization & seed
echo "[Ready2Code] Initializing database and verifying 100-problem bank..."
./venv/bin/python api/scripts/seed.py

# 4. Start services
echo "--------------------------------------------------------"
echo " -> Backend API:  http://localhost:8000"
echo " -> Frontend Web: http://localhost:3000"
echo "--------------------------------------------------------"

trap 'kill $(jobs -p)' EXIT

./venv/bin/python -m uvicorn app.main:app --app-dir api --port 8000 &
npm --prefix web run dev &

wait
