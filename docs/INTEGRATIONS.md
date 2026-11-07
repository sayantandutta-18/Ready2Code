# INTEGRATIONS.md - External services

## PostgreSQL 16
- Local: Docker service `postgres`, port 5432.
- Config: root `.env` for Docker (`POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) and `api/.env` for the app (`DATABASE_URL`). Keep them in sync.
- Production (planned): Neon or Supabase. Enable SSL. Use the connection string from the provider.

## Redis 7
- Local: Docker service `redis`, port 6379.
- Used for: contest leaderboards (sorted sets), caching of daily problem, rate-limit counters (planned).
- Config: `REDIS_URL=redis://:<password>@localhost:6379/0` if Redis has a password; `redis://localhost:6379/0` if not.
- If Redis is down, contests fall back to the database (planned behaviour).

## Judge0 CE (code execution)
- Local: Docker service `judge0`, port 2358. Optional until checkpoint S1.2.
- Env: `JUDGE0_URL=http://localhost:2358` locally; `JUDGE0_AUTH_TOKEN` if the instance is protected.
- Contract: stdin = JSON arguments, stdout = JSON return value (see API.md).
- Limits per problem: `time_limit_ms`, `memory_limit_mb` from the problem JSON.
- Security: run on a separate host with no outbound network in production. Never run user code on the API server.
- If Judge0 is unavailable, return `503 judge_unavailable`. Never fake a verdict.

## Anthropic API (AI features, Stage 8)
- Called from the server only. `ANTHROPIC_API_KEY` must never reach the browser.
- Features: Socratic hints, code review, error explainer, mock interviewer.
- Rules: system prompt forbids full solutions; rate limit per user; log token use.
- Not needed for Stages 0 to 7.

## Auth provider (decision pending)
- See AUTH.md. If Clerk: keys in `web/.env.local` (publishable) and `api/.env` (secret). Webhook endpoint in FastAPI creates a `users` row.

## Sentry (optional)
- `SENTRY_DSN` empty = disabled. The API logs "Sentry DSN not provided" at startup; this is normal.
- Set a DSN only in production.

## Hosting (planned, Stage 7)
| Part | Host | Notes |
|---|---|---|
| Web | Vercel | Root directory `web`. Set `NEXT_PUBLIC_API_URL` |
| API | Render or Railway | Deploy from `api/Dockerfile`, port 8000 |
| Database | Neon or Supabase | Daily backups, one restore test |
| Redis | Upstash or managed | Set password |
| Judge0 | Own VM | Separate network, no outbound access |

## GitHub
- Repo: `sayantandutta-18/Ready2Code` (public).
- Never commit `.env`, `api/.env`, `web/.env.local`, `node_modules/`, `venv/`, or `__pycache__/`. `.gitignore` covers these; check with `git status` before every commit.
- Use `git --no-pager` in the terminal to avoid the pager prompt.

## Environment variable summary
| Variable | Used by | Example (local) |
|---|---|---|
| `DATABASE_URL` | api | `postgresql://user:pass@localhost:5432/ready2code_dev` |
| `REDIS_URL` | api | `redis://localhost:6379/0` |
| `JUDGE0_URL` | api | `http://localhost:2358` |
| `CORS_ORIGINS` | api | `http://localhost:3000,http://127.0.0.1:3000` |
| `ENVIRONMENT` | api | `development` |
| `DEBUG` | api | `true` (dev only) |
| `JWT_SECRET` | api | long random string |
| `DEV_DEMO_LOGIN` | api, web | `true` (dev only) |
| `SENTRY_DSN` | api, web | empty locally |
| `NEXT_PUBLIC_API_URL` | web | `http://localhost:8000` |
| `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_DB` / `POSTGRES_PORT` | Docker (root `.env`) | see SETUP.md |
