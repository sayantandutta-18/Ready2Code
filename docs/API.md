# API.md - Backend API reference

Base URL (local): `http://localhost:8000`
Interactive docs (local): `http://localhost:8000/docs`

The frontend calls the API through `NEXT_PUBLIC_API_URL`. Keep this value in sync with the running backend port.

## Conventions
- JSON in, JSON out. Content type `application/json`.
- Every response is a Pydantic model. Lists use `{ "items": [...], "total": n, "page": n, "page_size": n }`.
- Errors use one shape: `{ "error": { "code": "string", "message": "human readable", "request_id": "..." } }`.
- Stack traces are never returned in production (`ENVIRONMENT=production`).
- Hidden test data is never returned by any endpoint.

## Implemented endpoints (verify against `/docs` before relying on them)
| Method | Path | Purpose |
|---|---|---|
| GET | `/` | Root check (returns 200) |
| GET | `/health` | Reports `db`, `redis`, `judge0` status separately |
| GET | `/problems` | List problems. Query: `topic`, `difficulty`, `tag`, `company`, `status`, `q`, `page`, `page_size`, `limit` |
| GET | `/problems/{slug}` | One problem with statement, examples, starter code. No hidden tests |
| GET | `/daily` | Today's daily problem (planned to read from `daily_problems`) |
| POST | `/submissions/run` | Run code on sample tests. Planned in checkpoint S1.2 |
| POST | `/submissions` | Submit code against hidden tests. Planned in checkpoint S1.2 |

## Health check
`GET /health` example response (target shape):
```json
{ "status": "ok", "db": true, "redis": true, "judge0": false }
```
- `db: false` - Postgres not reachable. Check Docker and `DATABASE_URL`.
- `redis: false` - Redis not reachable or password wrong.
- `judge0: false` - Judge0 not running. Problem list still works; Run and Submit do not.

## Query examples
```
GET /problems?topic=Strings&difficulty=easy
GET /problems?limit=200          (use for checks; the page uses page/page_size)
GET /problems/two-sum
```

## Rate limits (planned, Stage 7)
- Submissions: 30 per minute per user.
- AI endpoints: 20 per user per day.
Return `429` with a friendly message: "You are submitting too fast. Wait a minute and try again."

## Judge contract (used by Run and Submit)
- The judge receives JSON arguments on stdin, one value per parameter: `[[2,7,11,15], 9]`.
- The user's function returns a JSON value on stdout: `[0,1]`.
- Each problem stores `function_name` and `params`. The harness wraps the user's code and calls that function.

## Errors you may see
| Code | Meaning | What to do |
|---|---|---|
| 404 `problem_not_found` | Slug does not exist | Check the slug in `content/index.json` |
| 422 | Request body or query invalid | Read `detail` in `/docs` |
| 503 `judge_unavailable` | Judge0 down | Start Judge0 or show "Judge is unavailable, try again" |
| 429 | Rate limit | Wait and retry |

## Adding an endpoint
1. Add a Pydantic schema in `api/app/schemas/`.
2. Add a router function in `api/app/routers/`.
3. Add a pytest test in `api/tests/`.
4. Add the row to the table above.
