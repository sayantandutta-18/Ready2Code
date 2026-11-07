# SETUP.md - Local setup (Windows 10/11, PowerShell)

## Prerequisites
| Tool | Version | Check |
|---|---|---|
| Python | 3.12 or newer (3.14 is used in development) | `python --version` |
| Node.js | 20 or newer (Node 24 works) | `node --version` |
| npm | comes with Node | `npm --version` |
| Docker Desktop | latest | `docker --version` and "Engine running" in the app |
| Git | latest | `git --version` |

## Step 1: Open the project
```powershell
cd "C:\Users\<you>\OneDrive\Desktop\Ready2Code"
```

## Step 2: Python environment (once)
```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
pip install -r api\requirements.txt
```
The prompt should now start with `(venv)`. Activate it in every new backend window.

## Step 3: Environment files (once)
Copy the examples, then edit the copies. Do not commit them.
```powershell
copy .env.example .env
copy api\.env.example api\.env
copy web\.env.example web\.env.local
```

Root `.env` (for Docker):
```dotenv
POSTGRES_USER=ready2code
POSTGRES_PASSWORD=<choose-a-password>
POSTGRES_DB=ready2code_dev
POSTGRES_PORT=5432
REDIS_PASSWORD=<choose-a-password>
REDIS_PORT=6379
```

`api\.env` (for the API). Use the same values:
```dotenv
DATABASE_URL=postgresql://ready2code:<choose-a-password>@localhost:5432/ready2code_dev
REDIS_URL=redis://:<redis-password>@localhost:6379/0
JUDGE0_URL=http://localhost:2358
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001
ENVIRONMENT=development
DEBUG=true
JWT_SECRET=<long-random-string>
DEV_DEMO_LOGIN=true
SENTRY_DSN=
```

`web\.env.local`:
```dotenv
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Password rules: avoid `@ : / # % ` and spaces. If you already used a password in a chat or screenshot, change it.

## Step 4: Start the database and Redis
```powershell
docker compose up -d postgres redis
docker compose ps
```
Both should show `running` (or `healthy`). If not: `docker compose logs postgres`.

## Step 5: Create tables and load problems
```powershell
alembic -c api\migrations\alembic.ini upgrade head
python api\scripts\seed.py
```
Expected: `Total problems in database: 100` and `Total topics in database: 10`.
A second run prints `Loaded 0 new problems`. That is correct.

## Step 6: Start the API (window 1, keep open)
Free port 8000 first if needed:
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```
Then:
```powershell
cd "C:\Users\<you>\OneDrive\Desktop\Ready2Code"
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --app-dir api --port 8000
```
Expected: `Application startup complete.` Do not close this window. Do not use `--reload` while testing.

## Step 7: Start the web app (window 2, keep open)
```powershell
cd "C:\Users\<you>\OneDrive\Desktop\Ready2Code\web"
npm install
npx next dev -p 3000
```
Use `npx next dev`, not `npm run dev` (Windows `spawn EINVAL` issue).

## Step 8: Check
| URL | Expected |
|---|---|
| http://localhost:8000/health | `db` and `redis` are `true` |
| http://localhost:8000/problems?limit=5 | 5 problems in JSON |
| http://localhost:3000/problems | Problem list with 100 problems over pages |

## Stopping
- Window 1 and window 2: press Ctrl+C in each window.
- Docker: `docker compose stop` (keeps data). `docker compose down` stops and removes containers (data stays in the volume). `docker compose down -v` deletes local data.

## Next time
Start Docker Desktop, then Step 4 (only `up -d`), then Steps 6 and 7. Steps 2, 3 and 5 are done once.

## If something fails
See `DEBUGGING.md`. Find the exact error text and follow the entry.
