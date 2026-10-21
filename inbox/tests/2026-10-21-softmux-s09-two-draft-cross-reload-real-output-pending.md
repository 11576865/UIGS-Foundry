# Test (Pending CI) · S09 two distinct source/external drafts across browser reload

Date: 2026-10-21
Status: **Test candidate submitted; exact-head CI Pending. NOT accepted; NOT Canonical**
Product: `11576865/MKV-Fast-Muxer`
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/168
First exact product head: `cf47c3e7edfd0bd046c642f0c2a63fed44d8048c`
Reference: `docs/softmux-1.0-product-acceptance-contract-20261020.md` S09.

## Deduplication
- `inbox/tests/2026-10-15-mkv-external-checkpoint-sha-sidecar-rebind-cas-undo.md` already covers external track checkpoint SHA/sidecar rebind and consent/undo at its own boundary.
- Historical source-track detached-draft replay / original attachment case tests are already in product `scenarioVerifiedDetachedTrackRestore` and source/attachment recovery. No new general Candidate is proposed.
- This newly proposed **integration acceptance** binds *both existing portable draft types* to the same real user workbench across a literal page reload. It does not introduce a new merged project schema or general permission authority.

## Submitted test path
1. Real Chromium, current object workbench; public intake of `source-with-attachments.mkv` and `external.flac`. Edit a real scanned original audio-track title via Inspector, and external FLAC title via its existing owned editor.
2. Export the separately scoped original-source ContainerProject draft and external metadata checkpoint; verify source SHA-256 and actual edit intent.
3. Reload the actual page. Verify no File permission/selected source and no automatic consent. Import both JSON files; neither is permitted to restore File handles or authorize execution.
4. Re-import both original resources from current public UI; verify no silent metadata application. Independently SHA-256 verify/authorize source draft, then SHA-256 verify/authorize external checkpoint. Require separate confirmation checkboxes.
5. Verify frozen executable plan contains both actual titles; generate a real output Matroska, run independent native `ffprobe` on both audio-stream titles, and verify source bytes not modified.
6. Upload two JSON drafts + actual MKV + source-bound output receipt as one exact-run CI artifact.

## Explicit limitations
- No single atomic all-objects project export/import is claimed; existing implementation has **two** independent user-confirmed portable drafts.
- No browser File grants, arbitrary Chapters/Tags/UID edits, running job, persistent undo history or future device support is reconstructed by JSON import.
- UI change in `src/softmux-10.14-workbench.js` displays these restrictions inside the real recovery disclosure.
- S09 full contract additionally requires negative conflict tests, supported undo/redo scope and further device/UX acceptance. This PR **alone** cannot make S09 fully PASS.
- On CI failure capture exact assertion/error before any correction. No Canonical mutation from one fixture.
