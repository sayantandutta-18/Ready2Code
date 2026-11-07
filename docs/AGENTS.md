# AGENTS.md - Rules for AI coding agents

This file is for AI coding tools (Antigravity, Claude Code, Cursor and similar) working on Ready2Code.
Read it before every session.

## Start of every session
1. Read `PROJECT_STATUS.md` and `AUDIT.md` in the repo root.
2. Do only the checkpoint named in the prompt (for example `S1.2`). Do not start the next one.
3. List the files you plan to change before editing.

## Hard rules
- No hard-coded problems, topics, companies, counts or stats in the frontend or API. Read them from the database or from `content/`.
- Never print, commit or hard-code secrets. `.env`, `api/.env`, `web/.env.local` are never committed. Only `*.example` files are committed.
- Never return hidden test input or output to the browser.
- Never show the full solution in the code editor. Starter code is a stub.
- Every data-driven page shows loading, empty and error states. Error text must say what to do next, not "Error 500".
- Do not add new pages until Stage 1 (judge and accounts) is green.
- Do not change the database schema destructively. Use an Alembic migration and ask first.
- Do not delete working features to make a test pass.

## Done means
- The checkpoint's "Done when" test passes in the browser, not only in code.
- Relevant tests pass (see `TESTING.md`). The 13 existing API tests must still pass.
- `npx next build` (or `npm run build` inside `web/`) passes.
- `PROJECT_STATUS.md` is updated with the checkpoint ID, what changed and what is still open.
- Commit with the checkpoint ID: `S1.2: real judge verdicts`.
- Stop and report. Include the exact command run and its result.

## Evidence required in your report
- Commands run and their output (last 10 lines is enough).
- URLs opened and what they showed.
- Any test that failed, and why.

## Code style
- TypeScript strict in `web/`; avoid `any`.
- Pydantic models for every request and response in `api/`.
- SQLAlchemy ORM only. No raw SQL string building.
- Use `datetime.now(timezone.utc)`, not `datetime.utcnow()`.

## Where things are
- `web/` - Next.js 14 app (App Router, TypeScript, Tailwind, Monaco, React Three Fiber)
- `api/` - FastAPI service (SQLAlchemy, Alembic, Pydantic)
- `content/problems/` - one JSON file per problem
- `content/scripts/` - content generator and validator
- `scripts/` - repo-level scripts (validate_problems.py)
- `tests/e2e/` - Playwright tests
- `docs/` - PDFs and project docs

## Things to avoid
- Running `npm run dev` on Windows: `web/scripts/dev.js` fails with `spawn EINVAL`. Use `npx next dev -p 3000`.
- Using `&&` in PowerShell 5.x. Use `;` or separate lines.
- Changing ports without updating `CORS_ORIGINS` and `NEXT_PUBLIC_API_URL`.
