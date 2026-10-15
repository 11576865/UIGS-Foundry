# Observation: Contextual object navigation must confirm the destination actually accepted the source object

Date: 2026-10-16
Status: Observation / direct-main bounded implementation; current-head Chromium E2E not yet independently confirmed
Project: https://github.com/11576865/MKV-Fast-Muxer
Product release increment: 软封0.1015版本

## Source

In the developing object-centred workbench, an observed Matroska attachment can offer "定位来源附件编辑器". The first UI implementation fired a CustomEvent and immediately navigated back to the Tracks section whether or not the main integration found that source's real editor. This falsely implied success when source authorization, exact File identity, imported role, or real target lookup failed.

Change in `main`:
- UI sends a bubbling **cancelable** event carrying only the scanned source attachment index; it does not create a second editor or mutable attachment object.
- Real integration verifies actual File binding/scan and finds the matching existing ContainerDocument composition target; only after handling the operation does it call `event.preventDefault()`.
- Caller checks `event.defaultPrevented`. On rejection, it **stays in context and explains the inability to locate a verified editor object**, rather than silently switching tabs.
- The same development increment corrected source-observation selection to remain stable when the exact same File's properties change, and invalidate if the File object changes, even when name/size/mtime match.
- Product/reports version authority was unified separately, consistent with existing version-vector candidate.

## Transferable insight

A view transition after a contextual command should be contingent on **acknowledged command acceptance**, not merely that an event was dispatched. Preserve current object and draft context on rejection. Exact resource identity checks belong to domain-boundary handlers. An accepted view transition is not proof of a completed write; saving and output verification must remain separate.

## Dedupe / authority

Existing `inbox/cases/2026-10-14-mkv-external-assets-live-domain-file-identity-and-stale-form-epoch.md` already covers general exact File identity: do not duplicate that candidate. The `inbox/candidates/2026-10-15-version-vector-and-atomic-ui-cutover-gate.md` covers version vectors; not amended. This observation is specific to acknowledgment semantics for UI-to-domain navigation. It is not a Canonical rule.
