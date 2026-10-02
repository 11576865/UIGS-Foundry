# Cross-project Knowledge Inventory — Pass 5

Date: 2026-10-02

## ASS interaction grammar

Added **UIGS.INTERACTION.DISCOVERY_OVERLAY**. Preview picking is modeled as a discovery/interaction layer with explicit confidence and shared host semantics; it is not allowed to masquerade as renderer-backed glyph hit testing.

## CVS runtime ownership

Added **ARCH.RUNTIME.EXCLUSIVE_RESOURCE_OWNERSHIP**. A supervisor may stop only processes it owns. If another healthy runtime occupies the same exclusive resource group outside supervisor ownership, the correct behavior is a conflict/refusal rather than an implicit kill.

## HSR reusable state/update mechanisms

Added:
- **REL.CHECKPOINT.ROUTE_AND_INPUT_IDENTITY** — route identity plus per-record fingerprints gate reuse of paid translation work.
- **OPS.PROJECT.OWNERSHIP_AWARE_LIFECYCLE** — clone/delete behavior follows managed-vs-user-owned resource boundaries.
- **REL.UPDATE.CONFLICT_PRESERVING_PLAN** — new/existing/changed/variant/ambiguous update states remain separate and conflicts are preserved for review.

## Encoder remaining hardening

Implemented/verified mechanisms became Experimental:
- final APK native page/alignment verification;
- stable debug signing identity for replace-install testing;
- thermal-aware long-job progress.

Two documented policies remain Candidate because this pass did not locate matching implementation evidence:
- Android mediaProcessing timeout/background-budget handling;
- bounded FFmpegKit session/log retention.

This distinction is intentional: the Foundry must not turn a checklist item into a claim of implementation.
