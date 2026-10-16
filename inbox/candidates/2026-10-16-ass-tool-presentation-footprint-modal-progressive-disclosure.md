# Candidate — ASS Workbench presentation footprint is independent of tool activity

Date: 2026-10-16
Status: Candidate / Pending owner acceptance; not Canonical, not Figma edits
Project: 11576865/ASS-Workbench-Android
Design: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5

## Trigger
After classifying the 18 Workbench tools as active, passive, or hybrid, the owner clarified: "有些值得占用大部分屏幕，有些只适合得到一个小UI和弹窗". The former active/passive taxonomy answers which operations read versus write; it does not determine how much display area a tool deserves.

## Proposed orthogonal dimensions
- Activity / side effects: edit, observe, hybrid (plus user-initiated versus background refresh as a separate axis).
- Presentation footprint: primary workspace, docked/floating tool surface, contextual popover, inline status/cue, modal decision dialog.
- Persistence and interruptiveness: permanent context, user-retained instance, temporary peek, blocking decision. A modal is not the largest general editor: it is a decision gate that may need large before/after information; use sparingly.

## Candidate default footprint for all 18 persisted Tool IDs
| Tool ID | Default surface | Conditional expansion |
|---|---|---|
| SUBTITLES | docked list / compact drawer | workspace when searching/bulk navigating |
| TEXT | primary workspace | inline short edit if appropriate |
| EVENT | inspector | contextual popover for discrete fields |
| BATCH | primary workspace for scope/filter/recipe and diff review | decision dialog for risky commit |
| TIMELINE | large persistent dock, promotable to primary | collapsed strip when temporarily secondary |
| FRAMES | timeline companion / inspector | precision frame alignment workspace when needed |
| STYLE | persistent inspector/tool instance | font/color popovers, shared-impact review |
| POSITION | inspector + direct-manipulation overlay | large precision geometry workspace |
| VECTOR_CLIP | large video/canvas editing workspace | inspector / point-popover |
| EFFECTS | inspector for simple fade/blur | full keyframe workspace for complex transforms |
| KARAOKE | primary waveform/syllable editor | short contextual popup for timing values |
| FONTS | resource panel | expanded comparison/coverage surface |
| FONT_REQUIREMENTS | inline warning/status | small diagnostic details / inspector |
| QC | compact summary and issue navigation | report/issue inspector; conditional Quick Fix review |
| COMPATIBILITY | inline contextual signal | report panel / details |
| DIAGNOSTICS | inline health and status | log evidence/debug panel on demand |
| PROJECT | project/track inspector | file review, container operation dialog / wider workspace |
| CAPABILITIES | searchable overlay/drawer | never deserves a permanent giant panel merely because it lists all tools |

These are **initial presentation suggestions**, not declarations of currently implemented UI or new `WorkbenchTool` properties. WorkbenchToolGroup and persisted Tool IDs remain unchanged.

## Principles for implementation review
1. Space allocation follows **task complexity, comparison demands, information density, attention duration, and spatial editing needs**, not Active/Passive classification. QC is read-only by default yet can need a large report; a save command writes but should not occupy a permanent full screen.
2. **Progressive disclosure**: status/compact tool -> detailed inspector -> primary workspace when explicitly invoked; never auto-expand a warning into a modal for a routine nonblocking condition.
3. **Tool identity survives presentation changes**: switching compact/expanded, dock/float or FIXED/SPATIAL Host must not silently reset binding, Focus, Selection, draft, source provenance or write target. This is a future parity test, not currently proven in T1.1.
4. Respect tablet responsive surface: at 1024x768, promote drawer/overlay patterns to avoid five permanent columns; at 1440x900, allow more simultaneous tool inspection. Hit regions and input field usability require device testing, not only Figma pixels.
5. Modal should be for a specific interruptive decision or conflict; do not use modals for passive status, general documentation or everyday continuous editing. For risky mutation, show transaction scope and before/after, preserve undo, reject stale reviews.
6. Preserve innovative instance/edge bookmark models; a compact surface should be recallable, pinnable where allowed by `ToolDescriptor` and subject to real tested lifecycle.

## Deduplication and governance
Queried UIGS-Foundry for 'tool workspace surface footprint prominence adaptive popover', 'ASS tool surface promotion spatial hierarchy', 'active passive tool UI compact status modal', '任务空间动态升格 检查工具 UI'. No direct record of this **orthogonal footprint classification**; adjacent QHE workbench case existed. Existing candidate `inbox/candidates/2026-10-16-ass-workbench-active-passive-hybrid-tool-ui-taxonomy.md` only addresses action/side-effect behavior. This candidate extends it and must not automatically alter Canonical standards or replace T1.1 frames.

## Pending
Owner has not explicitly requested a Figma redraw in this turn, so no new Figma or Android changes. Requires owner review for tool-by-tool default and promotion patterns before implementing.
