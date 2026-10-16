# Case — ASS Workbench tablet V1.1 design implementation baseline with SPATIAL

Date: 2026-10-16
Status: **DESIGN BASELINE APPROVED by owner**; implementation and device acceptance PENDING
Figma file: https://www.figma.com/design/5yNY5dMnmpmaOnYxDlEhY5
Baseline page ID `56:2`: `ASS Workbench · Tablet UI V1.1 · 实施基线 2026-10-16`
Related prior Case: `inbox/cases/2026-10-16-ass-tablet-v11-desktop-professional-workspace-reference.md`

## Owner authorization
"实际上怎么样，只有使用了才知道，定稿吧。无限画布在这个UI里处于什么位置"

Scope: stop indefinite design-only iterations; designate V1.1 as **frozen implementation-design baseline**, not functionality-complete production release. Integrate the infinite canvas into the very same V1.1 product as a selectable alternative workspace, not a tool, unrelated app, or third permanent UI variant.

## Repository model grounding
`docs/INFINITE-CANVAS-WORKBENCH-V2.md`: new sessions default FIXED; previously saved `SPATIAL_EXPERIMENTAL` still restores; two Hosts share project, ASS domain model, media clock and tool identity. `docs/MULTI-UI-CAPABILITY-MIGRATION-2026-10-11.md` distinguishes production entries from historic experimental gaps: bookmark side model, dock and precision models partially migrated, but four-edge orchestration, dock/tab groups and universal draft survival remain unproved.
`app/src/main/kotlin/io/github/assworkbench/app/ui/WorkbenchToolCatalog.kt`: 18 stable Tool IDs; Style/Position support PinnedEvent and duplication; TEXT/EFFECTS do not claim pin by default. Maintain persisted names and preexisting project formats.

## Frozen V1.1 screens (all Figma-native editable)
The page now contains eight top-level tablet screens:
1. `56:3` FIXED main subtitle editor, 1440×900
2. `59:2` professional audio/timing task workspace, 1440×900
3. `61:2` compact FIXED editor, 1024×768
4. `63:2` compact subtitle grid drawer, 1024×768
5. `76:2` **SPATIAL board**, 1440×900 — selectable top workspace tab; shared project chrome; semantic world with independent ToolInstances, subtitle objects, media preview, POSITION pinned Event #38 vs Focus #39, side bookmarks, recall, birdseye and timeline Dock.
6. `77:2` **SPATIAL focused editor**, 1440×900 — native-density POSITION inspector, geometry proxy and same timeline Dock; explicit Back to board.
7. `78:2` **SPATIAL board**, 1024×768 — independent compact composition, not downscaled desktop canvas; toolbar, overview cards, independent bookmarks and persistent time dock.
8. `80:2` **SPATIAL focused editor**, 1024×768 — native-density controls and compact video reference; Back to board, dock preserved.

Design entry: FIXED main/timing SPATIAL top tab → 1440 board; compact FIXED SPATIAL tab → 1024 board; Position card → focused editor → same board; FIXED tab returns to corresponding FIXED layout. Eleven new view-only prototype routes were created in this approval turn in addition to preexisting V1.1 routes. Old V1 `43:2` and T1.1 legacy `0:1` remain separate and unmodified. Page renamed as implementation baseline; status-footers label **design finalized, pending Android device evidence**.

Actual Figma get_screenshot inspections performed for 1440 spatial board, 1440 focused, 1024 board and 1024 focused. Structural readback confirmed eight screens with 1440×900/1024×768 size and preserved editable text layers. A cloned 1024 "Add Tool" control incorrectly inherited a shortcut to the Event drawer; deliberately removed its prototype reaction in both compact spatial states. A design affordance with no real handler must not falsely navigate to an unrelated feature.

## Nonnegotiable native handoff
- This design freeze **does not** mean native UI built, benchmarked or tested. No Android code, renderer, parser, shipping version, release approval or Canonical changes.
- Preserve FIXED default and explicitly selectable SPATIAL_EXPERIMENTAL saved mode. Do not migrate away ToolInstance IDs, Binding, Focus/Selection, current write target, undo/document history, unsaved draft, world camera, node geometry, bookmarks or timeline media clock when switching Hosts.
- Spatial camera zoom must never shrink real tool text/touch affordances. Birdseye low-detail semantic cards vs focused full-density editor have different purposes. Dedicated gesture ownership separates camera manipulation from native editor manipulations. Camera/layout/focus transitions must not create ASS Undo entries.
- Dedicated regression plan required: 1440/1024 layout and IME, Focus vs Pinned identity, back/restore, timeline continuity, clipped panel and tap targets, file reopen/persistence, video libass actual renderer evidence, waveform responsiveness, older project migrations, fail-closed staged write/review.
- Some historical four-edge bookmaking and docking behaviors are **not shown** as fully implemented by this baseline. The compact Add Tool click and some workspace tools still lack prototype completion; schedule native wiring rather than claiming success.
- Review-after-use: owner may authorize targeted revision once tested, preserving baseline as a reference. Freeze is design scope closure, not product change ban.

## UIGS Foundry Intake
Searched `2026-10-16 ASS tablet V1.1 final implementation baseline SPATIAL`, `ASS Workbench frozen final UI FIXED SPATIAL shared ToolInstance`, `tablet v1.1 spatial focus native density baseline`. Found related earlier spatial-camera Candidate but not this explicitly approved eight-screen integrated product Case. New Case is bounded to this concrete project decision; **do not modify UIGS Canonical automatically**. Case state: complete Figma design, Pending Android parity and usability evidence.
