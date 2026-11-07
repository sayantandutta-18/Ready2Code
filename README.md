<div align="center">

# ⚡ Ready2Code

### Learn data structures & algorithms in 3D. Practice like it's a real interview.

[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Judge0](https://img.shields.io/badge/Judge0-CE-orange)](https://judge0.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[**Report a Bug**](https://github.com/sayantandutta-18/Ready2Code/issues) · [**Request a Feature**](https://github.com/sayantandutta-18/Ready2Code/issues)

</div>

---

## Why Ready2Code?

Most DSA platforms show you a problem and a blank editor. Ready2Code is built around how people actually learn:

- **See it, don't just read it.** Algorithms play out in 3D: arrays become pillars, graphs become glowing nodes, DP tables fill cell by cell. Scrub forward and back at your own pace.
- **Learn the patterns, not just the problems.** Sliding window, two pointers, monotonic stack, and more, with a quiz before each problem.
- **Get real judge verdicts.** Run against samples, submit against hidden tests, and get Accepted, Wrong Answer, TLE, Runtime Error, or Compile Error, with runtime and memory.
- **Build a daily habit.** A daily problem, streak tracking, and an activity heatmap keep you coming back.
- **Built for placement season.** Problem tracks and aptitude practice are designed with campus placements in mind.

---

## ✨ Features

| | Feature | What you get |
|---|---|---|
| 🧩 | **100-Problem Launch Bank** | Curated problems across 10 topics: arrays, strings, linked lists, trees, graphs, DP, binary search, heap, and more. Filter by topic, difficulty, status, and tag. |
| 🖥️ | **Monaco Code Editor** | The VS Code editor in your browser, with separate drafts per language and keyboard shortcuts (`Ctrl+Enter` runs samples, `Ctrl+Shift+Enter` submits). |
| ⚖️ | **Real Judging** | Sandboxed execution through Judge0 with verdicts, runtime, and memory. Hidden test data never reaches the browser. |
| 🎬 | **3D Algorithm Visualizer** | Step-by-step playback with play, pause, step, and scrub controls. Works with a flat fallback for low-power devices and reduced-motion settings. |
| 💡 | **Guided Hints** | Three hint levels that nudge you toward the idea without giving away the answer. |
| 📈 | **Progress Tracking** | Solved and attempted status, best runtimes, streaks, and a profile heatmap. |
| 📝 | **Notes & Bookmarks** | Autosaved notes per problem and a bookmarks list, synced to your account. |
| 🗺️ | **3D Topic Roadmap** | A learning path where each topic unlocks the next as you progress. |
| 📱 | **Mobile-Friendly** | Works down to 360px wide, with a tabbed layout on small screens. |
| 🎨 | **Accessible Design** | WCAG AA contrast, keyboard navigation, visible focus rings, and reduced-motion support. |

---

## 🏛️ Architecture

```text
                    ┌──────────────────────┐
                    │     Web Browser      │
                    │  (desktop & mobile)  │
                    └──────────┬───────────┘
                               │ HTTPS
                               ▼
                    ┌──────────────────────┐
                    │   Nginx / Reverse    │
                    │       Proxy          │
                    └────┬────────────┬────┘
              /api/*, WS │            │ pages, assets
                         ▼            ▼
          ┌──────────────────┐   ┌──────────────────┐
          │  FastAPI backend │   │ Next.js frontend │
          │  (Uvicorn, ASGI) │   │  (App Router)    │
          │  • auth, streaks │   │  • Monaco editor │
          │  • rate limits   │   │  • 3D scenes     │
          │  • JSON logging  │   │  • React Query   │
          └────────┬─────────┘   └──────────────────┘
                   │
     ┌─────────────┼──────────────────┐
     ▼             ▼                  ▼
┌──────────┐  ┌──────────┐   ┌────────────────────┐
│PostgreSQL│  │  Redis   │   │   Judge0 CE        │
│   16     │  │    7     │   │  isolated sandbox  │
│ problems,│  │ caching, │   │  multi-language,   │
│ users,   │  │ rankings │   │  time & memory     │
│ history  │  │          │   │  limits            │
└──────────┘  └──────────┘   └────────────────────┘
```

**Stack:** Next.js 14 · TypeScript · Tailwind CSS · Monaco · Three.js (React Three Fiber) · TanStack Query · FastAPI · SQLAlchemy 2.0 · Alembic · PostgreSQL 16 · Redis 7 · Judge0 CE

---

## 🚀 Quick Start

### Option A: One-Command Development Launcher (Windows PowerShell)

```powershell
.\start-dev.ps1
```
This automatically verifies environments, seeds the database with the 100-problem bank, and boots both the FastAPI backend and Next.js frontend!

### Option B: Docker Production Stack

```bash
# 1. Copy environment templates
cp .env.example .env
cp api/.env.example api/.env
cp web/.env.example web/.env.local

# 2. Start full production stack
docker compose -f docker-compose.prod.yml up -d --build
```

Then open:

| Service | URL |
|---|---|
| 🌐 Web app | http://localhost:3000 (or http://localhost through Nginx) |
| 📘 API docs | http://localhost:8000/docs |
| ❤️ Health check | http://localhost:8000/health |

---

## 🧪 Testing

```bash
# Backend API tests (28 passed tests)
python -m pytest api/tests/

# Validate problem files (100 problems, 1,192 tests)
python scripts/validate_problems.py
python content/scripts/validate_content.py

# Frontend unit tests (10 passed tests)
npm --prefix web test

# Frontend type-check
npm --prefix web run type-check

# Frontend production build
npm --prefix web run build

# End-to-end Playwright tests
npx playwright test
```

---

## 🚢 Deployment

Ready2Code separates the frontend and backend so each can scale independently.

| Layer | Recommended host | Notes |
|---|---|---|
| **Frontend** | [Vercel](https://vercel.com) | Set root directory to `web`, Node 20. |
| **API** | [Render](https://render.com) or [Railway](https://railway.app) | Deploy from `api/Dockerfile`, port 8000. |
| **Database** | [Neon](https://neon.tech) or [Supabase](https://supabase.com) | PostgreSQL 16+. Run migrations and seed. |
| **Cache** | [Upstash Redis](https://upstash.com) | Low-latency caching & leaderboards. |
| **Code execution** | Self-hosted Judge0 VM or managed Judge0 | Run isolated with no outbound network access. |

---

## 🔒 Security

- **Strict ORM parametrization:** 100% of queries use SQLAlchemy ORM.
- **Rate limiting:** Sliding-window limits on code submissions (15/min), AI endpoints (10/min), and general API requests (120/min).
- **CORS allowlist** enforced in production.
- **Zero leak of hidden test cases:** Hidden test inputs and outputs never touch the client.
- **Input validation:** Pydantic length and schema checks on code submissions and notes.
- **Production logging:** Stack traces stripped from public HTTP responses; structured JSON logs recorded.

---

## 📄 License

Released under the [MIT License](LICENSE).
