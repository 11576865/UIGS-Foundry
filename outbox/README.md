# Durable Outbox / Pending

The Outbox is the durable boundary between project-side events and Foundry intake.

Each participating product repository may create a dedicated uigs-outbox branch. Its adapter writes immutable JSON packets under packets/. The source repository's own GITHUB_TOKEN writes only to that repository; it does not need cross-repository credentials.

Foundry periodically reads those branches and imports unseen packets into outbox/pending/<owner>__<repo>/<packet-id>.json.

Imported packets remain in `outbox/pending/` as durable source evidence even after triage. Triage, proposal, and review state are stored separately under `outbox/triage/`, `outbox/proposals/`, and `outbox/reviews/`; therefore the raw Pending-file count is not an unprocessed-backlog count.

This keeps GitHub-side CI/project events durable even when the ChatGPT to GitHub connector is unavailable.

Boundary: a fact that exists only inside a chat while every external write path is unavailable cannot be made durably cross-chat by this repository alone. Such a fact must be reported as Pending until an external durable write succeeds.

Automatic collection never performs Canonical promotion.
