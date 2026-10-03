# Candidate: Foreground user intent should not disappear behind transient background work

Date: 2026-10-04
Status: Candidate
Scope: async UI / shared execution engines / background discovery

## Observation

A background container scan and a user-requested subtitle preview shared one FFmpeg execution resource. The preview handler used a generic busy guard and simply returned when the background scan happened to be active. From the user's perspective the click was accepted by the UI but produced no result, and automated verification waited until timeout.

A related batch path could observe stale output if a requested mux did not actually start because background work still owned the executor.

## Candidate principle

When optional/background discovery temporarily owns a shared executor, a foreground action should have an explicit policy:
- queue behind the background work;
- preempt/cancel it when safe; or
- reject visibly with a retry affordance.

Silently dropping the foreground action is not an acceptable busy-state policy.

For batch/transactional work, completion must also be correlated to a newly started operation rather than inferred from "not busy" plus an old artifact still being present.

## Reusable implication

Background work should be observational and low-authority. It must not consume foreground intent or let stale completion artifacts masquerade as the result of a request that never started.

Do not promote to Canonical from this single implementation.
