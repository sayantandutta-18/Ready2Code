# DATABASE.md

Engine: PostgreSQL 16 (local via Docker). ORM: SQLAlchemy 2.0. Migrations: Alembic in `api/migrations/`.

## Connection
Local `api/.env`:
```
DATABASE_URL=postgresql://<POSTGRES_USER>:<POSTGRES_PASSWORD>@localhost:5432/<POSTGRES_DB>
```
Use the same user, password and database name as the root `.env` used by Docker Compose.
Special characters in the password (`@ : / # % space`) must be URL-encoded or avoided.

## Migrations
```powershell
.\venv\Scripts\Activate.ps1
alembic -c api\migrations\alembic.ini upgrade head     # apply
alembic -c api\migrations\alembic.ini downgrade -1     # roll back one step
alembic -c api\migrations\alembic.ini revision -m "add xyz"   # new migration
```
Rules:
- One migration per schema change.
- Never edit an applied migration. Add a new one.
- Ask before any destructive change (dropping a column or table).

## Tables (current and planned)
| Table | Purpose | Status |
|---|---|---|
| topics | Ordered topic list (10 launch topics) | Seeded |
| problems | Slug, title, statement, difficulty, scene, limits, starter code | Seeded (100) |
| problem_tags | Pattern, company and custom tags | Planned/partial |
| problem_tests | Sample (`is_hidden=false`) and hidden (`is_hidden=true`) tests, JSON text | Seeded |
| problem_hints | Three hint levels per problem | Seeded (topic-level hints) |
| editorials | Approach, complexity, common mistake | Planned |
| submissions | Verdict, runtime, memory, failed test index | Planned (S1.2) |
| user_problem_status | todo, attempted, solved; best runtime | Planned (S1.3) |
| drafts | Server-side code drafts per user, problem, language | Planned (S1.4) |
| bookmarks, notes | Per user per problem | Planned (C1.8) |
| daily_problems, streaks | Daily goal and streak | Planned (S4.4) |
| patterns, pattern_quiz, quiz_attempts | Pattern lessons and quiz | Planned (S3.4) |
| aptitude_questions, aptitude_attempts | Placement aptitude | Planned (S5.2) |
| cs_questions, cs_progress | CS fundamentals | Planned (S5.3) |
| companies, company_problem_tags | Company pages with general info | Planned (S5.4) |
| interview_posts | Experience wall; status `pending`, `approved`, `hidden` | Planned (S5.5) |
| lists, list_items, contests, contest_entries, battles, discussions, badges, xp_ledger | Community features | Planned (Stage 6) |

## Seeding
```powershell
python api\scripts\seed.py
```
- Reads `content/problems/*.json` and `content/index.json`.
- Idempotent: running it again prints `Loaded 0 new problems`.
- Output to check: `Total problems in database: 100` and `Total topics in database: 10`.
- If it prints 0 after a fresh database, check that migrations ran first.

## Important columns
- `problems.slug` unique. Used in URLs.
- `problems.difficulty` one of easy, medium, hard.
- `problem_tests.input_text` and `output_text` store JSON text.
- Timestamps: timezone-aware (`timestamptz`), stored in UTC.

## Indexes (planned)
- `submissions(user_id, problem_id, created_at)`
- `problems(topic_id, difficulty)`
- `problem_tags(tag)`
- `user_problem_status(user_id, status)`
- `review_queue(user_id, due_date)`

## Backup and restore (before production)
- Daily dump. Test one restore before launch.
- Keep dumps out of the repo.

## Local reset (destroys local data only)
```powershell
docker compose down -v
docker compose up -d postgres redis
alembic -c api\migrations\alembic.ini upgrade head
python api\scripts\seed.py
```
Run this only on the development database. Check `POSTGRES_DB` first.
