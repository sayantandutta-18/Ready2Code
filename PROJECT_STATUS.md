# Ready2Code — Project Status & Roadmap

Platform: **Ready2Code** (Interactive 3D DSA Arena)
Current Phase: **Phase 3 (Core Functionality) COMPLETED**
Updated: November 2026

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
