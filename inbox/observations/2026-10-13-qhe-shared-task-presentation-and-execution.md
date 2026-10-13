# Observation: guided and professional views share a task executor

Date: 2026-10-13
Source: QHE PR #105 continuation after 104d9cd
Status: implementation/local checks passed; hosted browser acceptance Pending

Dedup: queried inbox/observations/2026-10-13-qhe-guided-manual-intent-handoff.md (blob 7674ef7). This extends that one-way CPU import into shared authoritative form/lifecycle presentation, not a new Canonical rule.

Both views retain one existing mediaTaskForm with the same current settings, checked output plan, result ownership, progress, cancellation and save/retry controls. Guided hides precision editors; switching views does not regenerate settings. Goal exploration is explicitly separate from the current executable task; its CPU template requires explicit apply. New normal guided execution delegates to the shared current-task submit path, bypassing the separate generic busy wrapper. Legacy recovered Native jobs keep their original monitor/export route. Whole-file measurement tools remain visible outside the hidden precision fieldset. Reparented shared output fields invalidate current compiled evidence even when their input events no longer bubble through the form.

Four new routing/presentation tests observed RED, then GREEN. Local Node 229 passed/8 conditional skips; six real FFmpeg integration cases and Vite build passed. Browser fixture checks unchanged canonical values across view switch, one form, shared task retaining preset and per-track channels, save failure/retry across views without re-encoding, and cancellation. Production phone checks now require shared workspace and absence of a second normal executor. Local Chromium missing; do not claim real DOM, native dialog, screenshots or usability acceptance until CI evidence is reviewed. Previous head 104d9cd all nine hosted workflows passed. Resolution cross-product, budget precision and broader field acceptance remain separate open work.


## Hosted acceptance observed

Head 2e81ac1449319136aafa70c103f2d3c178329694 passed all nine workflows. Frontend 38360213661 step check-media-ui.cjs completed, including unchanged canonical values across views, shared run, cancellation and failed-save retry across views without encoding again (simulated media callbacks). Windows smoke/stream-plan/VVC and Android emulator regressions also passed. Downloaded screenshot artifact 11795090075 SHA-256 matched 2a61c0dfd720bfa0013d781d3d556b9dc87f4ebcc92ff3d609325681201ec258. Phone guided shared workspace and desktop unloaded-source goal layout visually reviewed; images do not prove a real user-media/device flow. Guided phone remains long with configuration/trial content, a usability refinement debt. Product manifest docs/evidence/five-round-delivery/shared-task-ui-acceptance-2026-10-13.json records runs, PNG hashes and limits. This closes hosted-Pending evidence only; no Canonical promotion or physical/provider/player acceptance.
