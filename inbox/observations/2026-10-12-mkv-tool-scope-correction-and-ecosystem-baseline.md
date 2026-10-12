# Observation: Scope-correct a container tool before competing on generic mux breadth

Date: 2026-10-12
Status: Observation / design review and official-documentation comparison; no product implementation or user validation
Product: `11576865/MKV-Fast-Muxer`
Source state: product main `7781a4f410a9c6edb9a1f3d056091e6ace333cc4`
Related existing records:
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md`
- `inbox/candidates/2026-10-04-container-attachment-mutation-type-agnostic.md`
- `inbox/candidates/2026-10-04-container-compatibility-detection-wraps-mutations.md`
- `inbox/cases/2026-10-12-mkv-self-contained-subtitle-rendering-acceptance.md`

## User clarification and correction

The user explicitly distinguished general Matroska resource assembly from an ASS subtitle authoring tool. The desired output includes the possibility of an attachment-only Matroska containing a single still image and no media track, **not** automatically converting that image into a static video stream. The user explicitly did **not** request in-app ASS text/style editing, editing the bytes of embedded fonts, or automatically replacing source subtitle tracks as a core authoring workflow. Those are outside this product and can belong to the separate ASS project. They do want evidence that the planned/released MKV's subtitles can use retained in-container fonts rather than accidental system-font fallback.

## Official ecosystem baseline

- Matroska RFC 9559, §6.1: Info is the only REQUIRED top-level element; playable files additionally need Tracks and Cluster. The specification distinguishes valid non-playback containers from playable media. §21: attachments may include pictures, fonts, reports and arbitrary ancillary resources. https://www.rfc-editor.org/rfc/rfc9559
- MKVToolNix is a long-established Matroska mux / inspect / extract / property-edit reference family, not an absent market feature. https://www.matroska.org/downloads/mkvtoolnix.html
- `mkvpropedit` can add, replace, update and delete generic attachments and change properties without complete remux; its in-place edits have different safety/transaction semantics from immutable-source export. https://mkvtoolnix.download/doc/mkvpropedit.html
- LosslessCut provides multi-file track combination/extraction and contextual stream editing; MKV Muxing Batch GUI supports batch audio/subtitle/attachment/chapters; gMKVExtractGUI specializes in extraction. https://github.com/mifi/lossless-cut ; https://github.com/yaser01/mkv-muxing-batch-gui ; https://github.com/Gpower2/gMKVExtractGUI
- FontCollector has `--use-ass-in-mkv` and `mkvfontvalidator`, showing that embedded ASS/font validation and font collection are not globally unprecedented; renderer-isolated *visual* confirmation remains a distinct unverified differentiator. https://github.com/moi15moi/FontCollector

## Reusable design lesson (tentative)

When a narrowly differentiated product broadens to a general container/document domain:
1. First map the normative format structure and distinguish representation from current writer capability and player support.
2. Benchmark mature general-purpose ecosystems **before** inventing their basic domain verbs.
3. Keep an explicit ownership boundary: general container assembly and auditing vs specialized embedded-content authoring.
4. Preserve differentiators as a coherent end-to-end user workflow rather than claiming novelty for individual commodity operations.
5. Define a small comparative fixture matrix and report untested capabilities as unknown. Don't infer superiority from repository features or screenshots alone.
6. Research APIs, interfaces, workflows and test contracts for lawful inspiration; verify component licenses before reusing source. Do not make a visual skin of a mature tool without a distinct user job.

## Known limitations

Source/documentation comparison only. Does not establish competitor UX quality, the claim that MKV-Fast-Muxer is best-in-class, an attachment-only mkv writer implementation, or exact font/render compatibility. The product's PR #74 merges a composition-first UI projection but does not upgrade the general video-centric mux executor. A one-file attachment-only output should be treated as a standalone specification, writer and reader acceptance test.

No Canonical promotion.


## Further normative distinction: document validity, filename profile and writer support

Follow-up analysis on 2026-10-12, based on current official specification:
- RFC 9559 §6.1 requires `Info` as the only REQUIRED Matroska Segment top-level element. For a **playable** Matroska document it additionally requires `Tracks` and `Cluster`. This leaves room for a syntactically conforming non-playback Segment with attachments and no media tracks, contingent on observing the complete EBML/Matroska constraints. https://datatracker.ietf.org/doc/html/rfc9559#section-6.1
- The Matroska FAQ associates `.mkv` with at least one video track, `.mka` with audio-only, `.mks` with subtitles-only, and `.mk3d` with stereoscopic video. There is no dedicated, documented conventional extension for an attachments-only Matroska. Therefore output filename convention is a **third** distinct axis beyond structural validity and writer/reader support. https://www.matroska.org/faq.html
- The product currently rejects a main source without a video stream and uses `mainInputPath` as its mux execution anchor. Neither deleting this gate nor turning a single image into video should be presented as an attachment-only implementation. That scenario requires an independently tested writer and at least two independent readers or structural validators.
- The attachment class is semantically generic but optimized for ancillary resources connected to multimedia; the project should not infer that Matroska is a universal archive replacement.
- When product direction is not yet selected, keep candidate routes as *options*, not a Canonical decision or evidence-backed implementation assertion.

Potential cross-project applicability: document formats with independently varying structural validity, output-profile naming and runtime implementation support.
Evidence level: RFC/official docs plus static project code; no attachment-only output fixture executed.

## 2026-10-12 R-02 experiment and general target-model provenance (Pending external audit)

Product [Draft PR #88](https://github.com/11576865/MKV-Fast-Muxer/pull/88), initial head `c267e639ef6058ceb1c1ca0f7401ba8a24af794f`, implements the **model-level** correction: a read-only `projectMatroskaTarget` can describe attachment-only (one PNG, zero video/audio/subtitle Tracks), audio-only, metadata-only, empty and normal video composition; `resolveLegacyTargetCapability` refuses non-video writes under the current video-rooted FFmpeg adapter **without declaring the Matroska format itself invalid**. Seven Node tests were submitted; exact head full CI pending at intake.

A deliberately **test-only** EBML fixture generator constructs a Matroska Header and Segment with Info + exactly one PNG AttachedFile (no Tracks/Cluster). The independent acceptance path uses `mkvmerge -J` to inspect zero Tracks/one attachment, `mkvextract` to compare the attachment's extracted SHA-256 with the original PNG, and logs FFprobe acceptance/rejection separately. CI runs this as a **non-gating** experiment that always uploads JSON evidence; a green CI job is not an R-02 success claim. Normative reference: RFC 9559 §§4.5, 6.1, 21. The experiment does not establish production writer support, cross-player compatibility, or full conformance until independent results are inspected.

This updates an existing Observation on general Matroska and no-video semantics, not a new Canonical rule. Follow-up must inspect the R-02 report and update evidence status; unresolved #77 nested Chapter/Tag loss remains a separate preservation risk.
