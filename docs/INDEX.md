# INDEX.md - Documentation map

Start here. Read in this order if you are new:

1. **README.md** - what the project is and how to run it in 5 minutes.
2. **SETUP.md** - full local setup on Windows, step by step.
3. **ARCHITECTURE.md** - how the parts fit together.
4. **PRD.md** - what the product is for and what it must do.
5. **PLAN.md** - the staged roadmap and where we are now.
6. **FEATURES.md** - what works, what is broken, what is planned.

## Reference
| File | Read it when you need to... |
|---|---|
| API.md | Call or add an endpoint, or understand an error code |
| DATABASE.md | Change the schema, run migrations, seed or reset data |
| AUTH.md | Work on sign-in, sessions, or protected pages |
| DESIGN.md | Build or change a page, component, colour or 3D scene |
| INTEGRATIONS.md | Connect or configure Judge0, Redis, Postgres, AI, hosting |
| TESTING.md | Run tests or add a new one; know what "passed" means |
| DEBUGGING.md | Fix an error message you are seeing |

## For AI coding agents
| File | Purpose |
|---|---|
| AGENTS.md | Rules, session workflow, evidence required |
| MCP.md | How AI tools connect to project context and tools |

## Project records
- `PROJECT_STATUS.md` (repo root) - current stage and last passing checkpoint. Updated every session.
- `AUDIT.md` (repo root) - route, button and endpoint audit.
- `docs/` - the blueprint, roadmap and problem bank PDFs.

## Conventions used in these files
- Commands are PowerShell (Windows). Run them from the project root unless a step says `web\`.
- `<angle brackets>` mean "replace with your value". Never paste real passwords into shared docs.
- Checkpoint IDs (`S1.2`, `C3.5`) refer to the blueprint and roadmap PDFs.
