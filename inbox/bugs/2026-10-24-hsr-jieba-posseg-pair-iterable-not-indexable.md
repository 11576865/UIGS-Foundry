# Bug: Iterable jieba POS pairs leaked through a tuple-typed subtitle tokenizer boundary

Date: 2026-10-24
Project: `11576865/HSR-Voice-Archive-Builder`
Evidence: user-reported Android/Termux build failure; [HSR PR #216](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/216)
Status: **Bug / Candidate — source-level diagnosis, fix submitted; CI and device rebuild pending**
Maturity: observed failure + isolated deterministic reproduction; **not Canonical**

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
- Product patch: submitted, **not yet merged**.
- Full CI and Termux physical build: **Pending External Validation**.
- Dedup check: searched Foundry for `jieba` and `subscriptable`. The adjacent [2026-10-15 HSR Termux JSON/form type-erasure bug](https://github.com/11576865/UIGS-Foundry/blob/main/inbox/bugs/2026-10-15-hsr-termux-background-json-form-type-erasure.md) concerns another adapter type-contract failure, not a duplicate; preserve as a separate bug case.
- No Canonical promotion from this single incident.
