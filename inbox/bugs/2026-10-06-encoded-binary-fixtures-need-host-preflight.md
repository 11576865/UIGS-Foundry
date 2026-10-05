# Bug: encoded binary test fixtures must be validated before device execution

Status: **Bug / Observation**
Date: 2026-10-06
Project evidence: `11576865/ASS-Workbench-Android` PR #129

## Symptom

An Android Emulator regression intended to exercise a real MP3 bitstream failed immediately in:

`android.util.Base64.decode(...)`

with:

`java.lang.IllegalArgumentException: bad base-64`

The product path had not run yet.

## Root cause

The embedded MP3 fixture string was syntactically invalid Base64:

- length was 2430 characters;
- `length % 4 == 2`;
- only one trailing `=` padding character was present.

The fixture had been treated as opaque test data and was only validated indirectly when the Android device attempted to decode it.

This allowed a malformed fixture to masquerade as a product regression.

## Fix

The invalid fixture was replaced with a newly generated compact MP3 fixture that was preflight-checked before repository write:

- 44.1 kHz;
- stereo;
- MPEG Layer III;
- 522 bytes;
- Base64 length 696;
- `length % 4 == 0`.

No production MP3 import code was changed.

## Reusable test rule

When binary device fixtures are embedded through textual encodings such as Base64, validate the fixture at the cheapest earlier boundary before scheduling device/emulator execution.

At minimum, preflight should check:

1. textual encoding validity;
2. successful host-side decode;
3. decoded byte size > 0;
4. format signature / probe where practical;
5. any metadata assumed by the test (for example sample rate/channel count).

This separates:

- **fixture corruption**;
- **test harness failure**;
- **product behavior failure**.

Device CI should not be the first layer that discovers malformed textual fixture encoding.

## Evidence boundary

This is one concrete emulator failure in ASS-Workbench-Android PR #129. It is recorded as a Bug/Observation and does not by itself modify Canonical guidance.
