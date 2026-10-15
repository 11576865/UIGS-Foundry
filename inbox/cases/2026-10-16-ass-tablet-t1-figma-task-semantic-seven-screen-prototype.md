# Case — ASS Tablet T1: native editable Figma task-semantic design, not Android delivery

Date: 2026-10-16
Status: Design Case / 7 editable Figma frames and prototype links verified; **PENDING owner review, true media evidence, full interaction and native implementation**
Product: 11576865/ASS-Workbench-Android
Design file: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5
Baseline concept: 1440×900 tablet landscape ONLY; no phone layouts; no Android source modification.

## User instruction / design correction
The owner judged earlier R3 concept not sufficiently meaningful and said it had not been implemented in the application. Owner authorized a new Figma-native tablet UI drawing, consulting R3, v3, earlier interfaces and explicit icon distinctions from provided screenshots: object, action, status, explanatory controls. This is not approval of the prior R3 or permission to call the new concept final.

## Actual authoring in Figma
Seven distinct top-level Figma Design frames, native editable TEXT/FRAME/SHAPE/VECTOR trees rather than one flattened screenshot:
- 01 `2:21` — FIXED layout/visual subtitle manipulation, Event list, editable source-aware inspector, video reference illustration, shared clock/waveform/timeline.
- 02 `2:612` — TIME, full time-lane editing with video/audio/subtitle/effects tracks, start/end/duration, VFR boundary.
- 03 `4:2` — EFFECTS, distinct editable multi-property/keyframe curve, fade/blur/scale/alpha, Event tags, safety/preview/review.
- 04 `5:2` — Karaoke, `\k` syllable segments against waveform with selected segment timing, source and sum.
- 05 `6:2` — write review, literal Raw ASS before/after, Event-local target, source chain, Style unchanged, fail-closed revision intent, separated confirm.
- 06 `7:2` — SPATIAL as an independent selectable full-screen Host, world grid/camera, tool instances, bookmarks, media rendering reference, one timeline.
- 07 `8:2` — 18 stable professional Tool ID directory, grouped by task, including CAPABILITIES as the current directory role (not a recursive editor). Exact 18 IDs confirmed with 18 unique entries.

Figma design contains 18 local semantic color variables; per-frame structural audit counted 56–156 editable TEXT nodes each and vector-icon groups on all frames (all >0). 53 cross-screen Figma ON_CLICK NAVIGATE reactions were authored; readback after authoring found 7/7 root screens with 2–12 reaction-bearing nodes. **Navigation** works at prototype level; inputs, save, media, subtitle transforms and domain writes are designs, not executable implementations. Figma source: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5?node-id=2-21

## Actual visual review and corrections
Used `get_screenshot` on 01/02/03/04/05/06/07 at native or scaled dimensions, inspected output:
- 01 initial subtitle edit selection used an opaque accent rectangle, covering the text. Corrected to transparent fill plus accent stroke.
- 03/04 cloned navigation retained a stale selected indicator from POSITION; moved the indicator to the actual active task.
- 04 mini video preview used `resize()`, clipping the subtitle because children retained original coordinates. Restored source dimensions then `rescale(0.513)`, returning a 342.68×192.38 miniature with proportionally scaled descendants; verified in screenshot.
- Task-specific screens are genuinely differently composed, not seven R3 tri-column screenshots with relabeled tab titles.
- Concept media is an editable procedural city illustration labelled reference media; it is **not** actual video/ASS rendering.

## Tooling observations
1. A multi-screen `use_figma` call returned >20,480 bytes of created node IDs, and the service responded **'Canvas edits from this run were not committed.'** Split changes into bounded operations, then re-run, and return manageable ledgers.
2. Prototype `NAVIGATE` to the same top-level source frame was rejected with a clear validation error. Do not author self-links for selected tabs or CAPABILITIES-in-current-directory.
3. For nested visual previews, `resize` changes a clip frame without scaling descendants; `rescale` is required when the desired result is a faithful scaled reference.

## Limits / acceptance boundary
- Owner has not accepted the aesthetics, information density, navigation or touch affordance; do not freeze.
- Figma UI is **not** Android Jetpack Compose implementation or data-safe editor functionality. 18 visible entries do not prove 18 production consumers. Prototype links do not certify saved files, media PTS, libass, real writing or UI completeness.
- Some buttons intentionally do not simulate actions that would falsely imply save/commit. Representative real-media and external-device evidence remain pending.
- Next step is owner review in Figma, then a task-based interaction specification and selected source-to-native fidelity implementation and capture (exact SHA/device), not immediate replacement of current production UI.

## Dedupe / governance
Before recording, searched UIGS-Foundry for 'ASS Tablet T1 Figma seven screen design', 'Figma semantic icon grammar native editability prototype', 'Figma MCP NAVIGATE destination rejected self frame' and 'Figma rescale clipped media preview'; no exact match. Adjacent prior art: `inbox/observations/2026-10-14-ass-r3-four-screen-design-delivery-and-native-evidence-boundary.md`, `inbox/observations/2026-10-13-ass-design-reference-to-android-ui-fidelity-gap.md`, `inbox/observations/2026-10-13-ass-control-grammar-visibility-and-motion-task-hierarchy.md`. This Case records a **new actual Figma-native delivery plus concrete tool/visual QA**, not a normative replacement for those records. No Canonical modification.
