# Candidate: Human-facing trim time inputs should accept common clock formats and normalize centrally

Date: 2026-10-03
Status: Candidate
Scope: media trimming / hardsub UI / time parsing

## Observation

A media tool that exposes trim start/end as raw seconds only creates unnecessary input friction. Users naturally enter:
- seconds: `237`
- fractional seconds: `237.250`
- minute clock: `3:57` or `3:57.250`
- hour clock: `1:03:57` or `1:03:57.250`
- full-width colon variants from CJK input methods.

The current Quick-Automatic-Hardsub-Encoder task compiler converts start/end with JavaScript `Number(...)`, so decimal seconds are accepted but colon-delimited clock formats are rejected.

## Candidate principle

Parse human-facing time text through one central normalization function before task compilation. Preserve the internal authoritative unit as seconds (floating point) or a higher-precision timestamp representation.

Recommended accepted grammar:
- `SS[.fff]`
- `MM:SS[.fff]`
- `HH:MM:SS[.fff]`

Normalize full-width punctuation where unambiguous, reject invalid minute/second fields, and display the parsed canonical value back to the user.

Do not duplicate parser logic in separate UI branches.

## Testing

Include round-trip / rejection tests for:
- `3.57` => 3.57 seconds
- `3:57` => 237 seconds
- `3:57.250` => 237.25 seconds
- `1:03:57.250` => 3837.25 seconds
- full-width colon variants
- invalid values such as `3:99`, negative values, NaN, and end <= start.

Do not promote to Canonical from this single observation.
