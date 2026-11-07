# AUTH.md - Authentication and authorization

## Current state (local development)
- Sign-in uses a username (no password) through the "Sign In" modal.
- One-click demo accounts ("Ninja Coder", "Byte Master") exist for development only.
- Demo login is controlled by `DEV_DEMO_LOGIN`. It must be `false` in production.
- Known issue: the sign-in request previously failed with "Failed to fetch" when the API was not running or CORS blocked it. See `DEBUGGING.md`.

## Decision pending (checkpoint S1.1)
Pick one provider before building battles, lists, contests or streaks:
| Option | Pros | Cons |
|---|---|---|
| Clerk (recommended) | Sign-up, sessions, social login ready; less code | Third-party service; needs keys |
| Own JWT (`JWT_SECRET`) | No external service; full control | You write password hashing, reset, email |
| NextAuth | Good for Next.js | Split logic between web and api |

Write the final choice in this file and in `PROJECT_STATUS.md`.

## Rules (apply to any provider)
- Reading problems is public. Anonymous users can browse and read statements.
- These need a signed-in user: Run and Submit (save), notes, bookmarks, discussion posts, lists, contests, battles, streak.
- Protected endpoints return `401` with `{ "error": { "code": "not_signed_in", ... } }`.
- The frontend shows "Sign in to save your progress" instead of a broken error.
- A signed-in user can only read and change their own notes, submissions and drafts.

## Secrets
- `JWT_SECRET`: at least 32 random characters. Generate with `openssl rand -hex 32` (or PowerShell equivalent). Never commit it.
- Use different values for local, staging and production.
- If a secret was pasted into a chat, log, screenshot or public repo, rotate it.

## Test accounts
- Create test users only in the development database.
- Do not seed real personal data.
