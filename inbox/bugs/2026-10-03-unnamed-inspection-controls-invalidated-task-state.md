# Bug: Form-level input invalidation treated inspection controls as task-setting changes

Date: 2026-10-03
Status: Bug
Lifecycle: recorded
Scope: UI state ownership / media workbench / form event delegation

## Symptom

Post-operation verification controls such as an inspection-time slider could unexpectedly invalidate the compiled media task and erase the task object needed for source/output time mapping.

## Cause

A form-level `input` / `change` listener treated every descendant control event as a task-setting mutation. Inspection-only controls lived inside the same form but had no task-field `name`; nevertheless the generic invalidation path still cleared compiled task state.

## Fix pattern

Use semantic task-field ownership as the invalidation boundary:

- ignore form events that do not originate from a named task field;
- keep inspection/navigation controls outside task compilation semantics;
- when a visual proxy controls a real task field (for example a quality range slider), explicitly dispatch the mutation through the authoritative named field.

## Reusable implication

DOM containment is not state ownership. A shared form can contain task configuration, navigation, inspection and verification controls, but only authoritative task fields should invalidate a compiled plan.

Do not promote to Canonical from this single bug observation.
