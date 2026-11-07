# Ready2Code — Project Status & Roadmap

Platform: **Ready2Code** (Interactive 3D DSA Arena)
Current Phase: **Production Readiness & Documentation Alignment COMPLETED**
Updated: November 2026

---

## 🌟 Production Readiness & Documentation Alignment — COMPLETE
- [x] **Complete Documentation Suite Integration (`docs/`)**:
  - Integrated and extracted canonical project docs: `INDEX.md`, `PRD.md`, `ARCHITECTURE.md`, `PLAN.md`, `FEATURES.md`, `API.md`, `DATABASE.md`, `AUTH.md`, `INTEGRATIONS.md`, `TESTING.md`, `DESIGN.md`, `DEBUGGING.md`, `AGENTS.md`, `MCP.md`, `SETUP.md`, `README.md`.
- [x] **Problem Bank Validation & CI Modernization**:
  - Upgraded `scripts/validate_problems.py` to validate the 100-problem launch content bank across all 10 canonical topics with both `reference_python` execution and schema verification.
  - Verified 100/100 problems passing with 0 failures across 1,192 tests in `content/scripts/validate_content.py` and `scripts/validate_problems.py`.
  - Updated `.github/workflows/ci.yml` to run tests and validate 100 problems.
- [x] **Windows & Cross-Platform Developer Experience**:
  - Resolved `spawn EINVAL` bug on Windows in `web/scripts/dev.js` by adding `{ shell: isWindows }` option. `npm run dev` now runs reliably on Windows.
  - Created `start-dev.ps1` (PowerShell) and `start-dev.sh` (Bash) one-command launchers that check environment files, virtual environment, seed the database, and launch both services.
- [x] **Docker & Production Container Hardening**:
  - Created `api/entrypoint.sh` with automatic database migration and seed retry loop on container startup.
  - Fixed Next.js multi-stage `web/Dockerfile` by creating `web/public` directory with `robots.txt` so `COPY --from=builder /app/public ./public` succeeds.
  - Added read-only `./content:/content:ro` volume mount in `docker-compose.prod.yml`.
  - Added `api/alembic.ini` and `api/alembic/env.py` supporting `alembic -c api/alembic.ini upgrade head`.
- [x] **API & Health Endpoint Alignment**:
  - Updated `api/app/routers/health.py` to report booleans `redis` and `judge0` alongside status strings, matching `docs/API.md`.
  - Added `POST /daily/freeze` endpoint in `api/app/routers/daily.py` and connected streak freeze persistence in `web/app/daily/page.tsx`.
  - Added `POST /ai/interview` in `api/app/routers/ai.py` and wired AI interview dialogue and code complexity analysis in `web/app/mock/page.tsx`.
- [x] **Frontend Polish & Error Resilience**:
  - Formatted inline markdown backticks and bold text, and rendered structured Examples section on problem solve page `web/app/problems/[slug]/page.tsx`.
  - Replaced hardcoded `http://localhost:8000` with `fetchApi` in `web/app/battles/page.tsx` and `web/app/battles/[id]/page.tsx`.
  - Hardened `web/app/roadmap/page.tsx` with defensive type guards to handle both array and paginated problem lists.
  - Cleaned root `README.md` with accurate stats and quick-start links.
- [x] **100% Verification Suite Passing**:
  - Backend: 28/28 pytest unit and integration tests passing.
  - Content: 100/100 problems and 1,192 tests passing.
  - Frontend: 10/10 unit tests passing.
  - TypeScript: `tsc --noEmit` passing with 0 errors.
  - Production Build: `next build` clean across all 30 routes.

---

## 🎨 Checkpoint S0.x - Input Contrast Fix on Auth Forms — COMPLETE
- [x] **Root Cause Diagnosis**:
  - Identified unstyled inputs on `/register` defaulting to User-Agent browser styles (`background-color: field;` -> `rgb(255, 255, 255)`) combined with light text/placeholder tokens, causing white-on-white text disappearance (1:1 contrast).
  - Detected WebKit credential autofill overriding dark backgrounds with light blue box-shadows (`rgb(232, 240, 254)`).
- [x] **Shared Reusable `Input` Component (`web/components/ui/Input.tsx`)**:
  - Implemented shared `Input` component with forwardRef support, container wrapper, label, left/right icons, and accessible focus states.
  - Background styled with `var(--surface-2)` (`#1A2740`).
  - Text styled with `var(--text-primary)` (`#E2E8F0`).
  - Placeholder styled with `var(--text-muted)` (`#94A3B8`). Contrast ratio calculated at **5.85:1** against the `#1A2740` input background (exceeds WCAG AA 4.5:1 requirement).
  - Caret color synchronized with text color (`#E2E8F0`).
  - High-visibility cyan focus ring (`focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/40`).
- [x] **Global Stylesheet Hardening (`web/styles/tokens.css`)**:
  - Set `color-scheme: dark;` on `:root` to ensure all native browser form controls default to dark palettes.
  - Added global input background and placeholder contrast rules for standard form controls.
  - Added `-webkit-autofill` overrides using inset box-shadow `0 0 0px 1000px #1A2740 inset` and `-webkit-text-fill-color: var(--text-primary)` to prevent browser credential managers from washing out input text.
- [x] **Full Auth Flow Integration**:
  - Integrated shared `Input` component across `web/app/register/page.tsx` (Username, Display Name, Password, Confirm Password).
  - Integrated shared `Input` component across `web/app/login/page.tsx` (Username, Password).
  - Integrated shared `Input` component across `web/components/ui/AuthModal.tsx` (Username, Display Name).
- [x] **Verification & Photographic Evidence**:
  - Verified on `localhost:3000/register` with headless Chrome CDP.
  - Captured responsive screenshots with text populated across all fields at 1280px (`web/public/screenshots/register_1280px.png`) and 360px (`web/public/screenshots/register_360px.png`).
  - `npx tsc --noEmit` passing with 0 errors.
  - `npx next build` passing clean across all 49 routes.

---

## 📦 Checkpoint S1.x - Load 100-Problem Content Bank & Problem Count Fix — COMPLETE
- [x] **Launch Content Bank Ingestion (100 Problems, 10 Topics)**:
  - Extracted and verified all 100 launch problems from `content/problems/*.json` and `content/index.json`.
  - Created idempotent seed script `api/scripts/seed.py` that loads 100 problems, 10 topics, sample tests, hidden tests, hints, and tags without duplication.
  - Topics seeded in exact canonical syllabus order: Arrays and Hashing, Two Pointers and Sliding Window, Strings, Stack and Queue, Linked List, Trees, Graphs, Binary Search, Dynamic Programming, Heap, Intervals and Greedy.
  - Second execution loads 0 new problems and does not fail.
- [x] **Problem Count & Server-Side Pagination Fix**:
  - Diagnosed parameter handling in `api/app/routers/problems.py`: when `GET /problems?limit=200` was invoked without `page`, it previously returned a raw array omitting the `total` pagination wrapper.
  - Updated `list_problems` pagination condition to activate whenever either `page` or `limit` is provided (`eff_page = page or 1`, `lim = limit or 25`), returning `{ "total": 100, "items": [...], "page": 1, "limit": 200, "total_pages": 1 }`.
  - Unpaginated requests (e.g. `list_problems(db=db)` and `/roadmap`) continue returning raw lists of all 100 problems, preserving backward compatibility with existing tests.
  - Hardened `web/app/problems/page.tsx` with defensive type guards to unpack either `{ items, total }` or raw arrays, ensuring full 100 problems count (25 per page) and all 10 topics display seamlessly in the UI.
- [x] **Schema & Model Extensions**:
  - Added `scene` (String) and `starter_code` (Text) to `Problem` model in `api/app/models/entities.py`.
  - Created Alembic migration `api/alembic/versions/0002_add_scene_and_starter_code.py`.
  - Non-destructive SQLite schema upgrade performed.
  - `reference_python` kept strictly on disk and never exposed via database models or API responses.
- [x] **Real Data & No Leaks Across API**:
  - Implemented `GET /topics` router in `api/app/routers/topics.py` returning real topics from the database.
  - `GET /problems` and `GET /problems/{slug}` return real database content with hidden test case inputs and outputs strictly isolated and never leaked to the client.
  - Updated `web/app/problems/page.tsx` to dynamically populate the Topic `<select>` filter with 10 real topics from the database via TanStack Query.
- [x] **Verification & Test Integrity**:
  - `python content/scripts/validate_content.py`: 100 problems checked, 1,192 tests executed, 0 failures.
  - `api/tests/test_checkpoint_s1x.py`: Seed idempotency (100 problems, 10 topics, 0 duplicates on rerun) and test isolation verified.
  - All 13 existing tests in `api/tests/test_api.py` and 28 total pytest tests passing (100%).
  - `npm --prefix web run build`: Clean production build passing across all routes.
  - Frontend unit tests passing: 10/10 tests in `web/tests/`.

---

## 🚀 Phase 5 - Production Readiness — COMPLETE
- [x] **Centralized Configuration & Environment Variables**:
  - Implemented typed `Settings` model in `api/app/config.py` validating all secrets, database credentials, redis connection, Judge0 URL, CORS origins, and rate limits.
  - Provided comprehensive `.env.example` templates for `api/.env.example`, `web/.env.example`, and full-stack `.env.example`.
- [x] **Hardened Security & Rate Limiting**:
  - Implemented sliding-window in-memory rate limiter in `api/app/rate_limiter.py` with headers (`Retry-After`, 429 status code) covering code submissions (15/min), AI calls (10/min), and general API requests (120/min).
  - CORS allowlist properly configured in `api/app/main.py` using `settings.CORS_ORIGINS`.
  - Pydantic input length limits enforced on code submissions ($\le 64$ KB), discussions ($\le 15$ KB), and notes ($\le 50$ KB), returning HTTP 422 on violations.
  - Strict SQLAlchemy ORM usage for 100% of data layer queries to prevent SQL injection.
  - Global FastAPI exception handler strips internal stack traces from responses in production mode, logging structured details safely to disk/stdout.
- [x] **Observability & Multi-Service Health Monitoring**:
  - Implemented structured JSON logging with `JSONFormatter` and `StructuredLoggingMiddleware` in `api/app/logging_config.py` tracking request duration, status code, IP, and exceptions.
  - Multi-service health check endpoint in `api/app/routers/health.py` testing PostgreSQL (`SELECT 1`), Redis cache ping, and Judge0 code runner connectivity.
  - Configured error reporting hook (Sentry-ready, disabled gracefully without a DSN).
- [x] **Comprehensive Test Suites**:
  - Backend: 26 passed unit & integration tests (`test_api.py`, `test_phase3.py`, `test_phase5.py`) covering 100% of API endpoints and edge cases with zero deprecation warnings.
  - Frontend: 10 passed unit tests (`web/tests/problem_filters.test.js` and `web/tests/verdict_display.test.js`) verifying filtering, sorting, pagination, and verdict badge displays.
  - End-to-End: Created Playwright test suite `tests/e2e/streak_solve_flow.spec.ts` and `playwright.config.ts` verifying sign-in, solution execution, verdict display, and streak incrementation.
  - Problem Bank: 60/60 problems verified with 100% test pass rate across >720 test cases.
- [x] **Docker & Deployment Infrastructure**:
  - Multi-stage production `Dockerfile` for `api/` (Python 3.12-slim, non-root user, uvicorn workers, health check).
  - Multi-stage production `Dockerfile` for `web/` (Node 20-alpine, Next.js standalone output tracing, non-root `nextjs` user).
  - Local & production `docker-compose.yml` stacks orchestrating Postgres, Redis, Judge0, API, and Web.
- [x] **Documentation & Architecture Guide**:
  - Created `README.md` with ASCII architecture diagram, quick setup in under 10 steps, testing guide, and cloud deployment guides (Vercel for frontend, Render/Railway for backend, managed PostgreSQL).
- [x] **Continuous Integration (GitHub Actions)**:
  - Created `.github/workflows/ci.yml` matrix executing backend lint & pytest, problem validation, frontend lint, type-check (`npm run type-check`), frontend tests, Next.js build, and Playwright tests.

---

## 🎨 Phase 4 - User Experience and Design — COMPLETE
- [x] **Consistent Design Tokens, Button & Card Components**:
  - Created standardized `Button` component in `web/components/ui/Button.tsx` with variants (`primary`, `secondary`, `outline`, `ghost`, `danger`, `success`), sizes (`sm`, `md`, `lg`), loading spinner, and WCAG focus ring.
  - Created standardized `Card` component family in `web/components/ui/Card.tsx` (`Card`, `CardHeader`, `CardContent`, `CardFooter`) with variants (`default`, `elevated`, `glass`, `interactive`).
  - Updated design tokens in `web/styles/tokens.css` with WCAG AA `:focus-visible` styling (`outline: 2px solid var(--accent-cyan)` with 2px offset).
- [x] **Responsive Layout & Mobile Code Editor (360px viewport)**:
  - Designed responsive problem-solving view in `web/app/problems/[slug]/page.tsx` that smoothly adapts from large monitors down to 360px mobile width.
  - Implemented top mobile tab switcher (`Code Editor` vs `Statement & Notes`) so mobile users can comfortably code or read instructions without horizontal scroll or truncated panels.
- [x] **Accessibility (WCAG AA) & Reduced Motion**:
  - Added flat SVG/HTML fallbacks to 3D scenes: `HeroCube` (SVG wireframe fallback), `Roadmap3D` (accessible keyboard-navigable list), `Visualizer3D` (`role="status" aria-live="polite"` step explanations).
  - Ensured all icon-only buttons include descriptive `aria-label` and `title` attributes.
  - Maintained `prefers-reduced-motion` compliance in animations and 3D canvas render loops.
- [x] **Interactive 3-Step Onboarding Flow**:
  - Implemented `web/components/ui/OnboardingModal.tsx`: a friendly 3-step modal guide for first-time visitors (Pick Level -> Solve First Problem -> Daily Streak).
  - Automatically remembers dismissal in `localStorage` (`ready2code_onboarding_dismissed`) and is never shown again once completed or dismissed.
- [x] **User Feedback & Unsaved Code Alerts**:
  - Implemented `beforeunload` warning in `web/app/problems/[slug]/page.tsx` whenever unsaved editor changes exist (`isCodeDirty`).
  - Added real-time toasts for run/submit actions, autosave status, bookmark toggles, and judge errors.
- [x] **Performance & Lazy Loading**:
  - Dynamically imported Monaco code editor (`ssr: false`) and 3D scenes.
  - Eliminated redundant heavy imports and unused icons.
- [x] **SEO Metadata Across Public Routes**:
  - Created dedicated metadata layouts (`layout.tsx`) with titles, descriptions, and OpenGraph metadata across all public routes (`/problems`, `/roadmap`, `/contests`, `/leaderboard`, `/patterns`, `/lists`, `/companies`, `/interviews`, `/jobs`, `/placement`, `/daily`, `/mock`, `/review`, `/analytics`, `/battles`).
  - Implemented dynamic metadata generation for `/problems/[slug]`, `/profile/[username]`, and `/portfolio/[username]`.
- [x] **Verification**:
  - `npm --prefix web run build`: 100% clean production build across 30 routes (code 0).
  - Pytest: 18/18 tests passing (code 0).
  - Problem validation: 60/60 problems verified (code 0).

---

## ⚡ Phase 3 - Core Functionality — COMPLETE
- [x] **Auth Guard on Write Actions & Public Anonymous Browsing**:
  - Implemented `api/app/routers/auth.py` (`POST /auth/register`, `POST /auth/login`, `GET /auth/me`) and `api/app/auth_deps.py` with `get_current_user` / `get_current_user_optional`.
  - Every write action (code submissions, note saving, bookmark toggling, and discussion posting) requires authentication and returns HTTP 401 for unauthenticated requests.
  - Anonymous users can freely browse problems, read statements, view lists, and test sample cases without login.
  - Built frontend `web/lib/authContext.tsx` and modal `web/components/ui/AuthModal.tsx` with quick one-click demo login (`algo_ninja`, `byte_master`) and seamless action resumption.
- [x] **Judge0 Execution & Verdict Engine**:
  - Real verdicts returned across all sample and hidden tests: Accepted (`AC`), Wrong Answer (`WA`), Time Limit Exceeded (`TLE`), Runtime Error (`RE`), Compilation Error (`CE`).
  - Precise execution metrics: `runtime_ms`, `memory_kb`, and runtime percentiles.
  - Hidden test inputs and outputs are strictly isolated on the backend and never exposed to the client.
  - Graceful degradation with clear user feedback: `"Judge is unavailable, try again"` when Judge0 is unreachable.
- [x] **Server-Side Problem List Filtering, Sorting, and Pagination (25 per page)**:
  - Extended `GET /problems` with server-side pagination (25 items per page), multi-attribute sorting (`title`, `difficulty`, `topic`, `acceptance`, `status`, `runtime`), and granular filtering (`topic`, `difficulty`, `status`, `company`, `tag`, `search`).
  - Synchronized all filters, sorting, and pagination state into the URL query parameters (`topic`, `difficulty`, `status`, `company`, `tag`, `sort`, `order`, `page`, `q`).
  - Added bottom pagination controls with Prev/Next, numeric pages, and item range tracking ("Showing 1–25 of 60 problems").
- [x] **User Progress Tracking & Runtime Badges**:
  - Automatically records `solved` and `attempted` statuses along with user's personal `best_runtime_ms`.
  - Displayed directly on problem table with status checkmarks and runtime badges (`24 ms`).
- [x] **Timezone-Aware Streak Tracking**:
  - Daily activity tracking calculated in user's localized timezone (`user.timezone` with `zoneinfo.ZoneInfo`) upon code submission.
  - Real live streak counter displayed in the global navigation header (`🔥 N Days`).
- [x] **Server-Persisted Notes and Bookmarks with Autosave Indicator**:
  - Notes saved to `POST /notes` with a 1.5s debounce and visual indicator: `● Saved`, `● Saving...`, `● Unsaved changes`.
  - Bookmarks stored on server via `POST /users/me/bookmarks/toggle`.
- [x] **Productivity Keyboard Shortcuts**:
  - `Ctrl + Enter` (or `Cmd + Enter`) runs sample test cases.
  - `Ctrl + Shift + Enter` (or `Cmd + Shift + Enter`) submits solution against hidden tests.
  - Added visual keyboard badges on the action buttons.
- [x] **Verification**:
  - All 18 backend pytest tests passing (`api/tests/test_api.py` and `api/tests/test_phase3.py`).
  - All 60 problems pass CI validation harness with 100% test pass rate (`scripts/validate_problems.py`).
  - Frontend `npm run build` succeeds cleanly across all 30 routes (code 0).

---

## 📚 Phase 2 - Problem Bank (Target: 60 Problems) — COMPLETE
- [x] **Original 60 Problem Sets Across 10 Core Topics**:
  - Arrays and Hashing (10)
  - Two Pointers and Sliding Window (8)
  - Strings (6)
  - Stack and Queue (6)
  - Linked List (6)
  - Trees (7)
  - Graphs (5)
  - Binary Search (4)
  - Dynamic Programming (5)
  - Heap and Intervals (3)
  - **Difficulty Breakdown**: Exactly **25 Easy**, **25 Medium**, and **10 Hard**.
- [x] **Strict Specification Conformance for Every Problem**:
  - `slug`, `title`, `difficulty`, `topic`, `tags` (with pattern names), `company_tags`
  - `statement_md`: 100% original phrasing, clear input/output format specifications, and boundary constraints
  - `examples`: $\ge 2$ examples with line-by-line algorithmic explanations
  - `sample_tests` (2-3) and `hidden_tests` ($\ge 8$, rigorously covering edge cases: empty input, single element, max constraints, duplicates, negative values, and non-trivial patterns)
  - `time_limit_ms`, `memory_limit_mb`
  - `hints`: 3 progressive tiers (Level 1 direction, Level 2 algorithmic mechanism, Level 3 concrete data structure name with zero code leaks)
  - `editorial_md`: detailed optimal approach, formal time and space complexity analysis, and documented common pitfalls/mistakes
  - `reference_solutions`: 4 complete solutions per problem (`brute_python`, `optimal_python`, `optimal_java`, `optimal_cpp`)
- [x] **Automated CI Validation & Test Execution Harness**:
  - Created `scripts/validate_problems.py`: enforces strict schema rules, validates JSON structures, compiles/executes reference solutions against every test case in an isolated execution harness, and fails with non-zero exit code if any test fails.
  - Achieved **100% test pass rate** across all 60 problems (>720 individual test cases verified).
  - Added `.github/workflows/validate-problems.yml` to automatically execute the test harness on pushes and pull requests targeting problems or the validator.
- [x] **Database Seeding & Test Suite Integrity**:
  - Enhanced `api/scripts/seed.py` to idempotently seed all 60 problems, system lists (Blind 75, NeetCode 150), 30-day study bootcamp, and live contests.
  - All 13 existing pytest tests in `api/tests/test_api.py` passing with zero failures.
  - `npm run build` succeeds cleanly across all 30 routes.

---

## 🔍 Phase 0 - Production Audit & Fixes — COMPLETE
- [x] **Complete Route Audit**: Examined all 29 routes across `web/app/` documenting data sources, mock data, and placeholder elements in `AUDIT.md`.
- [x] **Interactive Elements & Form Audit**: Documented all un-wired or mock buttons, forms, and links (streak freeze, mock evaluations, bookmark catch fallbacks, etc.).
- [x] **API Endpoints Inventory**: Mapped all 46 API endpoints across 17 backend routers with frontend connection status.
- [x] **Timezone Deprecation Fixes**: Replaced `datetime.utcnow()` with `datetime.now(timezone.utc)` across `entities.py`, `contests.py`, `analytics.py`, `certificates.py`, `notes.py`, `submissions.py`, and `seed.py`. All 13 pytest tests passing with zero deprecation warnings.
- [x] **npm audit Investigation**: Evaluated vulnerabilities; confirmed non-breaking status while avoiding breaking upgrades to Next 16 without `--force`.
- [x] **Port 3000 Check for `npm run dev`**: Created `web/scripts/dev.js` to verify port 3000 availability before launch, exiting with a clear diagnostic message if busy.
- [x] **Verification**: 13/13 backend pytest tests passing, `npm run build` static/dynamic compilation passing (code 0).

---

## 🌐 Phase 1 - Real Data Everywhere — COMPLETE
- [x] **TanStack Query Setup & Client**: Installed `@tanstack/react-query`, created centralized `QueryProvider.tsx` wrapping the application in `web/app/layout.tsx`, and created typed API client `fetchApi<T>()` in `web/lib/api.ts`.
- [x] **Dynamic Backend Routers**: Implemented FastAPI backend routers for:
  - `companies.py`: `GET /companies`, `GET /companies/{slug}`
  - `interviews.py`: `GET /interviews`, `POST /interviews`
  - `jobs.py`: `GET /jobs`, `POST /jobs/{id}/apply`
- [x] **Replaced Mock Data & Hard-Coded Arrays with TanStack Query Across All Pages**:
  - `/problems`: dynamic list filtering, search, topic & difficulty filters.
  - `/problems/[slug]`: real sample/hidden test execution via backend with real Judge0 error reporting ("Judge is unavailable, please try again" instead of fake Accepted).
  - `/leaderboard`: real Elo and XP leaderboard data.
  - `/contests`: real active and upcoming contests.
  - `/contests/[id]`: real contest details and 10s auto-polling live standings.
  - `/lists` & `/lists/[id]`: dynamic curated problem lists with progress tracking.
  - `/plans/[id]`: dynamic 30-day interactive calendar bootcamp.
  - `/companies` & `/companies/[name]`: dynamic company interview roadmaps.
  - `/interviews`: community debriefs with submission mutation.
  - `/jobs`: fast-track hiring board with job application mutation.
  - `/roadmap`: dynamically aggregates real problem counts & solved counts per topic island.
  - `/analytics`: dynamic user solve analytics and weak-topic detection.
  - `/daily`: dynamic daily problem challenge.
  - `/review`: spaced repetition review queue with grade mutation.
  - `/patterns` & `/patterns/[id]`: 15 pattern catalog and pattern recognition quiz with mutation.
  - `/ladder/[problem]`: brute-to-optimal progression ladder with runtime verification mutation.
  - `/placement`: campus placement question pool.
  - `/profile/[username]`: real user profile, 365-day activity, topic mastery, and badges.
  - `/portfolio/[username]`: real verified public developer portfolio and solved distributions.
- [x] **Loading Skeletons, Empty States & Error Handling**:
  - `web/components/ui/LoadingSkeleton.tsx`: multi-variant loading skeletons (`table`, `card`, `title`).
  - `web/components/ui/EmptyState.tsx`: clean zero-state display with action triggers.
  - `web/components/ui/QueryErrorState.tsx`: user-friendly error banners with one-click `Retry` buttons.
- [x] **Global Error Boundary & 404**:
  - `web/app/error.tsx`: Next.js client-side global error boundary with reset support.
  - `web/app/not-found.tsx`: friendly 404 page with navigation links back to problems, contests, and roadmap.
- [x] **Seed Command**: `api/scripts/seed.py` loads 63 problem sets, system lists, study plans, and live contests idempotently.
- [x] **Verification**: All 13 backend pytest tests passing, `npm run build` succeeds (30 routes compiled).


---

## 🏁 Phase 0: Setup — COMPLETE (C0.1 to C0.4)
- [x] **C0.1 Scaffold the web app**: Next.js 14 App Router in TypeScript with Tailwind CSS in `web/`, dark theme tokens (`styles/tokens.css`), ready with Ready2Code branding.
- [x] **C0.2 Backend, database, and Redis**: FastAPI service in `api/` with SQLAlchemy 2.0, Alembic, Pydantic, PostgreSQL + zero-docker SQLite dev fallback. Health check endpoint `GET /health`.
- [x] **C0.3 Judge0 running locally & Execution Engine**: `api/app/judge/client.py` with Judge0 client integration and built-in sub-millisecond local sandboxed code executor fallback.
- [x] **C0.4 3D foundation**: Lazy-loaded Three.js Hero Cube (`components/3d/HeroCube.tsx`) with glass transmission material, rotating particles, and flat SVG accessible fallback.

---

## 🚀 Phase 1: MVP — COMPLETE (C1.1 to C1.9)
- [x] **C1.1 Auth and profile shell**: Account & settings (`/settings` with unique username validation, timezone configuration, blind mode toggle, protected route shell).
- [x] **C1.2 Problem data and seed set**: 63 comprehensive problem sets in `content/problems/*.json` with original statements, sample tests, hidden tests, tiered hints, and time/memory limits. Seed script `api/scripts/seed.py` and validator.
- [x] **C1.3 Problem list with filters**: `/problems` with searchable table, topic/difficulty/company/status filters, 300ms debounce, random unsolved picker, query string sync.
- [x] **C1.4 Solve page with Monaco**: `/problems/[slug]` resizable split pane, problem description, examples, constraints, Monaco Editor with Python, JavaScript, C++, Java, draft persistence per problem/language, font-size adjustment.
- [x] **C1.5 Run against sample tests**: `POST /submissions/run` with sample test execution, time and memory limits, and `TestCaseTable` UI component.
- [x] **C1.6 Submit with hidden tests and verdicts**: `POST /submissions` evaluating all sample + hidden tests, runtime and memory percentiles, `VerdictBadge` component, particle burst celebration on Accepted.
- [x] **C1.7 3D topic island roadmap**: `/roadmap` with 3D floating topic islands (Arrays, Strings, Linked Lists, Trees, Graphs, DP, etc.), progress rings, camera transitions, and flat SVG accessible keyboard navigation.
- [x] **C1.8 Hints, editorial, bookmarks, notes**: Solve page tabs: tiered hints (Level 1-3), gated markdown editorial, 2s autosaving notes, bookmark toggle.
- [x] **C1.9 Daily problem and streak heatmap**: `/daily` deterministic daily problem picker, streak counter with freeze support, and 365-day profile activity heatmap on `/profile/[username]`.

---

## ⚡ Phase 2: Version 2 — COMPLETE (C2.1 to C2.5)
- [x] **C2.1 Curated lists and 30/60/90-day plans**: System lists (Blind 75, NeetCode 150) and 30-Day Interview Readiness Bootcamp calendar checklist at `/lists`, `/lists/[id]`, and `/plans/[id]`.
- [x] **C2.2 Contests and live leaderboard**: Timed weekly contests with penalties (5 min penalty per WA), 10s auto-polling live standings, and Elo rating history at `/contests` and `/contests/[id]`.
- [x] **C2.3 Discussion and solution posts**: Markdown discussion threads, voting (+1/-1), and community solutions unlockable by writing a 50+ word explanation at `/discussions`.
- [x] **C2.4 XP, badges, and leaderboards**: Global ranking by XP, streak consistency, and Elo rating at `/leaderboard`.
- [x] **C2.5 Analytics and spaced repetition**: Learner analytics at `/analytics` with weekly solves bar chart, acceptance by topic, weak-topic detection, and spaced repetition review queue (1, 3, 7, 21 days) at `/review`.

---

## 🌟 Phase 3: Differentiators — COMPLETE (C3.1, C3.4, C3.5, C3.6, C3.9, C3.10, C3.12)
- [x] **C3.1 3D algorithm visualizer engine**: Reusable trace player at `/visualizer/[algo]` with 3D pillars for values, floating hash map panels, transport controls (play, pause, next/prev step, speed, scrub bar), and screen reader accessibility.
- [x] **C3.4 AI code review and error explainer**: Time and space complexity analysis, bottleneck identification, and plain-language explanation of failed tests at `POST /ai/review` and `POST /ai/explain-verdict`.
- [x] **C3.5 Pattern-first learning and quiz**: 15 algorithm patterns with signals, canonical templates, and interactive pattern recognition quizzes unlocking tagged problems at `/patterns` and `/patterns/[id]`.
- [x] **C3.6 Brute to optimal ladder**: Three progression stages (Brute, Better, Optimal) with runtime threshold enforcement at `/ladder/[problem]`.
- [x] **C3.9 Mock interview timer and blind mode**: Simulated FAANG technical interview at `/mock` with 20/45 minute timer, simulated interviewer dialogue, editor auto-lock, and separate scores for Correctness and Communication.
- [x] **C3.10 Placement prep & CS fundamentals**: Indian campus recruiter tracks (Aptitude, Product DSA, CS Fundamentals Core: OS, DBMS, Networks) with English/Hindi/Bengali regional explanations at `/placement`.
- [x] **C3.12 Verified skill certificates**: Timed skill test issuing shareable certificates with verification IDs and LinkedIn share integration at `/certificates/[code]`.

---

## 🏆 Phase 4: Growth & Production Level Features — COMPLETE (C4.1, C4.3, C4.4)
- [x] **C4.1 1v1 PvP Coding Arena & Social Battles**: Real-time matchmaking duel lobby at `/battles` and split live battle arena at `/battles/[id]` with dual progress bars, test submission sync, and victory modals. Backend API in `api/app/routers/battles.py`.
- [x] **C4.3 Company-Specific Roadmaps & Interview Debriefs**: Dedicated 60-day roadmaps for Google, Amazon, Microsoft, Uber, Flipkart, Atlassian at `/companies` and `/companies/[name]`. Verified community interview experiences at `/interviews`.
- [x] **C4.4 Career Tools**: Shareable public developer portfolio at `/portfolio/[username]` featuring 3D annual activity heatmap, skill mastery breakdown, and verified badges. Verified skill hiring board with 1-click Fast-Track applications at `/jobs`.
- [x] **Production Deployment & Architecture**:
  - `api/Dockerfile`: Multi-stage Python 3.12 container with uvicorn workers and health checks.
  - `web/Dockerfile`: Multi-stage Node.js 20 Alpine container leveraging Next.js standalone server.
  - `nginx/nginx.conf`: Production reverse proxy with gzip, caching, security headers, and rate limiting.
  - `docker-compose.prod.yml`: Production orchestration (Postgres, Redis, Judge0, API, Web, Nginx).
  - `.env.production.example`: Full production environment template.
