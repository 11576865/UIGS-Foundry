# Pending Triage

Pending triage converts durable intake packets into a machine-readable first assessment. It does **not** create Canonical knowledge.

For CI failures, triage uses evidence captured by the source adapter:

- workflow name and conclusion;
- failed job names;
- failed step names;
- source repository and routing hints.

The classifier is intentionally deterministic and conservative. It emits `unknown` when evidence is insufficient or when two categories are too close.

A triage record may also suggest related Foundry records. A suggestion means "inspect this prior knowledge"; it does not mean the new failure is the same bug.

Pipeline:

```
Pending Packet
-> deterministic Red Reason classification
-> related-knowledge hints
-> needs-review / auto-classified
-> human/agent triage
-> Bug / Test / Case / Observation / Candidate
```
