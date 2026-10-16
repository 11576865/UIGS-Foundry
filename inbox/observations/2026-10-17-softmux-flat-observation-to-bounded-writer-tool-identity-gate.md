# Observation: A flat source observation may navigate to a stronger writer, but must not become its edit authority

Date: 2026-10-17  
Status: **Observation / PR submitted, exact-head Chromium/native CI pending**  
Product: https://github.com/11576865/MKV-Fast-Muxer  
Implementation PR: https://github.com/11576865/MKV-Fast-Muxer/pull/159  
Superseded conflicting pre-R0 PR: #158 (closed; never merged)  
Authority: 2026-10-12 softmux Matroska theoretical 1.0, without new Canonical edits.

## Observed integration boundary

The object-centred UI has genuine `ffprobe`-derived flat Chapters and format-level Tags, but those fields cannot identify an arbitrary nested Matroska `ChapString` or `TagString` with its TargetUID/TagTargets structure. At the same time, the product already has a **separate**, independently reviewed byte-equal Matroska metadata text editor (`p2-matroska-inline-metadata-writer.js` and `p2-matroska-inline-metadata-ui.js`) with a strict EBML parser, raw byte preservation requirements and explicit consent. Letting a read-only source object offer a direct `Edit` would overstate what the shallow probe proves; forcing users to find and reselect the same File in an unrelated tool hides a legitimate interoperability path.

## Bounded observed implementation

PR #159 replays a small vertical slice onto successfully merged PR #157 main:

1. A selected **real scanned** Chapter or Tag observation offers `使用当前来源打开受限章节/标签工具`. The label and adjacent help state that no exact EBML writer field is mapped, even when a displayed name matches.
2. The source UI sends the exact ephemeral current `File` object, kind and observation ID through a cancelable local navigation intent. The production handler accepts it only if `sourceFile === videoInput.files[0] === scannedSourceFile`, the scan file-key matches, the unified imported-asset inventory still owns the same File under the selected source role, the observation ID exists in the current source projection, and no mux/batch is active.
3. Only on approval does the existing isolated P2 source File input rebind to that **same File instance** and fire its normal source-change handler. That invalidates prior candidate, review, field selection and save affordances, then **independently re-inspects EBML**. The UI navigates to the existing tool; no duplicate writable object model or new writer.
4. The user must separately select a real eligible `ChapString/TagString` field and explicitly approve the equal-UTF-8-byte modification; the original bounded writer still rejects unsupported structure and creates a new output copy only after its own structural checks.
5. The new browser E2E uses an actual source with chapters/tags, rejects a **forged distinct File with the same display name**, checks navigation and identity, and verifies there is no inherited writer consent or automatic save. The full native P2 writer test remains mandatory and separate.

## Reusable hypothesis

In a staged inspector→editor workflow, **navigation identity, observation evidence, writer capability and mutation authorization are four independent proofs**. A weaker read-only probe may be sufficient to show a route to a stronger independent tool, but the route must carry exact live source identity only. The stronger tool must re-establish field-level and structural authority from its own input bytes, rather than guessing from a flattened prior observation. Selection, review, write permission, previous successful output and saved-to-disk evidence must not be inherited through navigation.

## Evidence boundary / dedupe

Current evidence is committed code, exact-main replay and V8 syntax checks for three changed JS sources. The new PR #159 **has not yet completed exact-head Node/build/Chromium/native CI**; implementation maturity is not certified, and there is no new 57-scenario acceptance promotion.

Foundry search included `ffprobe flat chapter metadata TagTarget writer`, `source observation independent bounded writer exact File reinspection`, `read-only source object to edit tool transfer identity` and `metadata source rebind isolated editor not consent` and found no matching handoff-specific record. Related but different:
- `inbox/candidates/2026-10-02-read-only-source-inspection-must-not-inherit-downstream-gates.md`: read-only inspection availability should not require later execution prerequisites.
- `inbox/observations/2026-10-16-softmux-source-attachment-result-identity-freshness.md`: current source/plan freshness governs whether **completed output evidence** may be attached to a displayed object.
This new Observation covers **cross-evidence navigation to an independent writer**, not read-only access or completed-output badge projection. One PR is not enough to promote a universal Canonical rule.

Keep this status PENDING CI; update only with an independently observed exact-head verdict.
