# Candidate: Foundry operationalization phase

Status: active; baseline adapter/outbox phase implemented
Date: 2026-10-02

The initial archaeology phase has moved into operation.

Implemented baseline:
- project-side adapters for ASS-Workbench-Android, Character-Voice-Service, MKV-Fast-Muxer, Quick-Automatic-Hardsub-Encoder, and HSR-Voice-Archive-Builder;
- automatic tracked-CI failure intake;
- manual semantic packet emission;
- repository-local durable uigs-outbox branches;
- Foundry collector, receipt ledger, dedupe, Pending storage, schemas, and tests.

Still pending in this larger phase:
- richer report generation;
- selective PR/issue/release signals with bounded noise;
- more searchable/visual Interface Grammar realizations;
- targeted evidence-gap archaeology.

The baseline does not automate Canonical promotion.
