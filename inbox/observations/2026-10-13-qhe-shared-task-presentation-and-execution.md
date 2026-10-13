# Observation: guided and professional views share a task executor

Date: 2026-10-13
Source: QHE PR #105 continuation after 104d9cd
Status: implementation/local checks passed; hosted browser acceptance Pending

Dedup: queried inbox/observations/2026-10-13-qhe-guided-manual-intent-handoff.md (blob 7674ef7). This extends that one-way CPU import into shared authoritative form/lifecycle presentation, not a new Canonical rule.

Both views retain one existing mediaTaskForm with the same current settings, checked output plan, result ownership, progress, cancellation and save/retry controls. Guided hides precision editors; switching views does not regenerate settings. Goal exploration is explicitly separate from the current executable task; its CPU template requires explicit apply. New normal guided execution delegates to the shared current-task submit path, bypassing the separate generic busy wrapper. Legacy recovered Native jobs keep their original monitor/export route. Whole-file measurement tools remain visible outside the hidden precision fieldset. Reparented shared output fields invalidate current compiled evidence even when their input events no longer bubble through the form.

Four new routing/presentation tests observed RED, then GREEN. Local Node 229 passed/8 conditional skips; six real FFmpeg integration cases and Vite build passed. Browser fixture checks unchanged canonical values across view switch, one form, shared task retaining preset and per-track channels, save failure/retry across views without re-encoding, and cancellation. Production phone checks now require shared workspace and absence of a second normal executor. Local Chromium missing; do not claim real DOM, native dialog, screenshots or usability acceptance until CI evidence is reviewed. Previous head 104d9cd all nine hosted workflows passed. Resolution cross-product, budget precision and broader field acceptance remain separate open work.
