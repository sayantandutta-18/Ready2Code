# PRD.md - Product requirements

## Problem
Students preparing for placements (especially in India) struggle with DSA. Existing platforms show a problem and a blank editor. They explain little, give little structure for beginners, and offer weak support for aptitude and CS fundamentals.

## Product
Ready2Code is a DSA practice platform with a 3D visual identity. It combines a real code judge, visual step-by-step algorithm playback, pattern-first learning, and placement-preparation tracks.

## Users
| Persona | Goal | Needs most |
|---|---|---|
| First-year student | Become comfortable with DSA in 3 to 6 months | Clear starting point, plain language, hints by default, easy-to-hard order, daily goal |
| Final-year student | Pass placement tests and technical rounds | Company plans, aptitude timer, CS fundamentals, interview experiences |
| Working developer | Refresh patterns, practise under time pressure | Pattern library, timed mode, progress analytics |
| Teacher (later) | Track a class | Classroom mode, assignment progress |

## Core loop
Open the app -> see today's goal -> read a problem with examples -> write code (hints if stuck) -> Run samples -> Submit -> see a clear verdict -> view the visualizer for the idea -> see the streak go up.

## Functional requirements
### Must (launch)
- Browse 100+ problems with filters: topic, difficulty, status, tag, search. Server-side pagination.
- Problem page: statement with examples, constraints, starter code (stub), code editor, language selection.
- Run on sample tests; Submit on hidden tests; verdicts Accepted, Wrong Answer, Time Limit Exceeded, Runtime Error, Compile Error; runtime and memory shown.
- Hidden tests never sent to the browser.
- Sign-in; progress saved per user; drafts saved per user.
- Hints (3 levels); editorial after solve.
- Daily problem; streak.
- Topic roadmap (flat view and 3D view).
- Placement hub: start-here quiz, aptitude timed sets, CS fundamentals tracks, company pages with honest empty states, interview experience wall with moderation.
- Clear error messages for every failure.

### Should (after launch)
- Visualizer for 12 algorithms; dry-run mode; brute-to-optimal ladder; pattern quiz.
- Lists, contests with live standings, discussions, XP and badges.
- Spaced repetition review queue.

### Could (later)
- AI hints and code review (server-side, rate-limited).
- 1v1 battles, study rooms, certificates, PWA, React Native app.

## Non-functional requirements
- Performance: Run and Submit p95 under 3 seconds (excluding queue time). `/problems` first load under 110 kB JavaScript.
- Availability: API uptime 99 percent during beta.
- Security: no secrets in the client; hidden tests server-side only; judge isolated from API; rate limits on submissions and AI.
- Accessibility: WCAG AA; keyboard use for all actions; reduced motion respected; 3D has a flat fallback.
- Responsiveness: usable at 360px width.
- Privacy: account deletion; personal data minimal.
- Content: original statements only. No copied text from other platforms.

## Success metrics (beta)
| Metric | Target |
|---|---|
| First Run within 5 minutes of sign-up | 70 percent |
| First Accepted in first session | 50 percent |
| Day-7 return | 25 percent |
| Judge p95 | under 3 s |
| Page error rate | under 1 percent |

## Out of scope (for now)
- Paid plans, ads, and job-placement guarantees.
- Proctored exams.
- Full native mobile app (PWA first).
- Problems beyond the 150-problem launch set before beta feedback.

## Risks
See Section 11 of the roadmap PDF. Main ones: scope creep, content quality, Judge0 reliability and cost, unclear auth choice.
