# UIGS Intake

Intake is the automatic capture boundary between day-to-day work and reusable Foundry knowledge.

**Execution boundary:** Intake is bounded post-processing. It must follow `governance/AGENT-EXECUTION.md` and must not keep an interactive session alive for downstream Foundry CI, collection, triage, proposal generation, reporting, or promotion. If those are not immediately complete, record the appropriate Pending state and return control to the user.

After substantial work involving software design, UI/interaction, testing, failures, engineering process, architecture, CI, or cross-project methods, perform an **Intake Check**:

1. Did new reusable knowledge appear?
2. Is it already represented?
3. What is the narrowest existing family?
4. What is the source and evidence level?
5. Should it be Observation, Candidate, Case, Bug, Test, Lesson, Policy, Pattern, or implementation reference?
6. Can one bounded write or intake packet capture it now?
7. If not, mark it Pending and tell the user.
8. Stop after the bounded intake action; do not wait for downstream Foundry processing.

Automatic capture never implies automatic Canonical promotion.
