# Durable Outbox / Pending

The Outbox is the durable boundary between project-side events and Foundry intake.

Each participating product repository may create a dedicated uigs-outbox branch. Its adapter writes immutable JSON packets under packets/. The source repository's own GITHUB_TOKEN writes only to that repository; it does not need cross-repository credentials.

Foundry periodically reads those branches and imports unseen packets into outbox/pending/<owner>__<repo>/<packet-id>.json.

Imported packets remain in `outbox/pending/` as durable source evidence even after triage. Triage, proposal, and review state are stored separately under `outbox/triage/`, `outbox/proposals/`, and `outbox/reviews/`; therefore the raw Pending-file count is not an unprocessed-backlog count.

This keeps GitHub-side CI/project events durable even when the ChatGPT to GitHub connector is unavailable.

Boundary: a fact that exists only inside a chat while every external write path is unavailable cannot be made durably cross-chat by this repository alone. Such a fact must be reported as Pending until an external durable write succeeds.

Automatic collection never performs Canonical promotion.

## Collector consistency and failure boundaries

The collector's `--dry-run` reports proposed changes but does not write Pending,
Receipt or report files. One malformed packet does not block the remaining
packets in its repository. A Receipt whose Pending payload is missing or
identity-mismatched is a reported integrity error, not an already-collected success.

An interrupted run can adopt a byte-equivalent immutable Pending JSON object
after a previous crash, but refuses to overwrite a conflicting payload.
Collected successes are written even if another source or packet fails, and
the workflow remains red on any reported partial error. Downstream Git push
and review completion remain separate asynchronous evidence boundaries.
