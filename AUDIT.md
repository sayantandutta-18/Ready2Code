# Ready2Code — Comprehensive Codebase Audit (Phase 0)

Date: November 2026  
Status: Phase 0 Completed

---

## 1. Route Audit (`web/app`)

Every route in `web/app`, its data consumption model, and audit notes:

| Route | File Path | Data Source Category | API Endpoint Called (if any) | Hard-coded / Mock Data Elements |
| :--- | :--- | :--- | :--- | :--- |
| `/` | `web/app/page.tsx` | Partial API | `GET /api/daily` | Stats counters (63+ problems, 15 patterns), quick topic tags, hero problem initial fallback state. |
| `/analytics` | `web/app/analytics/page.tsx` | Partial API | `GET /api/analytics` | Hardcoded initial fallback state (weekly solves, topic acceptance, weak topics). |
| `/battles` | `web/app/battles/page.tsx` | Partial API | `POST /battles/queue` | Active duelists count (412 Online), Season 4 champion, rules list, recent duel matches list. |
| `/battles/[id]` | `web/app/battles/[id]/page.tsx` | Partial API | `GET /battles/{id}`, `POST /battles/{id}/submit` | Hardcoded initial problem (Two Sum), local interval simulation for opponent test passing, simulated judge output. |
| `/certificates/[code]` | `web/app/certificates/[code]/page.tsx` | Partial API | `GET /api/certificates/verify/{code}` | Fallback mock certificate object if API call fails. |
| `/companies` | `web/app/companies/page.tsx` | **Hard-coded Mock** | None | `COMPANIES_DATA` array containing 6 companies, packages, rounds, target topics, and descriptions. |
| `/companies/[name]` | `web/app/companies/[name]/page.tsx` | **Hard-coded Mock** | None | Hardcoded 8-day schedule array; milestone checkboxes update local component state only. |
| `/contests` | `web/app/contests/page.tsx` | Partial API | `GET /api/contests` | Fallback contest list if API fails. |
| `/contests/[id]` | `web/app/contests/[id]/page.tsx` | Full API | `GET /api/contests/{id}`, `GET /api/contests/{id}/standings`, `POST /api/contests/{id}/submit` | Fallback mock contest and problem list if API request fails. |
| `/daily` | `web/app/daily/page.tsx` | Partial API | `GET /api/daily` | Initial streak state (3 days); "Use Streak Freeze" only modifies local React state. |
| `/interviews` | `web/app/interviews/page.tsx` | **Hard-coded Mock** | None | `INTERVIEWS_DATA` array (4 candidate debriefs); filter buttons only filter local array. |
| `/jobs` | `web/app/jobs/page.tsx` | **Hard-coded Mock** | None | `JOBS_DATA` array (5 partner companies); "Fast-Track Apply" only modifies local state array. |
| `/ladder/[problem]` | `web/app/ladder/[problem]/page.tsx` | Full API | `GET /api/ladder/{problem}`, `POST /api/ladder/stage` | Fallback 3-stage ladder if API request fails. |
| `/leaderboard` | `web/app/leaderboard/page.tsx` | Partial API | `GET /api/leaderboard` | Fallback top-5 users array if API request fails. |
| `/lists` | `web/app/lists/page.tsx` | Full API | `GET /api/lists`, `GET /api/plans`, `POST /api/lists` | Fallback system lists (Blind 75, NeetCode 150) and 30-Day Bootcamp plan. |
| `/lists/[id]` | `web/app/lists/[id]/page.tsx` | Full API | `GET /api/lists/{id}` | Fallback mock problems array if API request fails. |
| `/mock` | `web/app/mock/page.tsx` | **Placeholder / Mock** | None | Hardcoded problem (Merge Intervals), hardcoded interviewer message dialogue, hardcoded evaluation score (85/90). |
| `/patterns` | `web/app/patterns/page.tsx` | Partial API | `GET /api/patterns` | Fallback 15 patterns array from `data.ts`. |
| `/patterns/[id]` | `web/app/patterns/[id]/page.tsx` | Full API | `GET /api/patterns/{id}`, `POST /api/patterns/{id}/quiz` | Fallback pattern template and quiz question if API request fails. |
| `/placement` | `web/app/placement/page.tsx` | Partial API | `GET /api/placement/questions` | Hardcoded tracks array; fallback CS questions (OS, DBMS, Networks). |
| `/plans/[id]` | `web/app/plans/[id]/page.tsx` | Partial API | `GET /api/plans/{id}` | Day checkboxes toggle local component state; not saved to backend. |
| `/portfolio/[username]` | `web/app/portfolio/[username]/page.tsx` | **Hard-coded Mock** | None | Hardcoded stats (1,640 ELO, 32-day streak, 148 problems solved); hardcoded `ActivityTower` props. |
| `/problems` | `web/app/problems/page.tsx` | Full API | `GET /api/problems` | Fallback problem list (12 problems) if API request fails. |
| `/problems/[slug]` | `web/app/problems/[slug]/page.tsx` | Full API | `GET /api/problems/{slug}`, `POST /api/submissions/run`, `POST /api/submissions`, `GET /api/submissions`, `GET /api/notes/{id}`, `POST /api/notes`, `POST /api/ai/hint`, `POST /api/ai/review`, `GET /api/discussions/problem/{slug}`, `POST /api/discussions`, `POST /api/users/me/bookmarks/toggle` | Silent mock fallbacks in catch blocks (fakes Accepted verdict with confetti if server/judge unreachable). |
| `/profile/[username]` | `web/app/profile/[username]/page.tsx` | Partial API | `GET /api/users/{username}` | Hardcoded badge definitions; fallback user stats if API request fails. |
| `/review` | `web/app/review/page.tsx` | Full API | `GET /api/review`, `POST /api/review/grade` | Fallback flashcards array if API request fails. |
| `/roadmap` | `web/app/roadmap/page.tsx` | **Hard-coded Mock** | None | `DEFAULT_TOPICS` (7 islands) and `TOPIC_PROBLEMS` dictionary hardcoded; zero API calls. |
| `/settings` | `web/app/settings/page.tsx` | Full API | `PATCH /api/users/me` | Timezone list and default blind mode setting stored in localStorage. |
| `/visualizer/[algo]` | `web/app/visualizer/[algo]/page.tsx` | **Hard-coded Mock** | None | `TWO_SUM_TRACE` and `BUBBLE_SORT_TRACE` hardcoded step frames; no API trace generation. |

---

## 2. Interactive Elements Audit (Buttons, Forms, Links)

Interactive elements that are non-functional, do not persist to the API, or have mock handlers:

| Page / Component | Element | Current Behavior | Required Production Fix |
| :--- | :--- | :--- | :--- |
| `web/app/daily/page.tsx` | "Use Streak Freeze" button | Only updates local React state (`freezes_left - 1`). Does not persist to backend. | Wire to `POST /api/daily/freeze` or `POST /api/users/me/streak/freeze`. |
| `web/app/plans/[id]/page.tsx` | Day milestone checkboxes | Toggles local state array `completedDays`. Reloading resets progress. | Save day progress to user plan progress API. |
| `web/app/companies/[name]/page.tsx` | Milestone checkboxes | Toggles local state array `completedDays`. Reloading resets progress. | Persist company roadmap progress to backend. |
| `web/app/jobs/page.tsx` | "1-Click Fast-Track Apply" button | Adds job ID to local component state array `appliedJobs`. No DB record. | Connect to `POST /api/jobs/{id}/apply` with user Elo & certificate. |
| `web/app/mock/page.tsx` | Interview chat "Send" button | Adds message and triggers canned simulated response timeout. | Send user message to AI interview model (`POST /api/ai/interview`). |
| `web/app/mock/page.tsx` | "Finish Interview" button | Hardcodes scores (`correctness: 85, communication: 90`). | Run user code against test suite & submit to `POST /api/ai/review`. |
| `web/app/problems/[slug]/page.tsx` | Run & Submit error catch blocks | On network/judge failure, catch block fakes sample test pass or fake Accepted submission. | Show clear error banner ("Judge unavailable, please try again") without faking results. |
| `web/app/problems/[slug]/page.tsx` | Bookmark toggle error catch block | On failure, quietly inverts boolean state without notifying user of failure. | Revert optimistic state and show error toast. |
| `web/app/battles/[id]/page.tsx` | Opponent test progress | Incremented every 28s via client-side `setInterval`. | Replace with server polling or WebSocket battle state updates. |
| `web/app/battles/[id]/page.tsx` | "Play Again" button | Calls `window.location.reload()`. | Queue user for a fresh matchmaking duel (`POST /battles/queue`). |
| `web/app/portfolio/[username]/page.tsx` | GitHub & LinkedIn icon buttons | Open generic `https://github.com` and `https://linkedin.com`. | Populate with user's configured social handles from profile settings. |
| `web/app/visualizer/[algo]/page.tsx` | Input editor button | Read-only static array displays for Two Sum and Bubble Sort. | Allow custom array input and generate execution trace. |
| `web/app/roadmap/page.tsx` | Topic island completion rings | Always shows hardcoded progress numbers (e.g. Arrays: 3/4 solved). | Compute progress dynamically from user's solved problem status. |

---

## 3. API Endpoints Audit (`api/app/routers`)

All endpoints across the 17 backend routers, their HTTP methods, and frontend integration status:

| Router File | Method & Path | Called by Frontend? | Calling Frontend Component / Page | Notes |
| :--- | :--- | :---: | :--- | :--- |
| `health.py` | `GET /health` | No | Direct container healthcheck | Verifies DB connection and Judge0 reachability. |
| `problems.py` | `GET /problems` | **Yes** | `web/app/problems/page.tsx` | Supports `search`, `topic`, `difficulty`, `status`. |
| `problems.py` | `GET /problems/{slug}` | **Yes** | `web/app/problems/[slug]/page.tsx` | Returns statement, sample tests, limits, hints, editorial. |
| `submissions.py` | `POST /submissions/run` | **Yes** | `web/app/problems/[slug]/page.tsx` | Executes against sample tests with limits. |
| `submissions.py` | `POST /submissions` | **Yes** | `web/app/problems/[slug]/page.tsx` | Evaluates hidden tests, assigns verdicts, updates XP & streak. |
| `submissions.py` | `GET /submissions` | **Yes** | `web/app/problems/[slug]/page.tsx` | Retrieves past submissions for problem. |
| `daily.py` | `GET /daily` | **Yes** | `web/app/page.tsx`, `web/app/daily/page.tsx` | Deterministic daily problem & streak count. |
| `users.py` | `GET /users/{username}` | **Yes** | `web/app/profile/[username]/page.tsx` | User profile, solve statistics, rating, streak. |
| `users.py` | `PATCH /users/me` | **Yes** | `web/app/settings/page.tsx` | Updates display name, username, timezone, preferences. |
| `users.py` | `GET /users/me/bookmarks` | No | None | Endpoint available; frontend lacks dedicated bookmarks view. |
| `users.py` | `POST /users/me/bookmarks/toggle` | **Yes** | `web/app/problems/[slug]/page.tsx` | Toggles bookmark for current problem. |
| `notes.py` | `GET /notes/{problem_id}` | **Yes** | `web/app/problems/[slug]/page.tsx` | Retrieves problem note markdown. |
| `notes.py` | `POST /notes` | **Yes** | `web/app/problems/[slug]/page.tsx` | 2-second debounced autosave note endpoint. |
| `ai.py` | `POST /ai/hint` | **Yes** | `web/app/problems/[slug]/page.tsx` | Socratic hint bot. |
| `ai.py` | `POST /ai/review` | **Yes** | `web/app/problems/[slug]/page.tsx` | Complexity analysis and code review. |
| `ai.py` | `POST /ai/explain-verdict` | No | None | Backend explainer for failed test cases; not wired in UI. |
| `lists.py` | `GET /lists` | **Yes** | `web/app/lists/page.tsx` | System and user curated lists. |
| `lists.py` | `GET /lists/{list_id}` | **Yes** | `web/app/lists/[id]/page.tsx` | List details and problem list items. |
| `lists.py` | `POST /lists` | **Yes** | `web/app/lists/page.tsx` | Creates a new custom list. |
| `lists.py` | `PUT /lists/{list_id}/reorder` | No | None | Endpoint ready; UI lacks drag-and-drop reorder. |
| `plans.py` | `GET /plans` | **Yes** | `web/app/lists/page.tsx` | List of 30/60/90-day study plans. |
| `plans.py` | `GET /plans/{plan_id}` | **Yes** | `web/app/plans/[id]/page.tsx` | Plan schedule with assigned daily problems. |
| `contests.py` | `GET /contests` | **Yes** | `web/app/contests/page.tsx` | Contests list with status calculation. |
| `contests.py` | `GET /contests/{contest_id}` | **Yes** | `web/app/contests/[id]/page.tsx` | Contest details and problems. |
| `contests.py` | `GET /contests/{contest_id}/standings` | **Yes** | `web/app/contests/[id]/page.tsx` | 10-second polling leaderboard with WA penalties. |
| `contests.py` | `POST /contests/{contest_id}/submit` | **Yes** | `web/app/contests/[id]/page.tsx` | Records contest submission score & penalty. |
| `contests.py` | `GET /contests/ratings/{username}` | No | None | Historical contest rating trajectory. |
| `discussions.py` | `GET /discussions/problem/{slug}` | **Yes** | `web/app/problems/[slug]/page.tsx` | Discussion threads & solutions for problem. |
| `discussions.py` | `POST /discussions` | **Yes** | `web/app/problems/[slug]/page.tsx` | Post discussion thread or gated community solution. |
| `discussions.py` | `POST /discussions/vote` | No | None | Upvote/downvote (+1/-1); not wired in UI. |
| `analytics.py` | `GET /analytics` | **Yes** | `web/app/analytics/page.tsx` | Solves per week, topic acceptance, weak topics. |
| `analytics.py` | `GET /review` | **Yes** | `web/app/review/page.tsx` | Active recall review queue (1, 3, 7, 21 days). |
| `analytics.py` | `POST /review/grade` | **Yes** | `web/app/review/page.tsx` | Grades spaced repetition flashcard. |
| `analytics.py` | `GET /leaderboard` | **Yes** | `web/app/leaderboard/page.tsx` | Rankings by XP, streak, and Elo rating. |
| `patterns.py` | `GET /patterns` | **Yes** | `web/app/patterns/page.tsx` | 15 algorithmic pattern templates & signals. |
| `patterns.py` | `GET /patterns/{slug}` | **Yes** | `web/app/patterns/[id]/page.tsx` | Pattern detail and quiz challenge. |
| `patterns.py` | `POST /patterns/{slug}/quiz` | **Yes** | `web/app/patterns/[id]/page.tsx` | Submits quiz answer and unlocks tagged problems. |
| `ladder.py` | `GET /ladder/{problem_slug}` | **Yes** | `web/app/ladder/[problem]/page.tsx` | 3-stage brute to optimal ladder for problem. |
| `ladder.py` | `POST /ladder/stage` | **Yes** | `web/app/ladder/[problem]/page.tsx` | Validates runtime threshold per ladder stage. |
| `placement.py` | `GET /placement/tracks` | No | None | Returns track catalogue; page uses local tab definitions. |
| `placement.py` | `GET /placement/questions` | **Yes** | `web/app/placement/page.tsx` | CS core, aptitude, and regional translations (EN/HI/BN). |
| `certificates.py` | `POST /certificates/issue` | No | Tested via Pytest | Timed proctored test flow not yet hooked in UI. |
| `certificates.py` | `GET /certificates/verify/{code}` | **Yes** | `web/app/certificates/[code]/page.tsx` | Validates public certificate ID. |
| `battles.py` | `POST /battles/queue` | **Yes** | `web/app/battles/page.tsx` | Matchmaking queue for 1v1 PvP coding duel. |
| `battles.py` | `GET /battles/{battle_id}` | **Yes** | `web/app/battles/[id]/page.tsx` | Duel status, problem details, and opponent progress. |
| `battles.py` | `POST /battles/{battle_id}/submit` | **Yes** | `web/app/battles/[id]/page.tsx` | Submits battle solution and triggers win state. |

---

## 4. Fixes Executed in Phase 0

1. **Timezone Awareness Standardization (`datetime.now(timezone.utc)`):**
   - Removed deprecated `datetime.utcnow()` from:
     - `api/app/models/entities.py` (all Column defaults & onupdates converted to timezone-aware UTC)
     - `api/app/routers/contests.py` (all comparison timestamps timezone-aware)
     - `api/app/routers/analytics.py`
     - `api/app/routers/certificates.py`
     - `api/app/routers/notes.py`
     - `api/app/routers/submissions.py`
     - `api/scripts/seed.py`
   - Verified with Pytest: **All 13 tests passing in 2.42s with zero deprecation warnings**.

2. **NPM Audit Analysis:**
   - Ran `npm audit fix` (without `--force`).
   - Identified that remaining advisory on Next.js/postcss would require upgrading to Next 16.x (which is a breaking change for Next 14 App Router). Remained on stable Next 14 per guidelines.

3. **Port Availability Enforcement for `npm run dev`:**
   - Created `web/scripts/dev.js` to probe port 3000 before starting.
   - If port 3000 is occupied, it exits immediately and displays a clean message:
     ```
     [Ready2Code] ERROR: Port 3000 is currently busy / in use by another process.
     Ready2Code web server requires port 3000 by default.
     Please free port 3000 or set PORT=<port> npm run dev.
     ```
   - Updated `web/package.json` `"dev"` script to invoke `node scripts/dev.js`.
