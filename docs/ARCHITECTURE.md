# ARCHITECTURE.md

## Components
```
Browser
  |  (same origin in production through a reverse proxy; localhost:3000 -> localhost:8000 in dev)
  v
Next.js 14 web app (web/, port 3000)
  - pages, Monaco editor, React Three Fiber scenes, TanStack Query
  |
  v  HTTP JSON
FastAPI api (api/, port 8000)
  - routers, Pydantic schemas, SQLAlchemy ORM, rate limits, structured logs
  |          |              |
  v          v              v
PostgreSQL  Redis          Judge0 CE (port 2358)
(port 5432) (port 6379)    isolated code execution
```

## Ports (local)
| Service | Port | Started by |
|---|---|---|
| Web (Next.js) | 3000 | `npx next dev -p 3000` in `web/` |
| API (FastAPI) | 8000 | `python -m uvicorn app.main:app --app-dir api --port 8000` |
| PostgreSQL | 5432 | `docker compose up -d postgres` |
| Redis | 6379 | `docker compose up -d redis` |
| Judge0 | 2358 | `docker compose up -d judge0` (optional until S1.2) |

## Data flow: opening a problem
1. Browser loads `/problems/[slug]`.
2. Page calls `GET /problems/{slug}` through TanStack Query.
3. API reads the problem, its examples and starter code from Postgres.
4. Hidden tests are never selected for this response.

## Data flow: Submit (planned, S1.2)
1. Browser sends `POST /submissions` with `problem_id`, `language`, `code`.
2. API loads hidden tests from Postgres (server side only).
3. API sends each test to Judge0 with the time and memory limits.
4. API maps the result to Accepted, Wrong Answer, TLE, RE or CE.
5. API stores the submission and updates `user_problem_status`.
6. API returns the verdict, the failing test index (not its data), runtime and memory.
7. If Judge0 is down, API returns `503 judge_unavailable`. It must not store a fake verdict.

## Content pipeline
```
content/scripts/problems_bank.py   (source of truth for launch problems, development only)
        |  build_content.py
        v
content/problems/*.json             (committed; one file per problem)
content/index.json
        |  api/scripts/seed.py      (idempotent; upserts by slug)
        v
PostgreSQL: topics, problems, problem_tests, problem_hints
```
The API and frontend never import `problems_bank.py`. They read only the database.

## Frontend structure
- `web/app/` - routes (App Router)
- `web/components/3d/` - lazy-loaded 3D scenes (never loaded on `/problems`)
- `web/components/ui/` - buttons, cards, verdict badges
- `web/styles/tokens.css` - design tokens (see DESIGN.md)

## Backend structure
- `api/app/main.py` - app factory, CORS, middleware, routers
- `api/app/routers/` - endpoints
- `api/app/models/` - SQLAlchemy models
- `api/app/schemas/` - Pydantic models
- `api/app/judge/` - Judge0 client and verdict mapping (planned)
- `api/migrations/` - Alembic migrations
- `api/scripts/seed.py` - loads `content/`

## Environments
| | Local dev | Production (planned) |
|---|---|---|
| Web | `next dev` on localhost:3000 | Vercel |
| API | uvicorn on localhost:8000 | Render or Railway (Docker) |
| Database | Docker Postgres | Neon or Supabase |
| Redis | Docker Redis | Upstash or managed Redis |
| Judge0 | Docker (optional) | Separate VM, no outbound network |

## Decisions
- FastAPI over Node: the solutions and the content pipeline are Python, so tests and the judge contract stay in one language.
- Judge0 first, own sandbox later: faster to launch; replace only if cost or latency requires.
- Same-origin API through rewrites (planned): removes most CORS issues.
- Visualizer reads traces by slug from `content/traces/` (planned).
