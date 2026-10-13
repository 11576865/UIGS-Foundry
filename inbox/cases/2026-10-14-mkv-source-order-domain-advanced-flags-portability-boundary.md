# Case: source-track ordering and advanced flags need one live authority; portable replay is a separate contract

Date: 2026-10-14  
Status: **Case; product PR submitted, exact-head Node/build/Chromium Pending**  
Source: [MKV-Fast-Muxer PR #129](https://github.com/11576865/MKV-Fast-Muxer/pull/129), stacked on [PR #128](https://github.com/11576865/MKV-Fast-Muxer/pull/128)  
Source commit: `75cfcb3e945d39b2c79ba525ecf9298745b0d061`

## Context

The earlier live-source owner Case `inbox/cases/2026-10-14-mkv-live-domain-track-authority-with-legacy-mux-projection.md` covered only source audio/subtitle include, title, language, Default and Forced. Actual source inspector and legacy controls still directly mutated Original, Commentary, Hearing Impaired and source order. Those edits could bypass the narrow immutable domain owner and create drift.

## Experiment: one session authority, two distinct restoration contracts

- Extended the live immutable `ContainerProject` field set for **source audio/subtitle** Original, Commentary and Hearing Impaired booleans. The same user-facing controls and reset operations now use the fail-closed domain transaction; source exclusion clears all five disposition flags as a unit.
- Both existing track-up/down arrows now perform a two-object immutable **within-kind** source order swap before materializing the same order change into the old FFmpeg execution-facing projection. Exact source File, current scan, unique numeric positions, included peer, expected relative order and preserve-all mode are validated.
- For detached draft export/import, advanced flag changes have scan baselines and coherent derived `set-attribute` intents. They can pass strict JSON import, source byte commitment, old-field conflict comparison and *explicit* verified replay/guarded undo.
- **Intentional scope limit:** although a moved track produces the correct current-session mux ordering, portable untrusted JSON has no separately proven reorder replay. The product therefore explicitly warns on export that order changes cannot be recovered on later draft import; `objects[].order` is not a grant to mutate the current editor or media. No false promise that “all work is saved”.
- Chapter/Tag preservation #77, attachment relation graphs and general EBML writer remain unmodified.

## Evidence

- Targeted in-isolate run of real source modules passed three advanced edits, two-track order swap, typed project serialization, strict project import and internal chain audit. A second run passed SHA-style proof-shaped source conflict preview, explicit prepared replay and correct advanced-field restoration without writing media.
- Submitted Node regressions include full flags, exclusion side effects, same-kind order moves with excluded peers, duplicate/external order drift, source File drift, and imported advanced flag replay.
- Existing real Chromium multi-track MKV scenario was extended: audio movement and advanced inspector/legacy controls lead to actual MKV; independent `ffprobe` checks the output; exported JSON must encode advanced intents and the UI must disclose order nonportability.
- Static JS syntax checks passed for changed files; **exact-head full CI Pending**. The feature must not be labeled merged or validated on devices.

## Reusable insight / deduplication

This Case extends, rather than repeats, the prior [live domain Case](inbox/cases/2026-10-14-mkv-live-domain-track-authority-with-legacy-mux-projection.md). Separating session-local executable state from **portable, conflict-checked recovery** prevents migration work from making unsupported durability promises. An edit being domain-owned and successfully reflected in final media does not establish that every part of the edit can later be securely reconstructed from a detached document.

Record at Case level only; do not promote a single implementation into UIGS Canonical. Reassess after exact-head CI, independent media evidence and a verified reorder replay design.
