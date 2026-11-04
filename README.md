# Ready2Code ⚡

> **A production-ready, interactive 3D Data Structures & Algorithms (DSA) practice arena and interview preparation platform.**

Built with **Next.js 14 (App Router, TypeScript, Tailwind CSS, Monaco Editor, Three.js)** and **FastAPI (SQLAlchemy, Alembic, PostgreSQL, Redis, Judge0)**.

---

## 🏛️ Architecture Overview

```text
                           ┌────────────────────────┐
                           │      Web Browser       │
                           │  (Desktop & Mobile 360)│
                           └───────────┬────────────┘
                                       │
                      HTTPS / Port 443 │
                                       ▼
                     ┌──────────────────────────────────┐
                     │          Nginx Reverse Proxy     │
                     └───────┬──────────────────┬───────┘
                             │                  │
                /api/* & WS  │                  │  Static & SSR (HTML/JS)
                             ▼                  ▼
             ┌────────────────────────┐    ┌────────────────────────┐
             │    FastAPI Backend     │    │   Next.js 14 Frontend  │
             │     (Uvicorn ASGI)     │    │   (Node 20 Standalone) │
             │  • Structured JSON Log │    │  • Monaco Code Editor  │
             │  • Sliding-Window Rate │    │  • 3D Algorithm Canvas │
             │  • Auth & User Streaks │    │  • TanStack React Query│
             └───────────┬────────────┘    └────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────────┐ ┌─────────┐ ┌─────────────────────────┐
│ PostgreSQL 16   │ │ Redis 7 │ │   Judge0 CE Engine      │
│ (Primary Store) │ │ (Cache) │ │ (Isolated Code Sandbox) │
│ • 60 Problems   │ └─────────┘ │ • Multi-language Worker │
│ • Tests & Users │             │ • Real Memory & Runtime │
└─────────────────┘             └─────────────────────────┘
```

---

## 🚀 Quick Setup (Under 10 Steps)

### Option A: Complete Docker Compose Stack (Recommended)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Ready2Code.git
   cd Ready2Code
   ```

2. **Configure environment files**:
   ```bash
   cp .env.example .env
   cp api/.env.example api/.env
   cp web/.env.example web/.env.local
   ```

3. **Start all services with Docker Compose**:
   ```bash
   docker compose up -d --build
   ```

4. **Seed the database with all 60 curated problems**:
   ```bash
   docker compose exec api python scripts/seed.py
   ```

5. **Open the web application**:
   - Web Application: [http://localhost:3000](http://localhost:3000)
   - FastAPI Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Multi-Service Health: [http://localhost:8000/health](http://localhost:8000/health)

---

### Option B: Bare-Metal Local Development

1. **Clone and enter repository**:
   ```bash
   git clone https://github.com/your-username/Ready2Code.git && cd Ready2Code
   ```

2. **Setup Python virtual environment for backend**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r api/requirements.txt
   ```

3. **Seed database with 60 problems & mock users**:
   ```bash
   python api/scripts/seed.py
   ```

4. **Start the FastAPI backend server**:
   ```bash
   python -m uvicorn app.main:app --app-dir api --port 8000 --reload
   ```

5. **Install frontend dependencies**:
   ```bash
   npm --prefix web install
   ```

6. **Start the Next.js development server**:
   ```bash
   npm --prefix web run dev
   ```

7. **Verify multi-service health**:
   Navigate to [http://localhost:8000/health](http://localhost:8000/health).

---

## 🧪 Testing & Quality Assurance

Run the comprehensive test suites across the stack:

```bash
# 1. Run all backend API unit & integration tests (26 passing tests)
python -m pytest api/tests/

# 2. Validate all 60 problem JSON schemas, sample & hidden tests
python scripts/validate_problems.py

# 3. Run frontend unit tests (problem filters & verdict display)
npm --prefix web test

# 4. Run production frontend type-check & build
npm --prefix web run build

# 5. Run end-to-end Playwright tests
npx playwright test
```

---

## 🚢 Production Deployment Guide

Ready2Code is designed for cloud-native deployment with decoupled frontend and backend layers:

### 1. Frontend: Vercel
1. Connect your GitHub repository to [Vercel](https://vercel.com).
2. Set root directory to `web`.
3. Configure Environment Variables:
   - `NEXT_PUBLIC_API_URL`: `https://api.yourdomain.com`
   - `API_INTERNAL_URL`: `https://api.yourdomain.com/:path*`
4. Deploy. Vercel automatically deploys the Next.js 14 App Router application with global edge caching.

### 2. Backend: Render / Railway
1. Create a new Web Service pointing to `api/Dockerfile`.
2. Configure Environment Variables:
   - `ENVIRONMENT`: `production`
   - `DATABASE_URL`: `postgresql://user:pass@host:5432/ready2code_prod`
   - `REDIS_URL`: `redis://default:pass@redis-host:6379/0`
   - `JUDGE0_URL`: `https://judge0.yourdomain.com`
   - `JWT_SECRET`: Generate a 64-character secret using `openssl rand -hex 32`
   - `CORS_ORIGINS`: `https://yourdomain.com,https://your-vercel-app.vercel.app`
3. Expose port `8000`.

### 3. Managed Database: Neon / Supabase / AWS RDS
1. Provision a PostgreSQL 15+ database instance.
2. Run database migrations:
   ```bash
   alembic upgrade head
   python api/scripts/seed.py
   ```

### 4. Code Execution Engine: Judge0 CE
1. Self-host Judge0 on a separate VM using `docker-compose.prod.yml` with Redis and Postgres.
2. Or connect to a managed Judge0 API instance.

---

## 🔒 Security & Performance Features

- **Strict ORM Access**: 100% of queries use SQLAlchemy ORM parameterization to eliminate SQL injection.
- **Sliding-Window Rate Limiting**: Built-in rate limiting for code submissions (15/min) and AI calls (10/min).
- **CORS Allowlist**: Configurable CORS origin restriction in production.
- **Zero Stack Traces in Production**: Unhandled exceptions return generic messages while logging structured details internally.
- **Input Length Restrictions**: Pydantic models strictly cap code (64 KB) and text submissions.
- **Hidden Test Case Masking**: Hidden inputs and outputs are never returned to the client browser.
