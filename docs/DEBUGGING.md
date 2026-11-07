# DEBUGGING.md - Known problems and fixes (Windows + PowerShell)

Find your error text below. Each entry: what it means, how to confirm, the fix.

## "Failed to fetch" on any page (problems, roadmap, sign-in)
- Meaning: the browser could not get any response from the API. Not a bug in that one page.
- Confirm: open `http://localhost:8000/health`. If it does not load, the API is not running.
- Fix: start the backend in its own window (see SETUP.md step 6). Keep that window open.

## `ECONNREFUSED ::1:8000` or `127.0.0.1:8000` in the frontend terminal
- Meaning: nothing is listening on port 8000. The Next.js proxy (`/daily`, `/problems`) failed.
- Fix: start the API. Check the API window does not print `Shutting down`.

## `Application startup complete` followed by `Shutting down`
- Meaning: the server stopped. Usually the window was closed, Ctrl+C was pressed, or a `--reload` restart happened while you copied text.
- Fix: run uvicorn without `--reload` while testing. Right-click to copy text in the terminal; do not press Ctrl+C by accident.

## `[Errno 10048] only one usage of each socket address`
- Meaning: port 8000 (or 3000) is already used by an old process.
- Fix:
```powershell
netstat -ano | findstr :8000
taskkill /PID <PID_number> /F
```

## `spawn EINVAL` when running `npm run dev`
- Meaning: `web/scripts/dev.js` cannot spawn `next` on Windows.
- Fix: use `npx next dev -p 3000` inside `web/`.

## `The token '&&' is not a valid statement separator`
- Meaning: PowerShell 5.x does not support `&&`.
- Fix: put each command on its own line, or use `;`.

## `.\venv\Scripts\Activate.ps1 is not recognized`
- Meaning: the venv folder does not exist yet, or you are in the wrong folder.
- Fix:
```powershell
cd "C:\Users\<you>\OneDrive\Desktop\Ready2Code"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r api\requirements.txt
```
If activation is blocked: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`.

## `Cannot find path ... api\.env` or `api\alembic.ini`
- Meaning: the file is not where the command expects.
- Fix: find it with `dir -Recurse -Filter .env*` or `dir -Recurse -Filter alembic.ini`, then use that path.

## `FAILED: No 'script_location' key found in configuration`
- Meaning: alembic was run with a config file that is not the Alembic config (or from the wrong folder).
- Fix: run `alembic -c <path-to-the-real-alembic.ini> upgrade head` from the project root.

## `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine`
- Meaning: Docker Desktop is not running.
- Fix: open Docker Desktop, wait for "Engine running", then retry.

## `no such service: db`
- Meaning: the service name in `docker-compose.yml` is different.
- Fix: `docker compose config --services` and use the printed name (here: `postgres`, `redis`, `api`, `judge0`, `web`).

## `password authentication failed for user`
- Meaning: the password in `DATABASE_URL` is not the one Postgres was created with.
- Fix: make `api\.env`, the root `.env` and `docker-compose.yml` use the same user, password and database. If the Postgres volume was created with an old password, reset local data (DATABASE.md "Local reset") or change the password inside the container.

## `NOAUTH Authentication required` (Redis)
- Meaning: Redis needs a password and `REDIS_URL` has none (or the reverse).
- Fix: `REDIS_URL=redis://:<REDIS_PASSWORD>@localhost:6379/0`. Remove the password part if Redis has none.

## `relation "problems" does not exist`
- Meaning: migrations were not applied to this database.
- Fix: `alembic -c api\migrations\alembic.ini upgrade head`, then seed.

## Only 1 problem shows on `/problems`
- Check in order: count files in `content/problems/*.json` (should be 100); call `http://localhost:8000/problems?limit=200` (should show 100); check frontend page size and default filters.
- If the API shows 100 but the page shows 1: frontend pagination or filter bug.

## `Loaded 0 new problems (all problems already present in database)`
- Meaning: this is good. The seed is idempotent. Problems are already in the database.

## git push rejected: `non-fast-forward`
- Meaning: GitHub has commits you do not have locally.
- Fix: `git pull --no-rebase --no-edit origin main`, resolve conflicts (keep the version you want), then `git push`.

## git error: `fatal: Cannot do a soft reset in the middle of a merge`
- Meaning: an unfinished merge is in progress.
- Fix: `git merge --abort`, then retry the pull.

## Pager prompts (`:`, `(press RETURN)`, `SUMMARY OF LESS COMMANDS`)
- Meaning: git opened `less`.
- Fix: press `q`. Use `git --no-pager <command>` or `git config --global core.pager ""`.

## Accidentally committed a file with a strange name (for example from a quote mistake)
- Fix: `git reset --soft HEAD~1`, `git reset`, delete the stray file, commit again.

## Checklist when something is broken
1. Is Docker Desktop running? (`docker ps`)
2. Is the API running and healthy? (`/health`)
3. Are the database and Redis `true`?
4. Are there 100 problems? (`/problems?limit=200`)
5. Is the browser console showing an error? (F12)
6. Did the last command print an error, or only warnings?
