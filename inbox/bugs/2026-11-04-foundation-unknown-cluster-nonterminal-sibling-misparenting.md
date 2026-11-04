# Bug: Foundation C/WASM adapter falsely admitted nonterminal unknown-size Cluster sibling as Cluster child

Date: 2026-11-04
Status: **Reproduced; fix implemented; latest exact-head CI pending**
Layer: Bug / implementation-specific, not Canonical
Product: 11576865/MKV-Fast-Muxer, [Draft PR #240](https://github.com/11576865/MKV-Fast-Muxer/pull/240), Issue #238

## Evidence, impact and precise attribution

The upstream BSD libMatroska2 EBML structural parser was reused through a product-authored machine-readable C ABI. For Matroska RFC 9559, both Segment and Cluster permit unknown sizes. The original bridge reconstructed parent scope from element start/end positions; it bounded an unknown-size Cluster by its Segment's end without independently rejecting a following top-level sibling.

A **native-recognized** fixture based on a real MKVToolNix-authored source was modified by a CI-only authoring script: the last Cluster was given an unknown size, and a valid top-level Tags master was placed *after* it inside a finite Segment. Both Track/Attachment structures remained available to native `mkvmerge -J`. The adapter's first Chromium implementation mistakenly returned **`inspected`** on this ambiguous shape and failed the explicit fail-closed gate. Exact run [#41837354731](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41837354731) failed at `Audit real unknown-sized Segment and CRC-protected attachments` with the test error `EDGE_CORRUPT_CRC_WAS_TRUSTED` (original generic negative-test wording; **this was not a CRC bug**). The problem is the project-owned C ABI ancestry reconstruction, **not evidence that the upstream library itself is intrinsically defective**.

The earlier positive [#41836661083](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/41836661083) demonstrated a genuinely **terminal** unknown-size Cluster that the Foundation-primary backend could inspect, while the legacy JS walker refused it; the nonterminal sample illustrates why terminal-only admission is essential. The test additionally observed fully valid nested Attachments/AttachedFile CRC behavior (2 scopes) and explicit inner-corrupt/outer-valid refusal.

## Remediation and policy

- C adapter now tracks when a direct-parent Master is an unknown-size Cluster; the recognized immediate-child ID set is restricted to the current Matroska Cluster schema (Timestamp, Position, PrevSize, SimpleBlock, BlockGroup, deprecated EncryptedBlock and SilentTracks, and CRC-32). A following Segment-level Tags/Attachments/Tracks/Cluster element cannot silently enter the unknown Cluster.
- **Void 0xEC deliberately excluded**, even though legal as a Cluster child, because an identically encoded Void after a size-unknown Cluster could be Segment-level and cannot safely prove a terminal Cluster boundary in this narrow integration. This is intentional fail-closed *subset support*, not a Matroska specification claim that Void is invalid.
- Machine-driven Chromium gates now use two independent negative cases (followed by Tags and followed by Void), plus the positive terminal unknown Cluster; the native `mkvmerge -J` reference must recognize each file. Positive attachments retain native `mkvextract` byte hashes.
- The existing parser remains the default, the Foundation-primary adapter remains explicit opt-in, and neither read status grants writer admission. No UI change.
- Future safe generalization requires upstream semantic/sibling-boundary evidence rather than another loosely assumed EOF rule. A reliable true parent scope oracle or conservative refusal is required before adding new arbitrary unknown-sized Cluster layouts.

## Remaining acceptance / Pending

At writing, exact patched product commit `e3b32199b7ecc9e4a75b3a2c8b4da2ee892236af` and its scoped + full product CI had not yet completed. Until those exact-head results are checked, status is **Pending verification** and no general retirement of the legacy path is allowed. When verified, update this Bug and the existing 2026-11-04 Matroska Foundation Case; do not modify Canonical.

**Dedup check:** searched the Foundry for unknown-size Cluster sibling/Tags misparenting and related Foundation C/WASM parent scope; no prior Bug with this concrete failure and exact native Chromium counterexample. The existing Foundation Case and older CRC Cases remain separate and are cross-referenced rather than duplicated.
