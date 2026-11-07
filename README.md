<div align="center">

# ⚡ Ready2Code

### Learn data structures & algorithms in 3D. Practice like it's a real interview.

[![Vercel Deployment](https://img.shields.io/badge/Vercel-Live_App-black?logo=vercel&logoColor=white)](https://ready2code.vercel.app)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Judge0](https://img.shields.io/badge/Judge0-CE-orange)](https://judge0.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[**🌐 Live Application**](https://ready2code.vercel.app) · [**🔑 Sign In**](https://ready2code.vercel.app/login) · [**✨ Create Account**](https://ready2code.vercel.app/register) · [**📚 Documentation**](docs/INDEX.md) · [**🐛 Report a Bug**](https://github.com/sayantandutta-18/Ready2Code/issues)

</div>

---

## 🌟 Live Demo & Quick Links

| Destination | Link | Description |
|---|---|---|
| 🚀 **Production Web App** | [ready2code.vercel.app](https://ready2code.vercel.app) | Live deployed Next.js 14 frontend on Vercel Edge Network |
| 🔑 **Sign In** | [ready2code.vercel.app/login](https://ready2code.vercel.app/login) | Full credential & 1-click demo profile login |
| ✨ **Register** | [ready2code.vercel.app/register](https://ready2code.vercel.app/register) | Account creation with experience level onboarding |
| 🧩 **Problems Explorer** | [ready2code.vercel.app/problems](https://ready2code.vercel.app/problems) | 100+ curated problems across 10 algorithmic topics |
| 🗺️ **3D Topic Roadmap** | [ready2code.vercel.app/roadmap](https://ready2code.vercel.app/roadmap) | Interactive Three.js spatial topic progression |
| ⚔️ **1v1 Battles** | [ready2code.vercel.app/battles](https://ready2code.vercel.app/battles) | Real-time competitive algorithmic code duels |
| 🏆 **Leaderboard** | [ready2code.vercel.app/leaderboard](https://ready2code.vercel.app/leaderboard) | Global XP and daily streak rankings |

---

## 💡 Why Ready2Code?

Most DSA platforms present you with a problem and a blank code box. Ready2Code is designed around how humans naturally build mental models:

- **Spatial 3D Mental Models:** Algorithms play out in Three.js — arrays manifest as 3D pillars, graphs glow as spatial topologies, and DP tables populate cell by cell. Scrub forward and backward synchronously with your code execution.
- **Pattern-First Learning:** Sliding window, two pointers, monotonic stack, divide-and-conquer, topological sort, and trie structures with concept checks before coding.
- **Sandboxed Multi-Language Judge:** Powered by Judge0 with verdicts (`Accepted`, `Wrong Answer`, `Time Limit Exceeded`, `Runtime Error`, `Compile Error`), execution runtime, and memory stats. Hidden test cases never leave the server.
- **Habit-Building Gamification:** Daily problems, streak maintenance, streak freeze protections, and personal progress heatmaps.
- **Placement & Interview Ready:** Tailored company tracks (Google, Microsoft, Amazon, Meta) and mock interview simulations.

---

## ✨ Core Features

| Category | Feature | Details |
|---|---|---|
| 🔐 **Authentication** | **Dedicated Sign In & Register** | Form validation, password masking, remember-me support, 1-click demo accounts (`algo_ninja`, `byte_master`), and token persistence. |
| 🧩 **Problem Bank** | **100+ Verified Problems** | Curated across 10 DSA categories with 1,192 verified test cases and complete reference solutions. |
| 🖥️ **Monaco Editor** | **VS Code in Browser** | Syntax highlighting, autocompletion, separate drafts per language (Python, C++, Java, JS), and keyboard shortcuts (`Ctrl+Enter` / `Ctrl+Shift+Enter`). |
| ⚖️ **Execution Sandbox** | **Judge0 Engine** | Isolated sandbox evaluation measuring millisecond runtime and memory usage against sample and secret tests. |
| 🎬 **3D Visualizer** | **Spatial Three.js Engine** | Interactive step-by-step 3D playback with camera controls, pause/step/scrub, and low-power 2D fallback. |
| 💡 **Socratic AI** | **Adaptive Hint System** | 3 progressive hint tiers nudging conceptual understanding without spoiling code. |
| 📈 **Streaks & XP** | **Daily Challenge & Leaderboard** | Streak freezes, milestone badges, daily streak counters in header, and global XP leaderboards. |
| 🏢 **Company Tracks** | **Targeted Placement Prep** | Curated problem sets tagged by FAANG company frequency and acceptance rate. |

---

## 🏛️ System Architecture

```text
                    ┌─────────────────────────┐
                    │       Web Client        │
                    │   Next.js 14 App Router │
                    │ (Desktop & Mobile PWA)  │
                    └────────────┬────────────┘
                                 │ HTTPS / WSS
                                 ▼
                    ┌─────────────────────────┐
                    │      Vercel / Nginx     │
                    │      Reverse Proxy      │
                    └─────┬─────────────┬─────┘
               /api/*, WS │             │ pages, SSR, assets
                          ▼             ▼
           ┌─────────────────────┐   ┌─────────────────────────┐
           │   FastAPI Backend   │   │  Vercel Edge Network    │
           │  (Uvicorn ASGI App) │   │  • 32 Pre-rendered /    │
           │  • Auth & Tokens    │   │    Dynamic Route Chunks │
           │  • Streaks & XP     │   │  • Three.js 3D Scenes   │
           │  • Rate Limiting    │   │  • Monaco Code Editor   │
           │  • Structured Logs  │   │  • React Query Cache    │
           └──────────┬──────────┘   └─────────────────────────┘
                      │
        ┌─────────────┼─────────────────────┐
        ▼             ▼                     ▼
 ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐
 │PostgreSQL 16 │ │   Redis 7    │ │      Judge0 CE       │
 │Problems,     │ │Leaderboards, │ │Isolated Code Sandbox │
 │Users, Drafts,│ │Sessions,     │ │Multi-language Runner │
 │Submissions   │ │Rate Limits   │ │Resource Limits       │
 └──────────────┘ └──────────────┘ └──────────────────────┘
```

**Technology Stack:**
- **Frontend:** Next.js 14 (App Router) · React 18 · TypeScript 5 · Tailwind CSS · Three.js / React Three Fiber · Monaco Editor · TanStack Query · Lucide Icons
- **Backend:** FastAPI · Python 3.11+ · SQLAlchemy 2.0 ORM · Alembic Migrations · Pydantic v2 · PyJWT · SlowAPI
- **Data & Sandbox:** PostgreSQL 16 · Redis 7 · Judge0 CE

---

## 🚀 Getting Started

### Local Development Setup

#### Prerequisites
- Node.js 18+ & npm
- Python 3.11+
- Git

#### Option 1: Automatic Launcher (Windows PowerShell)

```powershell
.\start-dev.ps1
```

This single command:
1. Validates Python and Node.js environments.
2. Creates virtual environment and installs dependencies.
3. Initializes the database and seeds the 100-problem bank.
4. Starts the FastAPI backend (`http://localhost:8000`) and Next.js frontend (`http://localhost:3000`) concurrently!

#### Option 2: Automatic Launcher (macOS / Linux)

```bash
chmod +x start-dev.sh
./start-dev.sh
```

#### Option 3: Manual Startup

```bash
# Backend setup
cd api
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
python ../scripts/seed_problems.py
uvicorn app.main:app --reload --port 8000

# Frontend setup (in a separate terminal)
cd web
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## 🧪 Testing & Verification

Ready2Code features comprehensive test suites across both backend and frontend layers:

```bash
# 1. Backend API & Router Tests (28 passed)
pytest api/tests/

# 2. Problem Bank Validation (100 problems, 1,192 tests passed)
python scripts/validate_problems.py

# 3. Content Integrity Check
python content/scripts/validate_content.py

# 4. Frontend Unit Tests (10 passed)
npm --prefix web test

# 5. Frontend TypeScript Verification
npm --prefix web run type-check

# 6. Frontend Production Build (32 routes compiled)
npm --prefix web run build
```

---

## 🚢 Production Deployment

### Frontend (Vercel)

The frontend is deployed live on Vercel at **[https://ready2code.vercel.app](https://ready2code.vercel.app)**.

Configuration files:
- [`vercel.json`](vercel.json): Root monorepo configuration with `framework: "nextjs"` and `npm --prefix web run build`.
- [`web/vercel.json`](web/vercel.json): Subdirectory configuration for root directory set to `web`.

To deploy your own fork to Vercel:
1. Import repository `sayantandutta-18/Ready2Code` in [Vercel](https://vercel.com/new).
2. Set **Root Directory** to `web`.
3. Add environment variable `NEXT_PUBLIC_API_URL` pointing to your deployed API.
4. Click **Deploy**.

### Backend (Railway / Render / Docker)

The backend includes a self-bootstrapping Docker production setup:

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Environment variables needed for the backend (`api/.env`):
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ready2code
REDIS_URL=redis://localhost:6379/0
JUDGE0_URL=http://localhost:2358
JWT_SECRET=your-secure-jwt-secret-key-at-least-32-chars
CORS_ORIGINS=["https://ready2code.vercel.app","http://localhost:3000"]
```

---

## 📁 Repository Structure

```text
Ready2Code/
├── api/                        # FastAPI Backend Application
│   ├── app/
│   │   ├── routers/            # auth, problems, submissions, daily, battles, ai
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic validation schemas
│   │   ├── core/               # database, config, security, rate limiting
│   │   └── main.py             # FastAPI entrypoint
│   ├── tests/                  # Pytest test suite (28 passing tests)
│   ├── alembic/                # Database migrations
│   └── Dockerfile              # Container definition
├── web/                        # Next.js 14 Frontend Application
│   ├── app/                    # 32 App Router routes (login, register, problems, visualizer, ...)
│   ├── components/
│   │   ├── 3d/                 # Three.js 3D spatial scenes (HeroCube, TopicIslands, Visualizer)
│   │   ├── editor/             # Monaco code editor integration
│   │   └── ui/                 # Navbar, TiltCard, DifficultyChip, Modals
│   ├── lib/                    # authContext, api client, types
│   ├── tests/                  # Node.js test runner unit test suite (10 passing tests)
│   └── public/                 # Static assets and icons
├── content/
│   └── problems/               # 100 Curated problems with reference code and test suites
├── docs/                       # Complete engineering documentation suite
│   ├── PRD.md                  # Product Requirements Document
│   ├── ARCHITECTURE.md         # Full architecture specification
│   ├── DESIGN.md               # Visual design tokens and UI components
│   ├── API.md                  # REST & WebSocket API specification
│   ├── AUTH.md                 # Authentication & authorization specs
│   └── TESTING.md              # Quality gates and test matrices
├── scripts/                    # Automation, seeders, and problem validators
├── vercel.json                 # Monorepo Vercel configuration
├── start-dev.ps1               # 1-click Windows PowerShell development launcher
├── start-dev.sh                # 1-click macOS / Linux development launcher
└── docker-compose.prod.yml     # Multi-container production stack
```

---

## 🔒 Security & Data Integrity

- **Strict Parameterized Queries:** 100% of queries use SQLAlchemy ORM with zero raw SQL concatenation.
- **Hidden Test Case Protection:** Hidden test inputs and outputs never reach the client; only execution verdicts, runtimes, and memory usages are returned.
- **Rate Limiting:** Sliding-window throttling on submission, AI, and authentication endpoints.
- **CORS Allowlist:** Strictly configured for trusted domains (`ready2code.vercel.app`).
- **CSR Protection & Suspense Boundaries:** Wrapped query parameters prevent hydration mismatch and CSR bailout.

---

## 📄 License

Ready2Code is released under the [MIT License](LICENSE).
