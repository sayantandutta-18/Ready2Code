# TESTING.md

## Test layers
| Layer | Tool | Location | Command |
|---|---|---|---|
| API unit and integration | pytest | `api/tests/` | `python -m pytest api\tests` |
| Content (problem bank) | judge-style validator | `content/scripts/validate_content.py` | `python content\scripts\validate_content.py` |
| Problem files (older checker) | Python script | `scripts/validate_problems.py` | `python scripts\validate_problems.py` |
| Frontend build and types | Next.js build | `web/` | `npx next build` |
| Frontend unit (planned) | Vitest + Testing Library | `web/` | `npm test` |
| End-to-end (planned, Stage 7) | Playwright | `tests/e2e/` | `npx playwright test` |
| Accessibility (planned) | axe in Playwright | `tests/e2e/` | part of e2e |

## Current baseline (must stay green)
- `api/tests/test_api.py`: 13 tests pass.
- `content/scripts/validate_content.py`: `failures: 0`, 100 problems, at least 8 hidden tests each (1,192 tests total at last run).
- `npx next build`: builds 20+ routes without errors.

## What validate_content.py does
- For each `content/problems/*.json`: runs `reference_python` on every sample and hidden test and compares with the stored output.
- Exit code 1 if any problem fails or has fewer than 8 hidden tests.
- Run it from the project root, before every commit that touches `content/`.

## Adding a test for a new endpoint
1. Put the test in `api/tests/test_<area>.py`.
2. Use the test client (or the real app) and check status code and response shape.
3. Check that no hidden test data appears in the response.
4. Run `python -m pytest api\tests`.

## Hidden-test rule (must be tested)
Add a test that calls `GET /problems/{slug}` and checks that no hidden test input or output appears in the JSON. Add it before S1.2 ships.

## Browser checks (manual, until Playwright exists)
For each checkpoint, open the page and record:
- Page loads with real data (count shown).
- Empty state appears when a filter matches nothing.
- Error state appears when the API is stopped (stop window 1, reload, expect a clear message; then start it again).
- Browser console (F12) has no red errors.

## Definition of done for a checkpoint
- The checkpoint's Done-when test passes in the browser.
- Relevant automated tests pass (above).
- No new console errors.
- Commit message names the checkpoint.

## Known gaps
- No frontend unit tests yet.
- No Playwright tests yet.
- Judge (Run and Submit) cannot be tested until Judge0 runs locally (S1.2).
