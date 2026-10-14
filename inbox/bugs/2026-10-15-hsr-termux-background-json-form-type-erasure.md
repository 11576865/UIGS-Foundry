# Bug: Termux Lite JSON-to-form adapter erased background spec and boolean types

Date: 2026-10-15
Project: `11576865/HSR-Voice-Archive-Builder`
Source: [HSR PR #165](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/165)
State: **Fix submitted in open PR; exact-head CI, merge and user physical Android acceptance pending**
Maturity: Bug / source-level diagnosis, not Canonical policy

## Concrete user report

The user could not import a project background image; switching to '项目图片' made the UI request a background color, then claimed the project image was unavailable. The UI also still imposed a 16 MiB image file limit. This occurred in an Android/Termux web session. The user also requested extra chapter FLACs inside the MKV, default gaps, language preset correction, and own AI API connectivity testing; all are scoped to HSR PR #165 rather than another Foundry issue.

## Source-level root cause

`app/lite_server.py::_form` called `_stringify_json_form`, converting JSON request dictionaries to serialized strings and JSON booleans to `"True"`/`"False"`.

Both background routes (`/api/output/archive-bundle` and `/api/output/archive-bundle/background-preview`) consumed `data["background_spec"]` directly as a native mapping, while `normalize_bundle_background` requires a mapping. They also tested `data.get("reuse_saved_background") is True`, which cannot succeed for the string `"True"`. Hence both uploaded image and saved-image replay could be rejected before FFmpeg ran.

A related presentation invariant was broken: `previous_bundle_settings` reported `image_saved=True` whenever saved background mode was `image`, without checking that the referenced content-addressed image exists and has a matching SHA-256. This could falsely present image reuse as available.

The selectable color still appeared in image mode even though it only served as a letterbox/padding color, not the requested image itself. The HTML and Python byte limits were 16 MiB image / 24 MiB JSON.

## Proposed repair in product PR

- Decode serialized nested `background_spec` JSON and convert string-like booleans using `_bool` for both Termux routes; keep existing dictionary and mode validation.
- Validate the content-addressed saved image before advertising reuse and prompt first-time image-mode users to upload or select a genuinely reusable image.
- Hide the unrelated solid-color picker in image mode; use a safe internal fallback for letterboxing.
- Expand image budget to 64 MiB (96 MiB bounded JSON), preserving FFprobe decode/dimension/pixel checks and warning against extrapolating low-memory device success.
- Add contract and real-media tests, with results **Pending CI**; do not claim phone-side success without a real image upload.

## Reusable observation

An adapter that serializes JSON into a form-style string dictionary **erases type semantics**; downstream consumers must either rehydrate at the adapter boundary or explicitly parse nested objects and booleans before business validation. JSON strings `"True"` and actual JSON booleans are not interchangeable under Python `is True`. Independently, a persisted mode choice does not prove its referenced asset is still available. This example is a concrete test case, not a universal Canonical rule.

Dedup check: searched Foundry for `background_spec Termux`, `reuse_saved_background`, `JSON form bool nested`, and `HSR background image import`. Adjacent existing HSR background-gradient observation found but no duplicate of this type-erasure failure. No automatic Canonical promotion.

Evidence boundary: the user-facing failure is reported; the precise TypeError/string-equality mechanism follows inspected code paths. PR #165 is a proposed repair whose automated and physical confirmation remain pending.
