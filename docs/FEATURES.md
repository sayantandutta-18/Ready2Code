# FEATURES.md - Feature status

Status key: DONE = verified in the browser. PARTIAL = visible but incomplete or not verified. BROKEN = known failing. PLANNED = not built. The status comes from the screenshots reviewed on 5 November 2026 and from the test results; update it after each checkpoint.

## Core practice
| Feature | Status | Notes / checkpoint |
|---|---|---|
| Problem bank (100 problems, 10 topics) | DONE (content) | Loaded by seed; check `/problems?limit=200` |
| Problem list with filters (topic, difficulty, status, tag, company, search) | BROKEN -> verify | Was "Could not load problems" (API down). C1.3 |
| Problem page: statement, examples, constraints | PARTIAL | Statement shows raw backticks; examples section missing (S3.1) |
| Monaco code editor, language select, font size, reset | DONE (UI) | Starter code gave away the solution; should be a stub (S1.4) |
| Run on samples | UNVERIFIED | Needs Judge0 running (S1.2) |
| Submit on hidden tests with verdicts | UNVERIFIED | S1.2 |
| Runtime and memory percentiles | PLANNED | S1.6 |
| Drafts saved per user and language | PLANNED | S1.4 |
| Hints (3 levels) | PARTIAL | Topic-level hints in content; problem-specific later (S3.2) |
| Editorial (gated until solved) | PLANNED | S3.2 |
| Notes and bookmarks | PLANNED | C1.8 |
| Brute to optimal ladder | PLANNED | S3.3 |
| Dry-run mode | PLANNED | S3.7 |
| Ctrl+Enter run, Ctrl+Shift+Enter submit | UNVERIFIED | Shortcut text shown on buttons |

## Learning and visualisation
| Feature | Status | Notes / checkpoint |
|---|---|---|
| 3D algorithm visualizer page | PARTIAL | Opens a default scene regardless of slug; labels overlap (S3.5) |
| Traces for 12 algorithms | PLANNED | S3.6 |
| Pattern library and quiz | PLANNED | S3.4 |
| Python execution trace | PLANNED | C3.2 |

## Progress and habit
| Feature | Status | Notes / checkpoint |
|---|---|---|
| Daily challenge card on home | PARTIAL | Shows even when API is down; may be static (S4.4) |
| Streak and XP in header | PARTIAL | Shows 0 when signed out |
| Profile heatmap and counts | PLANNED | S4.5 |
| 3D topic roadmap | BROKEN | "Could not load roadmap" (S4.1-S4.3) |

## Accounts
| Feature | Status | Notes / checkpoint |
|---|---|---|
| Sign in / create account modal | BROKEN | "Failed to fetch" when API down; demo buttons (S1.1) |
| Demo login | DEV ONLY | Must be off in production |

## Community and competition
| Feature | Status | Notes / checkpoint |
|---|---|---|
| Lists (system and custom) | UNVERIFIED | Reported broken (S6.1) |
| Contests with live standings | UNVERIFIED | Reported broken (S6.2) |
| 1v1 battles | UNVERIFIED | Reported broken; needs judge and auth first (S6.5) |
| Discussions | PLANNED | S6.3 |
| XP, badges, leaderboard | PLANNED | S6.4 |
| Spaced repetition review | PLANNED | S6.6 |

## Placement hub
| Feature | Status | Notes / checkpoint |
|---|---|---|
| Patterns page | UNVERIFIED | Reported broken (S3.4) |
| Companies pages | UNVERIFIED | Reported broken; needs honest empty states (S5.4) |
| Interview experience wall | UNVERIFIED | Reported broken; needs moderation (S5.5) |
| Aptitude module | PLANNED | S5.2 |
| CS fundamentals tracks | PLANNED | S5.3 |
| HR and resume track | PLANNED | S5.6 |
| Start-here onboarding quiz | PLANNED | S5.1 |
| Language toggle for summaries | PLANNED | S5.8 |

## Infrastructure
| Feature | Status | Notes |
|---|---|---|
| FastAPI + SQLAlchemy + Alembic | DONE | 13 pytest tests pass |
| PostgreSQL via Docker | DONE (local) | Requires Docker Desktop running |
| Redis via Docker | DONE (local) | Requires password match |
| Judge0 | PLANNED (local) | Start in S1.2 |
| Health endpoint | DONE | Reports db, redis, judge0 |
| CI (GitHub Actions) | PARTIAL | Workflow folder exists; verify it runs |
| Production deploy | PLANNED | Stage 7 |
