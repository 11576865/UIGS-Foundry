# Bug: absolute Windows paths break libass filtergraph in an independent media verifier

Date: 2026-10-14
Status: Bug / test-harness failure repaired, exact-head recovery CI Pending
Project: Quick-Automatic-Hardsub-Encoder PR #105
Failing workflow: https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/38554057407

## Observation

The first real Windows Native acceptance for QHE WU-02 completed MKV source generation, localhost embedded ASS/font extraction, shared schema-v4 task compilation, actual Native encoding and the independent output stream/audio/font checks. It then failed while generating an **additional no-events ASS counterexample** in `scripts/verify-wu02-native-output.mjs`. The verifier inserted an unescaped absolute Windows `D:\...` path into an FFmpeg filtergraph string as `ass=D:\...:fontsdir=D:\...`. FFmpeg parsed the drive colon and backslashes as filter syntax rather than opaque filenames, returning `No option name near ...`.

This is a verifier-side error; no evidence from this failure by itself shows that the product's relative `ass=subtitle.ass:fontsdir=fonts` Native encoding path failed.

## Bounded repair

QHE commit `1148bcda33bc74f66275eaad73d125e29930b8fb` changes the verifier to use `empty-events.ass:fontsdir=embedded-fonts` relative to a controlled private working directory (`cwd:work`), instead of interpolating an unescaped Windows absolute path into the filter expression.

## Evidence boundary

At record creation, the new exact-head hosted Windows acceptance has not been confirmed. Keep `PENDING`; do not attribute a completed WU-02 or whole application acceptance to the correction. This is a source-string / filtergraph escaping distinction, not a Canonical rule.
