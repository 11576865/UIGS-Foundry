# Bug: Rehosted UI subtrees can invalidate ancestor-scoped state updates

Status: **Bug / reusable UI architecture failure**
Date: 2026-10-03
Project evidence: `11576865/Quick-Automatic-Hardsub-Encoder`, PR #38

## Failure

A shared “audio and container” control block is physically rehosted between different mounts depending on the active hard-sub control strategy.

The copied-audio warning was initially updated through:

```js
section.querySelector('#taskAudioPlaybackWarning')
```

This worked while the output-policy subtree remained inside `section`. In Guided hard-sub mode the whole output-policy subtree is moved to a sibling shared mount. The element still exists and remains visible, but it is no longer a descendant of `section`.

As a result, later Copy → AAC changes called the update routine, but its ancestor-scoped lookup returned `null`. The warning stayed visible even though the selected policy had changed.

The same architecture also means form-level event bubbling cannot be assumed once a form-associated control is physically rehosted outside the form, even if its `form` attribute keeps it in `form.elements`.

## Reusable rule candidate

When a live UI subtree can be reparented / portaled / rehosted:

- do not use its former ancestor as the authoritative query root after rehosting;
- retain a stable element reference, query from the movable subtree itself, or use an invariant global root;
- distinguish **form association** from **DOM ancestry**: a control can belong to a form semantically without bubbling events through that form element;
- attach event handling to the control itself or to an ancestor that remains invariant across every host;
- tests must exercise state changes both before and after the subtree is moved, not only verify that the moved UI is visible.

A useful model is:

```text
logical ownership != DOM ancestry
form association != event propagation path
rehostable subtree -> stable references / stable event root required
```

## Fix evidence

PR #38 binds warning lookup to the movable `outputPolicy` subtree rather than the original `section`, and observes shared audio-policy changes from a stable document-level event root.

Browser UI smoke specifically verifies Guided hard-sub after the output policy has been rehosted:

```text
Copy -> warning visible
AAC  -> warning hidden
Copy -> warning visible again
```

The PR merged as `2c4dea6a2e634a7b0ea0bb34cd0b87858d89fa77` after frontend and Windows smoke checks passed.

## Scope

Applicable to portals, responsive reparenting, shared control decks, mode-dependent mounts, movable inspector panels and any interface where one logical component is physically moved between DOM containers.

This is Bug / Candidate-level evidence only. Do not promote to Canonical from this single implementation.
