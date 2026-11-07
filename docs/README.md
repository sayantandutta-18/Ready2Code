# Ready2Code

Practice data structures and algorithms with a real judge, step-by-step 3D visualizations, and placement-preparation tracks for students.

## What is in the repo
- `web/` - Next.js 14 app (TypeScript, Tailwind, Monaco editor, React Three Fiber)
- `api/` - FastAPI service (SQLAlchemy, Alembic, Pydantic)
- `content/` - 100 launch problems as JSON, plus generator and validator scripts
- `tests/e2e/` - Playwright end-to-end tests
- `docs/` - roadmap, blueprint and problem bank PDFs
- Documentation: `INDEX.md` lists every doc

## Quick start (Windows, PowerShell)
Full steps are in `SETUP.md`. Short version:

```powershell
# 1. Start Docker Desktop and wait for "Engine running"
docker compose up -d postgres redis

# 2. Backend (window 1, keep it open)
.\venv\Scripts\Activate.ps1
alembic -c api\migrations\alembic.ini upgrade head
python api\scripts\seed.py
python -m uvicorn app.main:app --app-dir api --port 8000

# 3. Frontend (window 2, keep it open)
cd web
npx next dev -p 3000
```

Open:
- Problems: http://localhost:3000/problems
- API health: http://localhost:8000/health
- API docs: http://localhost:8000/docs

## Status
Early development. Database and content work locally. Run and Submit, sign-in and several pages are still being completed. See `FEATURES.md` and `PLAN.md`.

## Tests
```powershell
python -m pytest api\tests
python content\scripts\validate_content.py
```
More in `TESTING.md`.

## Contributing
1. Read `AGENTS.md` and `PLAN.md`.
2. Write every problem statement in your own words. Do not copy text from other platforms.
3. Add a problem as a JSON file under `content/problems/`, with at least 8 hidden tests.
4. Run the validator. Open a pull request.

## Licence
MIT (see `LICENSE` when added).
