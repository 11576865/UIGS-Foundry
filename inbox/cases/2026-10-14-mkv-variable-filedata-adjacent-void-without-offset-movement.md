# Case: Adjacent reserved EBML Void permits a strictly bounded variable-length attachment edit without moving any original parent or media offset

Date: 2026-10-14
Status: **Submitted P0/P2 implementation; full exact-head real-browser/native-source audit Pending**
Source: [MKV-Fast-Muxer PR #137](https://github.com/11576865/MKV-Fast-Muxer/pull/137)
Evidence: [Actions 38538687371](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38538687371) (Node and Vite already green at initial checkpoint, Chromium Pending)
Classification: Case, not Canonical.

## New distinction from existing Case

The separately [merged, real-output-verified existing MKV equal-size attachment replacement](https://github.com/11576865/UIGS-Foundry/blob/main/inbox/cases/2026-10-14-mkv-existing-attachment-same-size-filedata-preservation.md) works only when FileData size remains unchanged. A conventional variable-length replacement would invalidate downstream byte offsets and possibly parent element size headers, SeekHead/Cues, CRC and UID-linked semantics. But there is a narrow independent source layout: an original `AttachedFile/FileData` is **immediately followed by an actual original `Void` child in the same AttachedFile**. This gives a source-owned local byte budget.

## Candidate bounded operation

A new FileData (with the original size-VINT width) and adjusted trailing valid Void can occupy **exactly** the original combined FileData+Void interval, even when payload length changes. The change never moves any preexisting EBML child outside the two-element interval and never rewrites parent AttachedFile, Attachments, Segment or EBML header size bytes. This class has different requirements from generic structural edits and from adding a new top-level Attachments master in pre-Info Void.

A source/target acceptance gate must verify current exact File object and selected FileUID, complete TagAttachmentUID target graph, absence of any target referencing the mutated AttachmentUID, well-formed Attachments/AttachedFile child walk, source and candidate byte hashes, original FileData size width and target offset, enough adjacent Void budget, valid leftover Void and no CRC coverage of changed bytes. Unknown top-level EBML, non-unique UID, unsupported unknown sizes and source changes refuse. A detached plan or similar filename never inherits File access.

Output evidence is *not* generic permission from the existing raw byte comparator; it remains `approvedToWrite:false`, since broader Matroska compatibility is not proved. The verified **bounded operator** must additionally compare every original top-level protected byte commitment, exact offsets, all other original FileUID/metadata/FileData, source prefix and suffix outside the two-element interval, native independently extracted Chapters/Tags, and all stream packets/timestamps.

## What is actually submitted

The project branch integrates a real workbench review UI, a bounded custom EBML child-reader and same-span writer, original-source/payload digests and output verification, adversarial Node tests, and a full real Chromium scenario. The real fixture originates with MKVToolNix/mkvpropedit and an *explicitly test-only* transformation of the original FileData field to install valid internal Void without shifting outer elements. Native MKVToolNix must read that modified source, and native mkvextract/ffprobe must validate the browser-produced downloaded MKV before any success claim.

**At creation, complete external CI not yet green; pending proof.** A green Node suite or synthetic fixture does not suffice. Scope remains <=60 MiB source, <=4 MiB replacement and an original adjacent Void with sufficient size-VINT capacity; this neither fixes general #77 FFmpeg remux loss nor delivers a full variable-length/CRC/UID target rewriter.

## Reusable (evidence-qualified) methodological observation

Classify writer capabilities by *exact source structural locality and protected-byte proof*, not merely by the business verb “replace attachment.” Some byte-length changes can remain local with source-owned reserved space and others cannot. UI review should distinguish genuine source-specific eligibility from a generic claimed writer capability. This record is a testable Case, not a normative update.

## Deduplication

Foundry search for `variable FileData reserved Void adjacent AttachedFile Matroska`, `non-remux in-place EBML Void offset preservation`, and `P0 P2 variable length attachment content reference graph` found no direct duplicate. The prior Case covers equal-size FileData and the older no-edit case covers preservation plus *new* Attachments in top-level reserved Void. This new Case tracks a different hierarchical source layout with new semantics. **Do not change Canonical on this single work item.**
