# Observation: Global Add must preserve active workbench context

Date: 2026-10-15
Status: Observation — source-level bug corrected in Draft PR; final-head E2E pending
Product: 11576865/MKV-Fast-Muxer
Implementation: https://github.com/11576865/MKV-Fast-Muxer/pull/155

## Reproduction in reviewed source

In the existing 10.14 UI shell `src/softmux-10.14-workbench.js`, the shared header command `#sf14Add` always invoked `changeView('single')`, focused the source pane, and clicked `#unifiedAssetInput`. When a user was actively reviewing the batch task matrix, the command unexpectedly switched workbench modes rather than adding resources to the current batch. A successful E2E run and attractive tablet screenshot did not cover this contextual error.

## Corrected behavior in Draft PR #155

- Keep the current batch view active when Add is invoked there.
- On tablet, reveal the same existing `.batch-inputs` drawer and focus the real `#batchUnifiedInput`; on larger screens use the real batch input directly. On single view, keep existing single-resource behavior.
- No duplicate file input, batch recipe, project state, listener or file permissions.
- E2E now asserts that the mode stays `batch`, batch sources become visible, and the original file input retains exactly one DOM identity.

This is a user-task routing rule, not a new backend command. It is distinct from a single centralized action whose semantics are independent of context.

## Transferable rule

When a global toolbar control names an action shared by multiple task modes (Add, Import, Save, Inspect), resolve its *target domain scope* from the active task before triggering side effects. Do not silently navigate into another task or data authority. If a command truly does not apply, disable it or explain that mismatch rather than silently changing scope. Test against populated state as well as a newly opened empty workbench, and verify the original handler/input identity after responsive reflow.

## Dedupe

- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md` governs prospective output composition as dominant object, not context-sensitive routing of shared commands.
- `inbox/observations/2026-10-13-ass-native-contextual-specialist-tool-access-low-copy.md` records specialist tool discoverability, not misdirected global resource intake.
- `inbox/observations/2026-10-15-softmux-design-backend-capabilities-miscast-as-ui-navigation.md` deals with backend algorithms being promoted into top-level navigation.

This is a narrow reproducible issue and bounded fix; it does not promote any Canonical UX rule. At submission the latest PR head for this fix is `4b60783708819154f0a22605c8f2abc60e002ae1`; final exact-head browser E2E must still be checked.
