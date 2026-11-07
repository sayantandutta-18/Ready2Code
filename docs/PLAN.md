# PLAN.md - Roadmap and current position

Detailed checkpoints, tasks and Done-when tests: see `Ready2Code_End_to_End_Roadmap.pdf` in `docs/`. The launch problem bank is in `Ready2Code_Launch_Problem_Bank.pdf`.

## Current position (update every session)
- Stage 0 (stabilise): in progress. Backend and frontend run locally. Database and seed work; 100 problems load.
- Known open issues: Run and Submit unverified (Judge0 not running); roadmap, lists, contests, battles, patterns, companies, interviews unverified or broken; sign-in needs a provider decision.

## Stages
| Stage | Name | Weeks (approx.) | Exit criteria |
|---|---|---|---|
| 0 | Stabilise | 1 | Every page shows real data or an honest error; one reliable dev command |
| 1 | Judge and accounts | 2-3 | Solve, submit, see "Solved" in the list; sign-in works |
| 2 | Content engine | 2-8 (parallel) | 150 validated problems (100 done) |
| 3 | Learning experience | 4-6 | Statement renderer, hints, ladder, patterns, visualizer with 12 traces |
| 4 | Progress and 3D roadmap | 6-7 | Daily goal, streak, profile; 3D roadmap with flat fallback |
| 5 | Placement hub | 7-9 | Aptitude, CS, company, HR tracks; beginner mode |
| 6 | Competition and community | 9-12 | Lists, contests, battles, discussions, XP |
| 7 | Production and beta | 12-14 | Security, monitoring, CI, deploy, 30-student beta |
| 8 | Growth | after beta | AI features, certificates, study rooms, PWA |

## Next actions (in order)
1. Finish S0.x: API and frontend run with one command; `/health` shows db and redis true; honest error messages.
2. S1.1: decide the auth provider (AUTH.md). Record it.
3. S1.2: start Judge0 locally; implement Run and Submit with verdicts.
4. S1.3-S1.4: progress and drafts.
5. Content batch 2: 50 more problems, mainly hard, plus Java and C++ references.

## Rules for this plan
- Do not start a new stage before the previous stage's exit criteria pass.
- New pages wait until Stage 1 is green.
- Each checkpoint ends with a commit and an update to `PROJECT_STATUS.md`.
