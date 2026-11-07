# Ready2Code — Comprehensive Codebase Audit (Phase 0)

Date: November 2026  
Status: Phase 0 Completed  
Workspace: `Ready2Code` (Interactive 3D DSA Arena)

---

## 1. Route Audit (`web/app`)

Every route in `web/app`, its data consumption model, API endpoints called, and hard-coded/mock elements:

| Route | File Path | Data Source Category | API Endpoint Called (if any) | Hard-coded / Mock Data Elements |
| :--- | :--- | :--- | :--- | :--- |
| `/` | `web/app/page.tsx` | Partial API | `GET /daily` | Stats counters (63+ problems, 15 patterns), hero problem fallback state. |
| `/analytics` | `web/app/analytics/page.tsx` | Partial API | `GET /analytics` | Fallback initial chart structure if API fails. |
| `/battles` | `web/app/battles/page.tsx` | Partial API | `POST /battles/queue`, `GET /battles/{id}` | Active duelists counter (412 Online), Season 4 champion banner, rules list. |
| `/battles/[id]` | `web/app/battles/[id]/page.tsx` | Partial API | `GET /battles/{id}`, `POST /battles/{id}/submit` | Opponent test progress simulated via client `setInterval`, initial problem state. |
| `/certificates/[code]` | `web/app/certificates/[code]/page.tsx` | Partial API | `GET /certificates/verify/{code}` | Fallback mock certificate if verification fails. |
| `/companies` | `web/app/companies/page.tsx` | Real API | `GET /companies` | None (reads dynamically from `GET /companies` via TanStack Query). |
| `/companies/[name]` | `web/app/companies/[name]/page.tsx` | Real API | `GET /companies/{name}` | None (reads company roadmap and milestones from backend API). |
| `/contests` | `web/app/contests/page.tsx` | Real API | `GET /contests`, `GET /leaderboard` | Fallback contest list if API unreachable. |
| `/contests/[id]` | `web/app/contests/[id]/page.tsx` | Real API | `GET /contests/{id}`, `GET /contests/{id}/standings` | Fallback mock contest if API unreachable. |
| `/daily` | `web/app/daily/page.tsx` | Real API | `GET /daily`, `POST /daily/freeze` | Fallback daily problem if API unreachable. |
| `/interviews` | `web/app/interviews/page.tsx` | Real API | `GET /interviews`, `POST /interviews` | None (reads debrief list from API and creates new experiences). |
| `/jobs` | `web/app/jobs/page.tsx` | Real API | `GET /jobs`, `POST /jobs/{id}/apply` | None (reads open jobs from API and posts applications). |
| `/ladder/[problem]` | `web/app/ladder/[problem]/page.tsx` | Real API | `GET /ladder/{problem}`, `POST /ladder/stage` | Fallback ladder steps if API unreachable. |
| `/leaderboard` | `web/app/leaderboard/page.tsx` | Real API | `GET /leaderboard` | Fallback top-5 users array if API unreachable. |
| `/lists` | `web/app/lists/page.tsx` | Real API | `GET /lists`, `GET /plans`, `POST /lists` | Fallback system lists (Blind 75, NeetCode 150). |
| `/lists/[id]` | `web/app/lists/[id]/page.tsx` | Real API | `GET /lists/{id}` | Fallback problem array if API unreachable. |
| `/login` | `web/app/login/page.tsx` | Real API | `POST /auth/login` | Demo profile buttons (`algo_ninja`, `byte_master`) when demo enabled. |
| `/mock` | `web/app/mock/page.tsx` | Partial API | `POST /ai/interview`, `POST /ai/review` | Hardcoded sample problem (Merge Intervals) and canned dialogue fallbacks. |
| `/patterns` | `web/app/patterns/page.tsx` | Real API | `GET /patterns` | Fallback pattern cards if API unreachable. |
| `/patterns/[id]` | `web/app/patterns/[id]/page.tsx` | Real API | `GET /patterns/{id}`, `POST /patterns/{id}/quiz` | Fallback pattern template and quiz if API unreachable. |
| `/placement` | `web/app/placement/page.tsx` | Real API | `GET /placement/questions` | Static track tab headers; questions loaded from API. |
| `/plans/[id]` | `web/app/plans/[id]/page.tsx` | Real API | `GET /plans/{id}` | Day checkboxes toggle local component state. |
| `/portfolio/[username]` | `web/app/portfolio/[username]/page.tsx` | Partial API | `GET /users/{username}` | Hardcoded activity tower stats; user profile read from API. |
| `/problems` | `web/app/problems/page.tsx` | Real API | `GET /problems`, `GET /topics` | None (100 problems, 25/page pagination, 10 topics from DB). |
| `/problems/[slug]` | `web/app/problems/[slug]/page.tsx` | Real API | `GET /problems/{slug}`, `POST /submissions/run`, `POST /submissions`, `GET /submissions`, `GET /notes/{id}`, `POST /notes`, `GET /users/me/bookmarks`, `POST /users/me/bookmarks/toggle` | None (Statement, tests, limits, Judge0 execution, notes, bookmarks from API). |
| `/profile/[username]` | `web/app/profile/[username]/page.tsx` | Real API | `GET /users/{username}` | Hardcoded badge rule templates; user stats from API. |
| `/register` | `web/app/register/page.tsx` | Real API | `POST /auth/register` | Demo profile quick-select chips when demo enabled. |
| `/review` | `web/app/review/page.tsx` | Real API | `GET /review`, `POST /review/grade` | Fallback flashcards array if API unreachable. |
| `/roadmap` | `web/app/roadmap/page.tsx` | Partial API | `GET /problems` | `TOPIC_CONFIG` hardcoded 8 topics instead of 10 from DB; problem data from API. |
| `/settings` | `web/app/settings/page.tsx` | Real API | `PATCH /users/me` | Timezone dropdown options static; user settings updated via API. |
| `/visualizer/[algo]` | `web/app/visualizer/[algo]/page.tsx` | **Placeholder / Mock** | None | Hardcoded traces (`TWO_SUM_TRACE`, `BUBBLE_SORT_TRACE`); client-only animation. |

---

## 2. API Endpoints Audit (`api/app/routers`)

All 58 endpoints across the 22 backend routers, their HTTP methods, paths, and frontend integration status:

| Router File | Method & Path | Called by Frontend? | Calling Frontend Component / Page | Notes |
| :--- | :--- | :---: | :--- | :--- |
| `ai.py` | `POST /ai/hint` | No | None | Available for Socratic hint bot. |
| `ai.py` | `POST /ai/review` | **Yes** | `web/app/mock/page.tsx` | Code review and complexity feedback. |
| `ai.py` | `POST /ai/interview` | **Yes** | `web/app/mock/page.tsx` | Interactive AI interview responses. |
| `ai.py` | `POST /ai/explain-verdict` | No | None | Backend explainer for failed test cases. |
| `analytics.py` | `GET /analytics` | **Yes** | `web/app/analytics/page.tsx` | Weekly solve counts and topic stats. |
| `analytics.py` | `GET /review` | **Yes** | `web/app/review/page.tsx` | Spaced repetition flashcards queue. |
| `analytics.py` | `POST /review/grade` | **Yes** | `web/app/review/page.tsx` | Grades spaced repetition flashcard. |
| `analytics.py` | `GET /leaderboard` | **Yes** | `web/app/leaderboard/page.tsx`, `web/app/contests/page.tsx` | Global XP and streak rankings. |
| `auth.py` | `POST /auth/register` | **Yes** | `web/lib/authContext.tsx`, `web/app/register/page.tsx` | User registration & JWT session. |
| `auth.py` | `POST /auth/login` | **Yes** | `web/lib/authContext.tsx`, `web/app/login/page.tsx` | User login & JWT session. |
| `auth.py` | `GET /auth/me` | **Yes** | `web/lib/authContext.tsx` | Validates session token & loads profile. |
| `battles.py` | `POST /battles/queue` | **Yes** | `web/app/battles/page.tsx` | Matchmaking queue for 1v1 duel. |
| `battles.py` | `GET /battles/{battle_id}` | **Yes** | `web/app/battles/[id]/page.tsx` | Duel status, problem, and opponent state. |
| `battles.py` | `POST /battles/{battle_id}/submit` | **Yes** | `web/app/battles/[id]/page.tsx` | Evaluates duel submission. |
| `certificates.py` | `POST /certificates/issue` | No | Tested via Pytest | Timed certification test issuance. |
| `certificates.py` | `GET /certificates/verify/{verify_code}` | **Yes** | `web/app/certificates/[code]/page.tsx` | Public certificate verification. |
| `companies.py` | `GET /companies` | **Yes** | `web/app/companies/page.tsx` | List of company preparation tracks. |
| `companies.py` | `GET /companies/{slug}` | **Yes** | `web/app/companies/[name]/page.tsx` | Company detailed roadmap & days. |
| `contests.py` | `GET /contests` | **Yes** | `web/app/contests/page.tsx` | List of live/past contests. |
| `contests.py` | `GET /contests/{contest_id}` | **Yes** | `web/app/contests/[id]/page.tsx` | Contest details and problem set. |
| `contests.py` | `GET /contests/{contest_id}/standings` | **Yes** | `web/app/contests/[id]/page.tsx` | Live contest scoreboard. |
| `contests.py` | `POST /contests/{contest_id}/submit` | No | UI wires to submissions router | Contest problem submission. |
| `contests.py` | `GET /contests/ratings/{username}` | No | None | Historical rating progression. |
| `daily.py` | `GET /daily` | **Yes** | `web/app/page.tsx`, `web/app/daily/page.tsx` | Daily challenge problem and streak. |
| `daily.py` | `POST /daily/freeze` | **Yes** | `web/app/daily/page.tsx` | Consumes streak freeze protection. |
| `discussions.py` | `GET /discussions/problem/{problem_slug}` | No | None | Problem discussion forum threads. |
| `discussions.py` | `POST /discussions` | No | None | Post community solution or comment. |
| `discussions.py` | `POST /discussions/vote` | No | None | Upvote/downvote comment. |
| `health.py` | `GET /health` | No | Docker & cloud healthchecks | Multi-service health check (DB, Redis, Judge0). |
| `interviews.py` | `GET /interviews` | **Yes** | `web/app/interviews/page.tsx` | Company interview debrief cards. |
| `interviews.py` | `POST /interviews` | **Yes** | `web/app/interviews/page.tsx` | Share student interview experience. |
| `jobs.py` | `GET /jobs` | **Yes** | `web/app/jobs/page.tsx` | Curated hiring opportunities. |
| `jobs.py` | `POST /jobs/{job_id}/apply` | **Yes** | `web/app/jobs/page.tsx` | 1-click fast track job application. |
| `ladder.py` | `GET /ladder/{problem_slug}` | **Yes** | `web/app/ladder/[problem]/page.tsx` | Multi-stage algorithmic ladder. |
| `ladder.py` | `POST /ladder/stage` | **Yes** | `web/app/ladder/[problem]/page.tsx` | Validates complexity ladder stage. |
| `lists.py` | `GET /lists` | **Yes** | `web/app/lists/page.tsx` | Curated problem lists (Blind 75, etc.). |
| `lists.py` | `GET /lists/{list_id}` | **Yes** | `web/app/lists/[id]/page.tsx` | List details and items. |
| `lists.py` | `POST /lists` | **Yes** | `web/app/lists/page.tsx` | Creates user custom list. |
| `lists.py` | `PUT /lists/{list_id}/reorder` | No | None | Reorders list items. |
| `notes.py` | `GET /notes/{problem_id}` | **Yes** | `web/app/problems/[slug]/page.tsx` | Retrieves user problem notes. |
| `notes.py` | `POST /notes` | **Yes** | `web/app/problems/[slug]/page.tsx` | Autosaves user notes. |
| `patterns.py` | `GET /patterns` | **Yes** | `web/app/patterns/page.tsx` | 15 core algorithmic patterns. |
| `patterns.py` | `GET /patterns/{slug}` | **Yes** | `web/app/patterns/[id]/page.tsx` | Pattern detail & template code. |
| `patterns.py` | `POST /patterns/{slug}/quiz` | **Yes** | `web/app/patterns/[id]/page.tsx` | Evaluates pattern quiz answer. |
| `placement.py` | `GET /placement/tracks` | No | None | Returns track metadata. |
| `placement.py` | `GET /placement/questions` | **Yes** | `web/app/placement/page.tsx` | CS fundamentals questions (OS, DBMS, Networks). |
| `plans.py` | `GET /plans` | **Yes** | `web/app/lists/page.tsx` | Bootcamp study schedules. |
| `plans.py` | `GET /plans/{plan_id}` | **Yes** | `web/app/plans/[id]/page.tsx` | Day-by-day plan problem schedule. |
| `problems.py` | `GET /problems` | **Yes** | `web/app/problems/page.tsx`, `web/app/roadmap/page.tsx` | 100 problems with server-side filters & pagination. |
| `problems.py` | `GET /problems/{slug}` | **Yes** | `web/app/problems/[slug]/page.tsx` | Full problem statement, sample tests, limits, hints. |
| `submissions.py` | `POST /submissions/run` | **Yes** | `web/app/problems/[slug]/page.tsx` | Executes user code on sample test cases. |
| `submissions.py` | `POST /submissions` | **Yes** | `web/app/problems/[slug]/page.tsx` | Evaluates hidden test cases via Judge0. |
| `submissions.py` | `GET /submissions` | **Yes** | `web/app/problems/[slug]/page.tsx` | Problem submission history. |
| `topics.py` | `GET /topics` | **Yes** | `web/app/problems/page.tsx` | 10 database topics and problem counts. |
| `users.py` | `GET /users/{username}` | **Yes** | `web/app/profile/[username]/page.tsx`, `web/app/portfolio/[username]/page.tsx` | User profile, solved count, rating, streak. |
| `users.py` | `PATCH /users/me` | **Yes** | `web/app/settings/page.tsx` | Updates user settings & preferences. |
| `users.py` | `GET /users/me/bookmarks` | **Yes** | `web/app/problems/[slug]/page.tsx` | User bookmarked problems. |
| `users.py` | `POST /users/me/bookmarks/toggle` | **Yes** | `web/app/problems/[slug]/page.tsx` | Toggles problem bookmark. |

---

## 3. Environment Variables Audit & Production Flags

### A. Frontend (`web`) Environment Variables

| Variable Name | Read By | Purpose | Masked Value | Production Status & Flags |
| :--- | :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | `web/lib/api.ts` | Base API URL for browser API requests | `http://localhost:8000` (local dev) | ⚠️ **FLAG: Default points to `http://localhost:8000`**. In production (Vercel), user browsers cannot reach localhost. Must be set to `<RENDER_URL>` in Vercel Environment Variables. |
| `API_INTERNAL_URL` | `web/next.config.js` | Target destination for Next.js server rewrites (`/api/:path*`) | `http://localhost:8000/:path*` | ⚠️ **FLAG: Default points to `http://localhost:8000` (or `http://api:8000` in Docker)**. On Vercel, serverless function rewrites cannot connect to `localhost:8000` or Docker internal `api:8000`. Must be updated to `<RENDER_URL>/:path*` or removed in favor of direct `NEXT_PUBLIC_API_URL` calls. |
| Next.js rewrites | `web/next.config.js` | Proxies `/api/:path*` to `API_INTERNAL_URL` | `source: /api/:path* -> destination: <API_INTERNAL_URL>` | ⚠️ **FLAG: Rewrites point to localhost by default**. In production on Vercel, must not rewrite to localhost or internal Docker hostnames. |

### B. Backend (`api`) Environment Variables

| Variable Name | Read By | Purpose | Masked Value | Production Status & Flags |
| :--- | :--- | :--- | :--- | :--- |
| `DATABASE_URL` | `api/app/config.py`, `api/alembic/env.py`, `api/scripts/seed.py` | Primary database connection string | `postgresql://ready2code:<POSTGRES_PASSWORD>@localhost:5432/ready2code_db` (local dev) | ⚠️ **FLAG: Default in `config.py` falls back to `sqlite:///./ready2code.db` and example files point to `localhost:5432`**. In production, must be set to Neon Postgres `<NEON_URL>` with `sslmode=require`. |
| `REDIS_URL` | `api/app/config.py`, `api/app/rate_limiter.py`, `api/app/routers/health.py` | Redis connection URL for caching & rate limiting | `redis://localhost:6379/0` (local dev) | ⚠️ **FLAG: Points to `localhost:6379`**. In production, must point to `<UPSTASH_REDIS_URL>` or be handled gracefully if Redis is disabled. |
| `CORS_ORIGINS` | `api/app/config.py`, `api/app/main.py` | Allowed CORS origins for browser fetch | `http://localhost:3000,http://127.0.0.1:3000,https://ready2code.vercel.app` | ✅ **OK**: Production origin `https://ready2code.vercel.app` is included in default list. |
| `JWT_SECRET` | `api/app/config.py`, `api/app/auth_deps.py`, `api/app/routers/auth.py` | Symmetric key for signing auth tokens | `<JWT_SECRET>` | ⚠️ **FLAG: Default in `config.py` is a hardcoded string**. Must be overridden in production with a 64+ char random secret. |
| `DEV_DEMO_LOGIN` | `api/app/config.py`, `web/lib/authContext.tsx`, `web/app/login/page.tsx` | Allows one-click demo credentials (`algo_ninja`) | `true` (local dev) | ⚠️ **FLAG: Must be explicitly set to `false` in production** to disable demo buttons and require registered accounts. |
| `ENVIRONMENT` | `api/app/config.py`, `api/app/main.py`, `api/app/logging_config.py` | App execution environment mode | `development` (local dev) | ⚠️ **FLAG: Must be set to `production` in production** to enable JSON logging, strict CORS credentials enforcement, and sanitize error responses. |
| `JUDGE0_URL` | `api/app/config.py`, `api/app/routers/submissions.py`, `api/app/routers/health.py` | Judge0 code evaluation API | `http://localhost:2358` (local dev), `http://judge0:2358` (docker) | ⚠️ **FLAG: Points to `http://localhost:2358` or `http://judge0:2358`**. In cloud production (Render/Railway), `judge0:2358` is unreachable unless Judge0 is hosted or public Judge0 CE is used. The submission endpoint correctly handles judge unavailability without crashing. |

---

## 4. Summary & Verification

- **31 Frontend Routes**: Audited and catalogued.
- **58 Backend API Endpoints**: Audited and cross-referenced with frontend calls.
- **Environment Flags**: All values pointing to `localhost`, `127.0.0.1`, `api:8000`, and `judge0:2358` have been flagged for the upcoming local setup (Phase 1) and production rollout (Phases 4-5).
- **Code Changes in Phase 0**: Zero code changes executed; purely audit report update.
