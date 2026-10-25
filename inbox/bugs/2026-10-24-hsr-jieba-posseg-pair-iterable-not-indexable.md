# Bug: Iterable jieba POS pairs leaked through a tuple-typed subtitle tokenizer boundary

Date: 2026-10-24
Project: `11576865/HSR-Voice-Archive-Builder`
Evidence: user-reported Android/Termux build failure; [HSR PR #216](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/216)
Status: **Bug / Candidate — source fix, build regression and Termux-lite CI regression merged; physical Android/Termux rebuild pending**
Maturity: observed failure + isolated deterministic reproduction + passing PR CI + merged implementation; **not Canonical**

## Symptom

A user building an `evanescia` voice archive on Termux saw `TypeError: 'pair' object is not subscriptable`. The visible traceback showed entry frames in `app/jobs.py:300` and `app/lite_server.py:1096` calling `build_project_v02`. Those frames were task wrappers, not the failing subscript.

## Source-level mechanism

`subtitle_layout/semantic_chunker.py::_cut_words` declares `list[tuple[str, str]]` but returned `list(jieba.posseg.cut(text))`. `jieba.posseg.cut` yields `pair` objects that support iteration/unpacking but do **not** implement `__getitem__`.

The downstream orphan-protection branch inside `split_chinese_semantic` can execute `last_word = words1[-1][0]` after stripping punctuation from a candidate line boundary. When that path receives a `pair` rather than a tuple, it raises exactly the observed error, aborting the parent archive build.

## Repair and tests

[HSR PR #216](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/216) changes the adapter to `[(word, flag) for word, flag in pseg.cut(cleaned)]`. It preserves word/tag values while materializing ordinary indexable tuples. It also adds `tests/test_semantic_chunker_pair.py` with:
- a POS pair double that is iterable but intentionally not subscriptable;
- a punctuation-stripping/orphan path regression;
- a no-jieba character fallback regression.

Isolated pre/post demonstration: indexing a raw `pair` raises `TypeError`; indexing the normalized tuple succeeds. This is local mechanism evidence, not a claim that the full mobile archive finished building.

## Reusable observation and scope

A third-party result may support tuple *unpacking* without tuple *indexing*. Static return type annotations do not transform the runtime type. Normalize at the **integration boundary** if downstream code requires a stronger sequence contract; test with a realistic non-subscriptable adapter object, not solely with Python tuples.

Applicable to NLP tokenizers, parsers, vendor SDKs and other iterable object adapters. Keep the conclusion scoped to this failure class; do not mandate materialization when streaming is intentionally required.

## Evidence boundary and provenance

- User screenshot: reported failure and abbreviated upper traceback.
- Repository inspection: actual `_cut_words` and orphan guard mismatch.
- Deterministic reproduction: isolated tuple-indexing behavior.
- Product patch: **merged as PR #216** into HSR main at merge commit `19145b4ec7cba4c96da0a818c7ee35944cd0dd9e`.
- PR #216 exact PR-head CI: **5 workflows passed** (`tests`, HSR seven ASS requirements, sustained concurrent job journal regression, Windows writer and journal safety, pinned legacy interop and process-exit recovery). Later merge-head evidence and remaining device validation are listed below.
- Dedup check: searched Foundry for `jieba` and `subscriptable`. The adjacent [2026-10-15 HSR Termux JSON/form type-erasure bug](https://github.com/11576865/UIGS-Foundry/blob/main/inbox/bugs/2026-10-15-hsr-termux-background-json-form-type-erasure.md) concerns another adapter type-contract failure, not a duplicate; preserve as a separate bug case.
- Follow-up [HSR PR #217](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/217) added a synthetic `build_project_v02 -> ASS` integration regression with a real PCM WAV, official Chinese LAB, and a non-subscriptable POS pair double. The test asserts that `你好吗` entered the formerly vulnerable orphan-guard branch, rather than merely succeeding without exercising it. **Merged** into HSR main at `c4e67fed174a37989669b1b98dcdc8321bd13f63`. Exact PR-head CI: **5 workflows succeeded**. Merge-head CI: **6 executing workflows succeeded** (see next line).
- Merge-head verification: HSR main `c4e67fed174a37989669b1b98dcdc8321bd13f63` completed 6 executing workflows successfully; UIGS Intake Adapter skipped. This supports code/test integration only, not native Termux acceptance.
- Dependency-surface follow-up: [HSR PR #218](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/218) adds the same ASS build regression to the existing `termux-lite-surface` CI job under `requirements-termux.txt` (no FastAPI, py7zr or vendor SDK). **Merged** into HSR main at `27c281aba9bc6d17053ac548d4a39fdc9b0c55d5`; exact PR-head **5 workflows succeeded** and `termux-lite-surface` explicitly passed its new build regression step. On HSR merge-head `27c281aba9bc6d17053ac548d4a39fdc9b0c55d5`, **6 executing workflows succeeded, 0 failed**, and the UIGS Intake Adapter was skipped; GitHub source-side verification complete. Physical Android/Termux acceptance remains **Pending External Validation**. Ubuntu emulation does not replace the still-**Pending** physical Android Termux `evanescia` rebuild.
- Durable HSR task checkpoint: `.uigs/tasks/hsr-jieba-pair-build-crash-20261024.json` (main commit `200e8f64457753b29f329134d8bd9e3a38ed6860`); explicitly separates passing CI from missing real-device build and output inspection.
- No Canonical promotion from this single incident.
