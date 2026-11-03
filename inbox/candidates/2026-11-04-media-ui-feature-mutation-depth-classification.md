# Candidate: Classify a media UI feature by its actual mutation depth, not its label

Date: 2026-11-04
Status: Candidate / documentation-grounded conceptual distinction; no product validation
Domains: interface-grammar, media-container-editing, user-intent, output-verification
Trigger: Owner asked how many apparent MKVToolNix features are actually simple parameter changes, naming conventions, or saved presets, after examining cover images as Matroska attachments.

## Observation and distinction

A UI command can carry substantial user meaning while implementing only a small change in storage. In Matroska, a cover image is an ordinary AttachedFile recognized by filename conventions, not a separate cover track; track name, language, default/forced flags, segment title and display dimensions are examples of header/metadata operations. Other commands, such as adding attachments, remuxing selected tracks, appending streams and splitting by keyframe-constrained timestamps, change the actual container topology and/or packet timeline. Some options adjust timestamp semantics without media re-encoding. A preset is saved application configuration rather than necessarily a Matroska feature.

Count or significance of product features must not be inferred from the number of buttons or backend flags. No quantitative claim about the proportion of MKVToolNix features was established.

## Candidate model

For a container-oriented workbench, consider associating each user-visible operation with:

1. User intent / affordance (e.g. “set cover”, “prefer subtitle”).
2. Underlying data operation: naming convention; stored metadata/flag; configuration-only preset; packet timing; object add/remove/reorder; stream copy/remux; media essence transformation.
3. Observable effect: container object/field change, player-dependent behavior, and actual media bytes changed or preserved.
4. Execution path: in-place header edit, full remux, physical attachment read/write, or re-encode; do not equate absence of re-encode with absence of structural mutation.
5. Evidence: output re-read and object/byte preservation tests appropriate to the claimed operation.

Suggested UI implication: specialized user intents can be presented directly while sharing a generic lower-level mutation engine, and the UI should not imply guaranteed player behavior for convention-driven metadata. Distinguish user-friendly semantic shortcuts from distinct storage objects or separate execution implementations.

## Sources and boundaries

- RFC 9559 §21: Matroska cover art is an Attachment with documented case-sensitive filename conventions; readers MAY use it.
  https://www.rfc-editor.org/rfc/rfc9559.html
- MKVToolNix official mkvmerge manual: metadata flags, track name/language, attachment names, remux/append/split and timing.
  https://mkvtoolnix.download/doc/mkvmerge.html
- MKVToolNix official mkvpropedit manual: certain track/segment properties can be edited without full remux.
  https://mkvtoolnix.download/doc/mkvpropedit.html

## Deduplication

Checked Foundry:
- inbox/candidates/2026-10-04-container-attachment-mutation-type-agnostic.md (generic attachments and safe mutation), overlapping narrower mechanism;
- inbox/cases/2026-10-04-matroska-generic-attachment-cover-image-acceptance.md (specific cover acceptance);
- inbox/observations/2026-11-03-matroska-image-attachment-demuxer-projection.md (actual EBML object vs demuxer projection);
- inbox/candidates/2026-10-03-requested-vs-realizable-edit-boundary.md (intent vs executable keyframe constraint);
- inbox/observations/2026-11-01-softmux-five-layer-product-identity-ambiguity.md (product identity and evidence separation).

This entry is limited to the cross-operation taxonomy of UI feature labels vs actual mutation depth. It is **not** a new universal law, a software implementation result, permission to simplify product scope, or a Canonical update. Future validation requires an actual MKV UI operation inventory mapped to commands, resulting EBML differences, and independent output checks.
