# Ready2Code — Project Status & Roadmap

Platform: **Ready2Code** (Interactive 3D DSA Arena)
Updated: November 2026

---

## 🏁 Phase 0: Setup — COMPLETE (C0.1 to C0.4)
- [x] **C0.1 Scaffold the web app**: Next.js App Router project in TypeScript with Tailwind CSS in `web/`, dark theme tokens (`styles/tokens.css`), ready with Ready2Code branding.
- [x] **C0.2 Backend, database, and Redis**: FastAPI service in `api/` with SQLAlchemy 2.0, Alembic, Pydantic, and dual database support (PostgreSQL + SQLite fallback for seamless zero-docker local dev). Health check endpoint `GET /health`.
- [x] **C0.3 Judge0 running locally & Execution Engine**: `api/app/judge/client.py` with Judge0 client integration and built-in safe sandboxed code executor fallback.
- [x] **C0.4 3D foundation**: Lazy-loaded Three.js Hero Cube (`components/3d/HeroCube.tsx`) with glass transmission material, rotating particles, and flat SVG accessible fallback.

---

## 🚀 Phase 1: MVP — COMPLETE (C1.1 to C1.9)
- [x] **C1.1 Auth and profile shell**: Account & settings (`/settings` with unique username validation, timezone configuration, blind mode toggle, protected route shell).
- [x] **C1.2 Problem data and seed set**: 12 verified starter problems in `content/problems/*.json` with original statements, sample tests, hidden tests, tiered hints, and time/memory limits. Seed script `api/scripts/seed.py` and validator.
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

## 🔮 Next Planned Phase: Phase 4 Growth
- **C4.1 Social practice**: Real-time study rooms with Yjs and 1v1 battles.
- **C4.2 Retention & rewards**: Mentor marketplace and avatar collection.
- **C4.3 Company roadmaps**: 60-day company-specific plans and interview experience wall.
- **C4.4 Career tools**: Verified skill portfolio and job referral board.
- **C4.5 Creators & classrooms**: Custom problem authoring with reference validation and teacher classroom mode.
