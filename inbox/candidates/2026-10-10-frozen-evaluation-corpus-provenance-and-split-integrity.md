# Candidate: Freeze evaluation corpus provenance and split/reference identity before cross-engine comparisons

Status: **Candidate** (not Canonical)
Date: 2026-10-10
Source project: `11576865/Character-Voice-Service`
Source PR: https://github.com/11576865/Character-Voice-Service/pull/14
Source revision: `b3c539923986bf09a83943c8a9fcd7c071644825`

## Observation

A model registry and an evaluation-decision registry do not by themselves establish a reproducible voice-quality benchmark. Without an explicitly curated, content-addressed corpus and held-out partitions, engine or checkpoint comparisons can unknowingly reuse training/test audio, silently change reference prompts, or compare different source recordings.

In CVS's first dataset-freeze slice, source records explicitly distinguish ORIGINAL WAV and manually reviewed text, keep stable sample IDs and relative paths, and freeze WAV/transcript SHA-256 alongside split membership and reference-pool participation. The manifest is canonically fingerprinted; verification rechecks source WAV hashes. Audio is not modified or copied into the public repository.

## Reusable hypothesis

Before model/engine comparison is interpreted as evidence, make the evaluation inputs independently reproducible:

1. Treat original input identity, transcript provenance and derived/synthetic output as separate domains.
2. Freeze the exact sample inventory and train/dev/held-out-test membership rather than generating a new random split for each run.
3. Model reference prompt membership separately from dataset split: reference examples can come from non-test train/dev samples, but held-out test audio must not become a prompt.
4. Reject source audio duplication by content hash (not merely path); report repeated text across partitions separately from audio duplication.
5. Bind downstream evaluation records to the dataset fingerprint, selected reference IDs and model/runtime generation revision before promoting or comparing results.
6. Keep source assets private and immutable; manifest creation and verification must never rewrite source WAV.

## Evidence and limits

- CVS PR #14 adds the freeze/verify CLI, a deterministic manifest schema, explicit reference roles and 14 targeted local regression tests.
- The local tests passed; GitHub CI on the PR is Pending at submission. No private 400-clip dataset was accessed, no benchmark was executed, and no audio quality/accuracy gain is claimed.
- This is a single-project engineering implementation and a reusable **Candidate**, not sufficient evidence for Canonical promotion.

## Dedup check

Repository search on 2026-10-10 for benchmark dataset, evaluation corpus, split leakage, dataset fingerprint and provenance did not find an equivalent existing Candidate. Related asset-provenance and input-identity records are adjacent but do not cover frozen evaluation partitions/reference contamination.

## Follow-up implementation evidence — 2026-10-10

- CVS [PR #15](https://github.com/11576865/Character-Voice-Service/pull/15) is stacked on PR #14 and implements this Candidate's previously proposed downstream evaluation linkage.
- v1.1 evaluation records declare an immutable `model_revision`, opaque `generation_revision`, frozen `dataset_sha256`, complete held-out test IDs and one served voice reference mapped to a non-test source item.
- The promotion gate rejects schema v1.0 records (retained for historical reads), missing/stale manifest fingerprints, wrong model revisions, incomplete held-out coverage and reference/test contamination.
- Cross-project nuance: a `generation_revision` derived from a chosen reference must not be reused across multiple distinct reference choices. Current v1.1 intentionally uses one reference per evaluation record.
- Targeted regression tests and source changes are committed; CI and real-audio/real-device acceptance remain **Pending**. This is **declared provenance consistency**, not attestation of generated audio quality.
- The entry remains **Candidate**. This is follow-up evidence for an existing hypothesis, not an automatic Canonical promotion or a second duplicate Candidate.

## Runtime evidence implementation — 2026-10-10

CVS [PR #16](https://github.com/11576865/Character-Voice-Service/pull/16) adds a bounded synthesis runner, stacked after dataset freezing (#14) and the evaluation provenance gate (#15).

- **Declared reference mapping vs live reference identity:** a frozen mapping from `reference_id` to a reference corpus item does not by itself prove the engine is using the matching bytes. The runner uses a protected local CVS endpoint and checks the **live reference WAV SHA-256** against the frozen source hash before any generation.
- **Run identity fence:** pin immutable model revision, opaque generation revision, voice/reference, runtime/binding identity, dataset SHA and current output hashes. Per-sample resolve and returned speech headers must agree with the pinned identity. Resume rejects input, live reference, runtime or prior artifact drift.
- **Measurement is not evaluation:** valid output PCM, HTTP success, elapsed seconds and real-time factor are **generation-path evidence**, not correctness of speech, voice similarity, naturalness or promotability. Output is explicitly `quality_evaluation: not_performed`.
- **Isolation:** local loopback-only generation and admin token transport, sequential single writer, exclusive output artifacts and durable per-item checkpoints. A failed sample leaves partial—not successful—status.

Evidence: 18 local mocked-HTTP tests passed and source/CLI/docs were committed. Full CVS CI and real GPT-SoVITS/IndexTTS runtime or private original WAV acceptance are **Pending**. No Canonical promotion.

Dedup: the prior Candidate already covers frozen corpus and reference provenance; related Foundry records cover request-identity fencing and artifact identity in other domains. These are follow-up engineering observations for the existing Candidate, not evidence for creating another overlapping rule.
