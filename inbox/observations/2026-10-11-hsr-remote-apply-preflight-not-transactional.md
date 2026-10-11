# Observation: Remote archive Apply must validate source revision at commit, not only at request

Date: 2026-10-11
Status: Open engineering risk based on source review; runtime race reproduction pending
Project: HSR-Voice-Archive-Builder
PR reviewed: https://github.com/11576865/HSR-Voice-Archive-Builder/pull/133
Head reviewed: a0d4b95712bf2fa320584224c49099afd0c2c80f

## Findings

- FastAPI `app/server.py` lines ~1351–1375 and Termux `app/lite_server.py` lines ~1232–1254 verify plan Manifest SHA-256 before enqueuing `remote-update-apply`; background closure later downloads and alters combined source/config/index without a second revision guard near publication.
- `app/jobs.py` only enforces one active task for `BUILD_KINDS = {"build", "quick-build"}` when starting a job. The remote-update-apply kind is not covered by that guard. While specific concurrent scheduling scenarios require a runtime test, there is no evident shared per-project mutation transaction encompassing remote apply and archive build.
- `app/server.py` removes existing combined directory before replacing with staging, then writes incremental CSV and changes project configuration. An interruption in the middle can leave an incomplete intermediate state. Source/member basename preflight is useful but not full rollback/atomic publication.
- Existing UI `showPlan(plan)` initializes `selectedRemoteAdditions` to *all* remote `new_logical` rows; subgroup presentation is not proof of chapter-level explicit selection.

## Recommendations for focused follow-up

Bind a committed update plan to archive and input-package revisions; recheck at publication. Introduce a per-project mutation lock covering build and remote apply. Write generated audio/index/report to versioned staging; publish only on success, preserve rollback provenance and a recoverable previous source config. Require explicit selection acknowledgment rather than advertising automatic full-selection as selective review. Validate concurrency, interrupted job, provider data changes and realistic multi-chapter WAV package.

This is a source-based Observation, not demonstrated user data corruption or a production acceptance failure. Canonical unchanged.
