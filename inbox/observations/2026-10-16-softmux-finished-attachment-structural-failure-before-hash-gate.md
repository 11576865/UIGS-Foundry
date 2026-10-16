# Observation: Distinguish a finished object structural failure from unavailable byte proof

Date: 2026-10-16
Status: Observation / implemented directly on product main; full exact-head CI and Pages not independently established
Product: https://github.com/11576865/MKV-Fast-Muxer
Increment: 软封0.1019版本
Affected: `src/source-attachment-delivery-evidence.js`, `src/softmux-10.14-workbench.js`, corresponding Node and Chromium E2E tests.

## Concrete issue and action

The 0.1018 read-only per-attachment finished-MKV evidence linked independently inspected source and output FileData, actual `ffprobe` inventory and immutable source/plan identity. However the included-attachment branch first checked the byte-audit receipt; an unavailable byte audit could mask a more actionable finished-output problem such as an entirely missing attachment or mismatched MIME. The UI often showed only `成品待复核` even when structural evidence already identified the failure.

0.1019 first checks **actual final-MKV attachment inventory uniqueness and expected MIME** within the same result model, then checks that the genuine independent EBML FileData SHA-256 audit authorizes a byte match. It adds separate fail-closed reason codes `OUTPUT_ATTACHMENT_MISSING` and `OUTPUT_MIME_MISMATCH` while retaining duplicate output name detection and strict `FILEDATA_AUDIT_UNTRUSTED`. No `filedata-verified` status can result from an `ffprobe` match alone. Existing source/plan File reference freshness continues to prevent stale result badges in the live Inspector.

UI applies reason-code-specific labels, renders the actual source stream index, original name -> intended name and intended MIME alongside the proof, and never claims UID/TagTargets or persisted-save correctness. Tests cover structural mismatch even in the presence of otherwise valid digest observations, and output proof boundaries.

## Generalizable finding

Separate:
1. A structurally missing or mismatched finished object (actionable failure).
2. A structurally present object whose payload is unverified (scope/availability gap).
3. An independently proven payload match (positive scoped proof).

All three are distinct from UID reference preservation and actual durable save. A generic unavailable badge for all three discards useful debugging evidence, while a structural presence check alone cannot produce a green verified badge.

## Dedupe and authority

Existing `inbox/observations/2026-10-16-softmux-source-attachment-result-identity-freshness.md` covers **per-object evidence identity, scope and plan freshness**; this item is narrower, about **diagnostic precedence when independent evidence layers disagree or are missing**. No Canonical modification; full product Chromium, native output and published site acceptance must be checked separately.
