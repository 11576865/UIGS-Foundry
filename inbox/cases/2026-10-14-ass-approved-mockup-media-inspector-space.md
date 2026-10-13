# Case — Approved mockup adaptation keeps native timeline ownership and editor space

Status: Case / Pending Android validation. No Canonical promotion.

User confirmed a native tablet layout concept after rejecting a previous semantic narrowing. Implementation composes existing renderer, timeline and authoring tools, preserves shared Style versus Event scope and does not invent one global Apply transaction.

Dedupe: search `repo:11576865/UIGS-Foundry "timeline" "movable"` returned existing Candidate `inbox/candidates/2026-10-03-presentation-density-state-continuity-by-stable-component-identity.md` and spatial-camera Candidate. This record supplies case evidence for those existing ideas rather than a new Canonical rule.

Specific addition: optional timeline dock and read-only Raw source must yield height to the active editor under IME/short-host pressure. A single movable timeline plus one saveable state owner serves dock and primary editor. Code review found a local-filter dialog gate referencing only global search, and optional Raw chrome pressure; both were corrected, with authored Android regressions pending.

Evidence: media policy probe passed 25 boundary cases; existing tablet policy passed 160 cases; 14 Kotlin files parsed without syntax errors. No Android compile, instrumentation, APK or device screenshot is claimed.

Product implementation checkpoint: b398782c on local feat/native-tablet-ui-20261014; product public push remains blocked by prior automatic review requiring explicit publication authorization. Native implementation and external validation remain separate.
