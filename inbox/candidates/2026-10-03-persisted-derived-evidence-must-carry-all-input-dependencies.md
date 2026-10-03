# Candidate: Persisted derived evidence must carry all input dependencies

Status: Candidate

## Observation

A persisted calibration or prediction record can be numerically valid yet unsafe to reuse when its identity omits an input that materially affects the measurement.

In Quick-Automatic-Hardsub-Encoder PR #47, a quality sample was initially keyed by source video + encoder runtime + codec + preset. The sampled encode also burns ASS subtitles and uses selected fonts, so changing subtitle text/style/font inputs can change both bitrate and measured quality even when the source video is unchanged.

## Candidate rule

For persisted derived evidence:

- define the complete dependency set of the measurement before enabling reuse;
- include every material input/configuration dependency in the reuse identity, or disable reuse;
- distinguish source identity from render/configuration identity when both affect the result;
- treat runtime/toolchain identity as another dependency when implementation changes can shift measurements;
- prefer collecting evidence without reuse over reusing evidence under an incomplete key.

A cache/evidence key is a correctness boundary, not merely an optimization detail.

## Evidence

Single project observation from compression quality calibration review. This does not justify a Canonical rule by itself.


## Follow-up implementation evidence

PR #47 was changed so quality calibration records with an incomplete render dependency key are persisted as `observation` evidence only. They are excluded from reusable source-quality priors until the effective ASS/font/render configuration is included in the identity.

This makes the safe fallback explicit: retain measurements for later analysis, but do not let incomplete identity silently become cache reuse.
