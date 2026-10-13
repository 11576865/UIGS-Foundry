# Case: Native Fade/Blur editing draft safety

Date: 2026-10-14
Status: Source committed; native validation pending
Project: ASS-Workbench-Android

## Observation
Native Fade and Blur fields in an Event editor previously depended on transient Composable state and could disappear across task or Host switches. Fade Apply also lacked an authoritative Event source check.

## Changes
- Introduced session/Event-owned Fade and Blur drafts with source baselines, conflict state, explicit discard and saveable restoration.
- Separate Blur and Fade groups can retain each other's unfinished values while the edited group is acknowledged.
- Routed Fade to source-checked ViewModel Apply, with alpha and timeline validation, existing ASS semantic patchers and Undo history.
- Rejected manual Blur input beyond its current bounded writer range instead of silently clamping.
- Retained concise visible conflict text and exact numeric controls.

## GitHub commits
- Draft store: 7359ee4c5bdf521a2de6ed4e32ce21d99bf8d0fa
- Native UI: 33ec3314e86de0e6e54d5d95b2d51572ec25f968
- Guarded Fade writer: a713fb5b7d07963e67e8fa9e6e96c9a0658d3916
- JVM tests: 6cc61f954cc37784f1e4d11f191dfe468ecd1d26
- Android tests: b554af442d6197abc6ebc8fd385aee8b78af6821 and 0f30eead48cddf240e244a533ba20a284c5b19f3
- Bounded Blur and tests: 9db98c6de37c058358d6bfa024cb1b6c7eb13c79 and ade7f88069bc91a957af8d487ed56c0aeee523a6

## Verification
Source and test files are committed on main, not executed or native-accepted. Latest combined status had no reported checks. Android build, emulator, gestures, libass and real file round-trip remain pending.

## Governance
Searched Foundry for native Fade Blur session drafts and source guards and found no matching Case. Related prior Transform/Blur Case covers a different scope. Do not promote to Canonical.
