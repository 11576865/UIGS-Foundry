# Bug: Unknown cached media header could skip a Matroska preservation preflight

Date: 2026-10-13
Status: **Remediation verified by exact-head Chromium CI; historical risk confirmed in source review. General complex-MKV writer remains unsupported.**
Product: [MKV-Fast-Muxer PR #108](https://github.com/11576865/MKV-Fast-Muxer/pull/108)
Review evidence: https://github.com/11576865/MKV-Fast-Muxer/pull/108#discussion_r4254474086
Related existing Candidate: `inbox/candidates/2026-10-12-structured-container-preservation-gate-before-mutating-writer.md`
Related existing Bug: `inbox/bugs/2026-10-12-mkv-browser-remux-nested-chapter-and-target-tag-loss.md`

## Threat / causal source

The legacy mux start originally decided whether to run `inspectMatroskaPreservation(source)` by **the previous async filename/size-keyed header classification**:

`if (['matroska', 'matroska-webm'].includes(headerVideoIdentity.container)) ...`

If the first `File.slice().arrayBuffer()` read fails transiently, the cached container may be `unknown`, while the actual source is a valid MKV with nested ChapterAtoms and ChapterUID-targeted Tags. The condition then skips the structural gate instead of failing closed. A UI-only preview block cannot be treated as an authorization boundary because programmatic invocation or future adapters can call the execution function.

This is a code-review identified conditional bypass (P1), **not yet a completed independent red/green browser reproduction**.

## Submitted fix / acceptance requirements

- Re-read the **actual File's content header** inside the final executor authorization boundary. Reject unknown or changed identity before creating a new artifact. Do not trust a stale name/size/mtime identity cache.
- At batch preflight, reject unknown actual source container **before any job executes**, rather than `continue`-ing past it. The inner per-job executor still independently checks.
- Add a real Chromium adversarial case that injects exactly one initial File header-read failure on the independently authored P0 nested ChapterUID fixture, then confirms that the UI is blocked, programmatic dispatch to mux is refused and no artifact links appear.
- Keep the existing independent source fixture and result audit. An all-green regular mux suite alone does not establish that unknown-header bypass is closed.

Product PR #108 has patch and new Node/browser tests committed. **Exact-head CI Pending.** This single-project Bug does not amend Canonical.

## Reusable boundary

Security preflight selection itself must not be controlled by an earlier **fallible classification result** unless unknown classification is an explicit refusal. A result such as "unknown" is not evidence that the source belongs to a class exempt from safety validation. Enforce and test the rule at the final execution boundary, separately from UI disabled state.

## Verified remediation (2026-10-13)

Product [PR #108](https://github.com/11576865/MKV-Fast-Muxer/pull/108), exact tested head `c0ebc77bdbb1db23c6519b0e1d1dd970044b4dad`, merged `main@5b98af3af17269add441c7571d39009848b2e604`.

- [Node tests / Pages build workflow 38344211490](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38344211490) **success**.
- [Full Chromium E2E workflow 38344211420](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38344211420) **success**, including test-only forced mux invocation, independently authored nested-Chapter/ChapterUID-targeted source refusal, and an adversarial first-header-read error.
- The runtime authorization boundary now independently re-sniffs the exact source before choosing preservation behavior. If cached vs actual source container differ or either is unknown, execution is refused, not silently exempted. Batch preflight also refuses unknown source containers before any output.
- The browser UI now gives source-scoped pre-click readiness with blocked/pending/warning categories and generation/file-identity invalidation. This is not a claim that normal FFmpeg remux retains arbitrary nested chapters, metadata or unknown EBML.
- Initial E2E iterations found mislocated tablet assertions, same-source invalid-font recovery, and a disabled-button event that did not reach the executor. They were corrected while retaining independent writer and runtime checks; only the latest exact-head passing run is accepted.

The remediation is evidence-backed for the checked browser fixtures, not a formal universal safety proof. Keep Bug history and link to related Candidate; do not modify Canonical.
