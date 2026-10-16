# Test: Finished-MKV attachment FileData verdict must reject a malformed audit receipt

Date: 2026-10-16
Status: **Test Candidate — implementation committed on product main; exact-head full Chromium CI pending**
Product: https://github.com/11576865/MKV-Fast-Muxer
Product increment: 软封0.1018版本
Files: `src/source-attachment-delivery-evidence.js`, `tests/source-attachment-delivery-evidence.test.mjs`, `src/softmux-10.14-workbench.js`, `tests/e2e/browser-mux.e2e.mjs`

## Prior lesson and distinct gap

Existing Foundry `inbox/observations/2026-10-16-softmux-source-attachment-result-identity-freshness.md` established the three axes **object identity, bounded proof scope and freshness** for projecting independently verified MKV results into live UI objects. It did not verify that the *input proof record itself* carries a complete self-consistent audit type and count.

The previous projection accepted any truthy `sha256` and positive `byteLength` in a matching `observations` array. A record claiming an arbitrary short digest, incorrect `verified` count, a different type of audit, or an unavailable whole-audit status could still produce an object-level `filedata-verified` result if the names matched. This is an **evidence-interpretation bug**, not proof that an attacker can forge the actual trusted browser execution; textual metadata validation is not cryptographic authentication.

## Bounded 0.1018 correction

- Require the existing independent source-to-final-MKV `FileData` auditor's declared evidence and scope, valid pass/warning overall audit state, coherent verified/total/observed counts, a complete 64-hex SHA-256, and a positive safe-integer byte length.
- Even with that record, match a single scanned original name and a single intended final output name against the actual output attachment inventory; preserve "unavailable" when identity or inventory is ambiguous.
- Do not escalate to `FileUID`, TagTargets, unknown EBML preservation, or actual disk save proof.
- Return granular machine-testable `reasonCode` values for no inventory, ambiguous identity, untrusted/incoherent receipt, unverified observed payload, or failed overall structural audit; show those explanations within the existing object inspector.
- Focused JavaScript execution ran the updated test bodies (10/10 including source parsers) successfully; full Node/Vite/Chromium workflow for 0.1018 remains unconfirmed. E2E extends the already real MKV selective-attachment/rename test to assert that the object UI displays the complete independently recovered digest and that the excluded source only receives a scoped inventory-absence claim.

## Reusable falsification gate

A global green indicator, a plausible source/destination name match or a string called `sha256` cannot authorize an object-specific verified badge. The proof schema, measurement scope, digest format, count conservation, and object identity must agree. A genuine multi-object audit may be globally warning while one uniquely observed attachment's digest is still independently verified; do not discard correct per-object evidence or convert other unresolved objects into success.

## Dedupe and evidence status

Compared with existing 0.1017 per-object freshness observation and 2026-10-12 scoped independent Matroska oracle Case. This Test adds **malformed-receipt negative fixtures and UI reason-code assertions**, not a new Canonical rule. Exact-head full GitHub Actions results were not retrievable through the available commit-status interface at intake; remain pending.
