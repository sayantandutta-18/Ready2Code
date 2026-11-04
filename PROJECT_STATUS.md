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

## 🌟 Advanced Differentiators Included
- [x] **C3.1 3D Algorithm Visualizer Engine**: Reusable trace player in `/visualizer/[algo]` rendering arrays as 3D pillars, floating hash map panels, transport controls (play, pause, step forward/back, speed 0.5x/1x/2x, scrub bar), and screen reader accessibility.
- [x] **C3.3 Socratic AI Hint Bot**: Tiered hints (Level 1 conceptual, Level 2 pattern, Level 3 data structure) with XP costs.
- [x] **C3.4 AI Code Review**: Complexity analysis and bottleneck detector at `POST /ai/review`.
- [x] **C3.9 Blind Mode**: Toggle to hide problem difficulty and tags to simulate real interview pressure.

---

## 🔮 Next Checkpoints Planned
- **Phase 2: Version 2**: Curated lists (Blind 75, NeetCode 150), 30/60/90-day study plans (C2.1), Timed contests & live standings (C2.2), Community discussion forum (C2.3), Spaced repetition review queue (C2.5).
