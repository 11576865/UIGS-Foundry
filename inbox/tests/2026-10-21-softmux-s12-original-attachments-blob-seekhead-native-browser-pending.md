# Test · S12 original Matroska Attachments byte-range reinsertion after independent A/V mux

Date: 2026-10-21
Status: **Scoped native 128/256MiB + browser File/Blob 128/256MiB PASS on prior exact research heads; final safety-negative regression exact head Pending; no production authorization; NOT Canonical.**
Product: `11576865/MKV-Fast-Muxer`
Research PR: https://github.com/11576865/MKV-Fast-Muxer/pull/175
Latest head at intake: `a3ddc6a7f897706876adeb2349d5f6553b726d44`
Product main baseline: **softmux 0.1027.0** (unchanged).

## Deduplication and distinction
- Reuses `src/ebml-crc32-bounded.js` (CRC-32) and code/evidence patterns in previous Foundry `inbox/cases/2026-10-14-mkv-nonfinal-attachedfile-relay-offset-evidence.md` and `inbox/cases/2026-10-14-ebml-crc32-nested-attachedfile-attachments-writer.md`. It is **not a new generic Matroska writer rule**.
- The existing `inbox/tests/2026-10-21-softmux-s12-genuine-large-mkv-wasm-envelope-pending.md` establishes real source capacity and controlled 128/256MiB direct-FFmpeg.wasm original attachment failures; this separate Test asks whether an alternative **source original Attachments EBML master byte-range** can be reinserted after AV+new-subtitle mux without passing the original raw attachment streams into the mux.
- A previous bounded append-one-attachment research module (`existing-mkv-append-attachment-candidate.js`) has a different source shape: initial MKV contains **no Attachments** and adds one new attachment to the *same* preserved source. This experiment uses **existing original Attachments** and an independently remuxed **no-original-attachments** output. No claim of overlap in authorized domains.

## Submitted research mechanics
- Only a single finite Segment/valid Matroska structure with one original Attachments master and no remuxed Attachments. Remuxed output must expose a first SeekHead with valid CRC-32 and adjacent Void reservation. No original source Chapters or Tags accepted; no source Segment CRC, unknown-size Segment, unsupported pre-Segment layout or changed-size SeekHead slot. Experimental parser input budget ≤340MiB, **not a user size cap**.
- The source's complete **original Attachments master EBML byte span** is preserved using `original.slice(start,end)`. Reinsert into a new `Blob` after the remuxed Segment body. Exactly rewrite fixed-width Segment size, same-span SeekHead+Void, `SeekID=Attachments` and `SeekPosition`, and recompute SeekHead CRC using the project's existing crc32IEEE/ebmlCrc32LE code. Other remuxed Segment children retain absolute positions. No large original FileData materialization into JavaScript arrays in the reinsertion path.
- Research output explicitly has `authorization='NONE_RESEARCH_ONLY'`; code is under `research/` and standalone test scripts, not product UI/FFmpeg executor/batch. Native-reduced baseline may already have lost source metadata; therefore strictly refuse original Tags/Chapters in this research class.

## Real native source + detached mux + output proofs
- First narrow native [CI #39612797576](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39612797576), head `e99140160dca669acc2664107213ae94a05b222f`: **PASS** for two small original attachments, FFmpeg no-attachment remux plus new subtitle, SeekHead+CRC repair; actual candidate 207,637 bytes; independent ffprobe, mkvmerge, mkvextract and full original payload SHA.
- Explicitly generated REAL, physically written random original attachments (not `truncate`/sparse). Research head `54cd86aa0d27dc35910c014530403e876acb977c`, [native CI #39628804745](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39628804745): all three large native jobs **PASS**:
  - 128MiB = 2×64MiB originals → 134,261,524-byte native output.
  - 256MiB = 2×128MiB originals → 268,479,253-byte native output.
  - 256MiB = 4×64MiB originals → 268,479,389-byte native output.
  - Every positive job: physical source native probe; FFmpeg only A/V + new SRT with `-c copy`; Node 22 `fs.openAsBlob` on actual source/base (disk-backed), `Blob.slice` original Attachments reinsertion and streamed new output, ffprobe/mkvmerge attachment inventory, native extraction and each complete SHA, original full source SHA unchanged. Large files ephemeral on runner; small receipts archived.
- Independent **actual Chromium File/Blob** [CI #39629839822](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/39629839822), head `6e37807cd69d6992c2f7aab5207d8609f8f0c2cc`: two **browser jobs PASS** with real `File` inputs, `Blob.slice`+object URL download:
  - 128MiB 2×64MiB → downloaded 134,261,524-byte output.
  - 256MiB 4×64MiB → downloaded 268,479,389-byte output.
  - Post-download independent native video/audio/subtitle/attachments plus per-part full SHA and original source digest unchanged.
  - **Limitation**: the *no-attachments media remux baseline was produced by native FFmpeg*, not browser FFmpeg.wasm; this does NOT close the original large-attachment workbench execution path or user save.
- Following new no-silent-metadata-loss fail-closed check, the original small test source contained real FFmpeg-generated Tags. Explicit source Tags/Chapters refusal was correct but caused old negative test to fail for the earlier-than-expected refusal code. The small fixture was rewritten using native mkvmerge with `--no-global-tags --no-track-tags --no-chapters` and a separately authored **real Tagged original** rejection check. A further safety-preserving ordering adjustment first rejects missing/duplicate original-attachment shape before Tag/Chapter graph checks. Final head `a3ddc6a7f897706876adeb2349d5f6553b726d44` **Pending exact-head CI** at intake. Prior green large jobs remain valid *for those exact commits* only.

## Remaining gates
- Real Chromium **FFmpeg.wasm** mux that excludes original attached streams, then browser `Blob` reattachment and independent native output audit for the same 256MiB source. Current browser test never ran FFmpeg.wasm.
- Source Tags, Chapters, TagAttachmentUID / ChapterUID target graph, unrelated CRC masters and Cues/SeekHead diversity must be independently proven or refused. The controlled fixture forbids source Tags/Chapters, not universal metadata preservation.
- Research-only cap, no full-source JS array, no product dispatcher, no 1.0 S12 overall acceptance, no tablet/realistic long film/direct persistence claim.
- Only after accepted exact-head binary outputs and negative-matrix evidence could a bounded Candidate be considered. Never auto-promote Canonical.
