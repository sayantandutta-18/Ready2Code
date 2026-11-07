# DESIGN.md - Visual and interaction design

## Principles
- Dark, spatial interface. 3D is used only where it teaches or rewards: the visualizer, the topic map, the activity view, the hero.
- Forms, tables, and the code editor stay flat and high contrast.
- Motion explains state (unlock, verdict, progress). No decorative motion.
- Students first: plain language, clear next step, no dead ends.

## Color tokens (`web/styles/tokens.css`)
| Token | Hex | Use |
|---|---|---|
| `--bg-space` | `#0B1220` | Page background, 3D clear color |
| `--surface-1` | `#121C2F` | Cards, panels |
| `--surface-2` | `#1A2740` | Raised panels, modals |
| `--accent-cyan` | `#22D3EE` | Primary action, active node |
| `--accent-violet` | `#8B5CF6` | Secondary accent, patterns, badges |
| `--text-primary` | `#E2E8F0` | Body text |
| `--text-muted` | `#94A3B8` | Helper text (check contrast on surface-2) |
| `--verdict-ac` | `#22C55E` | Accepted |
| `--verdict-wa` | `#EF4444` | Wrong Answer, Runtime Error |
| `--verdict-tle` | `#F59E0B` | Time Limit Exceeded |
| `--easy` / `--medium` / `--hard` | `#34D399` / `#FBBF24` / `#F472B6` | Difficulty chips |

Contrast: WCAG AA. 4.5:1 for body text, 3:1 for large text.

## Elevation
| Level | Use | Treatment |
|---|---|---|
| 0 | Background, 3D scene | No shadow |
| 1 | Cards, rows | 1px border `rgba(148,163,184,0.15)`, soft shadow |
| 2 | Hover, modal | Cyan border glow, stronger shadow, `translateZ(24px)` |
| 3 | Active verdict, unlocked node | Pulse glow, scale 1.04 |

## Components (use these; do not restyle per page)
Button (primary, ghost, danger), TiltCard, Panel, VerdictBadge, DifficultyChip, TagChip, SplitPane, CodeEditor (Monaco wrapper), TestCaseTable, StreakBadge, XPBar, Toast, Modal, EmptyState, Skeleton, Scene3DFallback.

## Layout and responsiveness
- Must work at 360px width.
- Problem page: statement and editor side by side on desktop (resizable); on mobile, a tab switch between "Problem" and "Code".
- Keep the editor and statement above the fold at 1280px.

## 3D rules
- Lazy-load every 3D component (`next/dynamic`, `ssr: false`). The 3D code must not load on `/problems`.
- Pixel ratio capped at 1.5.
- Use instancing for more than about 50 objects.
- Every 3D view has a flat fallback with the same labels and controls.
- Respect `prefers-reduced-motion`: no tween, instant state change.
- Never place 3D behind the code editor or the statement text.

## Visualizer (3D algorithm stage)
- Input: a trace file per problem (frames of state and notes).
- Controls: play, pause, previous, next, speed, scrub bar, reset camera.
- Keyboard: Space plays or pauses, Left and Right step, 1 to 3 change speed.
- Every frame has a text note under the canvas, read by a live region.
- Labels must not overlap. Check at 1280px wide.

## Copy and tone
- Button text uses action words: "Run samples", "Submit", "Solve next problem", "Save list".
- Empty states say what to do next, with one button.
- Errors say what happened and what to try, for example "Cannot reach the server. Start the API, then press Retry."

## Accessibility checklist
- Visible focus ring on every interactive element.
- Icon-only buttons have `aria-label`.
- Verdict is never shown by colour alone; include the text.
- Forms have labels, not only placeholders.
