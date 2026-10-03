# Bug: Invalid batch form input can silently disappear and broaden the recipe

Date: 2026-10-04
Status: Bug
Scope: batch editing / form validation / destructive scope / preview

## Symptom

A user can type an invalid value into an optional batch filter or transform field and still obtain a syntactically valid recipe in which that requested constraint/action has simply disappeared.

The dangerous case is an invalid filter: dropping the filter can broaden the affected set from the user's intended subset to many or all Events.

Examples in ASS Workbench Android's Batch pane included:

- malformed Raw ASS Regex filter → regex filter omitted;
- non-integer Layer filter → layer filter omitted;
- malformed duration bounds → bound omitted;
- invalid Regex replacement pattern → replacement action omitted;
- partially invalid timing-scale fields → scaling action omitted;
- invalid numeric override → override action omitted.

If other actions remain valid, Preview/Commit can therefore represent a materially different recipe from what the form visibly contains.

## Failure mechanism

Optional-field construction used patterns such as `toIntOrNull()?.let { ... }` and `runCatching { Regex(raw) }.getOrNull()?.let { ... }`.

Those are convenient parsers, but without a separate validity state they conflate:

1. field intentionally left blank; and
2. field present but invalid.

Recipe construction then treats both as “feature absent”.

## Mitigation implemented

ASS Workbench Android PR #95 now separates local form validation from recipe construction:

- blank optional fields remain absent;
- nonblank invalid fields produce an explicit batch preflight error;
- the expensive document scan is not run while local input is invalid;
- Commit remains unavailable until a current explicit Preview succeeds;
- malformed filters/actions cannot silently disappear into a broader/partial recipe.

Android regression coverage includes malformed Raw ASS Regex and invalid Karaoke parameters, both with unchanged canonical document.

## Reusable lesson

For destructive or bulk editors, **invalid optional input is not equivalent to omitted input**.

The form layer should preserve this three-state distinction:

- absent,
- present and valid,
- present and invalid.

Only the first may be silently omitted from the compiled operation. The third must block Preview/Commit or otherwise be surfaced as an explicit user decision.

## Provenance

- project: `11576865/ASS-Workbench-Android`
- PR: #95
- evidence level: concrete destructive-scope defect found during code review + fail-closed UI correction + regression coverage
- deduplication: searched UIGS-Foundry for invalid optional batch fields, silently omitted filters/actions, and broadened batch scope; no direct duplicate found

This Bug entry is evidence, not a Canonical rule.
