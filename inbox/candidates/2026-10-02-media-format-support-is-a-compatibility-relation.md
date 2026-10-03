# Candidate: Media format support is a compatibility relation, not a Cartesian product of individually supported formats

Status: candidate
Date: 2026-10-02
Domains: media-processing, compatibility-modeling, product-semantics, evidence-modeling

## Summary

A media tool may correctly claim support for several video, audio, subtitle and font formats while still being unable to execute every possible combination of those individually supported resources.

Therefore “supported formats” should not be modeled as independent allowlists whose Cartesian product is implicitly valid. The executable capability is a relation across the actual resources, target container, processing policy and playback target.

A representative relation is:

`Compatibility(video streams, audio streams, subtitle streams, font attachments, target container, processing policy, playback profile)`

## Candidate rule

For media-processing products that combine heterogeneous resources:

- identify the actual container / stream codecs before compatibility resolution; filename extensions are hints rather than authoritative media identity;
- model compatibility compositionally across resource relationships instead of treating per-format support lists as equivalent to supported combinations;
- distinguish at least:
  - container / mux legality;
  - codec Stream Copy policy;
  - required explicit transformations;
  - semantic relevance between resources (for example fonts and ASS/SSA);
  - target playback / renderer compatibility;
  - evidence confidence;
- surface a finite, explicit decision vocabulary such as:
  - `DIRECT_COPY`;
  - `COMPATIBILITY_WARNING`;
  - `CONVERSION_REQUIRED`;
  - `UNSUPPORTED`;
  - `UNVERIFIED`;
- unknown combinations should remain `UNVERIFIED` when a real executor can safely provide stronger evidence, rather than being guessed as supported or automatically rejected;
- never silently transcode or otherwise change user intent to “repair” an incompatible combination;
- if a transformation is built into the workflow, expose its exact scope (for example WebVTT → SubRip on one subtitle stream while video/audio remain Stream Copy);
- do not treat container-level mux success as proof of playback compatibility in an unspecified player or renderer;
- even a successful full decode by the application's bundled decoder proves only that decoder/path can consume the stream; it still does not prove playback in a different target player or platform decoder.
- record rule-level compatibility and actual execution / audit evidence separately.

## Evidence

In `11576865/MKV-Fast-Muxer`, PR #55 introduces a compositional compatibility resolver after actual media probing and before the real FFmpeg mux.

Observed cases include:

- H.264 + AAC/FLAC + ASS + font can resolve as a direct-copy plan;
- WebVTT requires an explicit subtitle-only conversion to SubRip while video/audio remain Stream Copy;
- unknown video/audio codecs remain `UNVERIFIED` and are delegated to the actual FFmpeg mux rather than silently transcoded;
- a font attachment alongside only SRT / WebVTT / PGS / VobSub is not treated as a rendering dependency;
- target-player compatibility remains explicitly unverified unless a playback profile is evaluated separately.

The mux report records both compatibility-rule output and actual mux/audit evidence.

## Relationship to existing Candidate

This extends, rather than duplicates, `2026-10-02-generalized-media-workspace-legacy-output-assumptions.md`.

That Candidate concerns a single-purpose media product evolving into multiple operation modes and recommends a compatibility matrix when historical output assumptions become independent product dimensions.

This Candidate concerns a different abstraction boundary: even inside one operation and one fixed target container, individually supported heterogeneous resources do not imply arbitrary cross-product compatibility. It defines the compatibility relation, evidence states and separation of mux compatibility from playback compatibility.

It also complements `2026-10-02-filename-extension-vs-content-probe-media-ingestion-bug.md`: actual media identity is a prerequisite for compatibility resolution, but identity and compatibility are separate responsibilities.

## Scope

Applicable to muxers, transcoders, NLE/export pipelines, subtitle tooling, media ingest systems, asset packagers and other workflows that combine independently selectable media resources.

This is a Candidate only. It is not Canonical.


## Implementation result — MKV-Fast-Muxer PR #55

PR #55 merged after unit/build and full Chromium browser E2E success as `3955641f5cb6fee192acf3447d781cf6e615237a`.

The implementation keeps rule-level compatibility distinct from real execution evidence: the resolver runs after actual media probing and before mux; `UNSUPPORTED` blocks execution, `UNVERIFIED` proceeds to the real FFmpeg path without silent transcoding, and the JSON mux report records both the compatibility result and `actual-ffmpeg-mux` execution/audit evidence. Browser E2E verifies both a normal direct-copy case and an explicit WebVTT → SubRip subtitle-only conversion case.

This remains Candidate-level evidence and is not Canonical.


## Follow-up observation — “verified set” needs fixture-backed evidence

A later review of current `MKV-Fast-Muxer` main found a gap between the resolver's static “known Matroska Stream Copy” codec sets and the browser E2E evidence actually present in the repository.

The resolver currently lists multiple video and audio codecs as known direct-copy candidates, while the generated E2E fixtures exercise only a much smaller subset end-to-end. This means the word “verified” can silently drift from “observed in real mux + post-mux audit” toward “believed to be supported by the container/toolchain”.

Reusable refinement:

- a codec or combination should enter a **verified** compatibility set only when there is an explicit evidence record tying the rule to a reproducible fixture, actual executor run, and output audit;
- otherwise classify it as documented/expected support or `UNVERIFIED`, even when the container specification or native FFmpeg is known to support it;
- keep the evidence matrix machine-readable enough that tests can detect when a hard-coded verified rule lacks a corresponding fixture/test case;
- treat bundled runtime constraints separately from native FFmpeg capability, because browser/wasm builds may differ from desktop builds.

This does not invalidate PR #55's compatibility relation; it narrows the meaning of “verified” and suggests making the evidence backing explicit.

This remains Candidate-level evidence and is not Canonical.


## Implementation evidence — fixture-backed Compatibility Evidence Matrix

MKV-Fast-Muxer PR #59 merged as `e858ffb31318fc5fb47cc6615d0d2b89905e8305` and turns the follow-up observation above into an executable evidence contract.

The resolver no longer derives `DIRECT_COPY` from static “known codec” sets. A machine-readable `src/compatibility-evidence.js` now records each codec's evidence status. Only entries marked `verified-e2e` suppress `UNVERIFIED`; expected-only or unrecorded codecs continue to the real mux path without silent transcoding but are not described as already verified.

CI now generates concrete fixtures and executes the browser-local ffmpeg.wasm path for each verified entry. For every case, E2E requires:

```text
generated source fixture
  -> browser Media Identity / Compatibility Resolver
  -> ffmpeg.wasm Stream Copy to Matroska
  -> downloaded output
  -> system ffprobe codec comparison
  -> JSON compatibility evidence record
  -> post-mux audit success
```

The merged matrix executed **18/18 verified cases** in CI:

- video: MPEG-4 Part 2, H.264, HEVC, AV1, VP8, VP9;
- audio: AAC, FLAC, MP3, Opus, Vorbis, AC-3, E-AC-3, ALAC, PCM s16/s24/s32/f32 LE.

DTS intentionally remains `expected` / `UNVERIFIED` because the repository does not yet contain equivalent browser E2E evidence for it.

This strengthens the Candidate with direct toolchain-specific execution evidence but does not promote it to Canonical.


## Cross-project evidence — copied audio can mux correctly and still play silently

Quick-Automatic-Hardsub-Encoder PR #38 adds a second-project instance of the distinction between **container / mux success** and **playback compatibility**.

Observed user behavior:

```text
hard-sub with copied source audio
  -> encode/mux completes
  -> resulting file is silent in the user's playback path

same source + explicit AAC transcode
  -> resulting file has audible playback
```

The project already verifies structural output properties such as stream presence and packet-duration continuity. Those checks can show that an audio track survived the pipeline, but they cannot prove that an unspecified target player can decode the copied codec.

Reusable refinement:

- when an operation uses audio Stream Copy, surface playback compatibility as a separate uncertainty even if container compatibility and output audit succeed;
- do not silently transcode to “fix” the uncertainty;
- provide an explicit recovery action such as AAC conversion when broad playback compatibility matters;
- wording should distinguish “audio track exists” from “target player can render/decode this audio”.

PR #38 implements this as a visible shared audio-policy warning and carries the same warning into compiled task compatibility output. It merged as `2c4dea6a2e634a7b0ea0bb34cd0b87858d89fa77` after frontend, Windows smoke, FFmpeg integration, build and UI smoke checks passed.

This strengthens the existing Candidate with cross-project evidence. It remains Candidate-level and is not promoted to Canonical.


## Implementation refinement — codec-aware playback guidance

Quick-Automatic-Hardsub-Encoder PR #39 merged as `94238aa40826e48f3c6841486ec545e6f04fa461` and refines the generic copied-audio warning into probe-backed, codec-aware guidance.

The implementation consumes existing FFprobe / Native probe evidence:

```text
audioCodecs
audioTracks
audioBitRate
```

and separates **evidence about the source stream** from **claims about the target player**.

Current policy:

- AAC / MP3 copied audio is rendered as informational guidance because those codecs usually have broad playback support, but the UI still explicitly says that the actual external player has not been verified;
- DTS, FLAC, Opus, mixed codec sets, and other player-dependent codecs retain warning-level guidance;
- missing codec identity remains explicitly unknown rather than guessed;
- no case silently converts copied audio;
- warning-level cases provide explicit AAC conversion as a user-controlled recovery action;
- source-media UI exposes all detected audio codecs, track count and aggregate bitrate rather than collapsing multi-track input to only the first codec.

Reusable refinement:

- compatibility communication should use the strongest available **observed identity evidence** to make warnings more specific;
- reduced warning severity must not erase the remaining evidence boundary: broad ecosystem support is not the same as target-player verification;
- UI state should distinguish `common / informational` from `player-dependent / warning` and `unknown`, instead of giving every copied stream the same generic warning;
- a recovery action should remain explicit and reversible rather than automatic.

Browser UI regression coverage verifies probe-driven AAC ↔ DTS state changes as well as Copy ↔ AAC policy changes.

This strengthens the Candidate but remains non-Canonical.

## Follow-up observation — metadata probe success is not decoder support

A Quick-Automatic-Hardsub-Encoder capability review for Bink 2 (`.bk2`) adds another evidence boundary.

The Windows Native probe separately records:
- FFprobe/container/stream metadata;
- a one-frame FFmpeg decode smoke result (`inputDecodeSmoke`).

That separation matters because an executor may recognize the container/header well enough to return dimensions, duration, streams or format identity while still lacking a decoder for the actual video bitstream. Current FFmpeg Bink demuxing is a concrete example: Bink-family metadata can be recognized while Bink 2 video decoding is not implemented.

Reusable refinement:
- media-ingest capability should distinguish at least **recognized/probed**, **decodable**, and **transcodable**;
- a successful metadata probe must not promote an input to “supported” if decode evidence failed or is unavailable;
- downstream transcode/hardsub execution should gate on decode capability, not merely on probe success;
- UI should surface “metadata readable but video decoder unavailable” as a first-class unsupported state rather than allowing the failure to appear later during preview or encode.

This reinforces the existing compatibility-relation Candidate; it does not create a new Canonical rule.

