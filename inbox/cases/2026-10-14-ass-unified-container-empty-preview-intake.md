# Case — Unified native container entry must preserve empty-preview intake

Status: Case / Pending Android validation. No Canonical promotion.

User identified conflicting reference-video and MKV-project entries in ASS Workbench and required one container intake from the menu or empty preview, with optional subtitles/fonts rather than mandatory prerequisites.

Source investigation: empty preview called openPickedVideo -> attachVideo, while a separate openMkvProject scanned ASS/fonts. A single OpenDocument callback now routes by header bytes into the existing Matroska reader or generic media playback/probe adapter. Matroska auto-selects a default supported ASS track, falling back to first. Video-only/no-subtitle/no-font is valid. Generic subtitle tracks are explicitly detected-but-not-editable; unified intake does not imply all adapters or output mutation are available.

Dedupe: Foundry search for container/entry found existing MKV primary-action/editor-discoverability and semantic-reconciliation visible-contract-drift records. This is ASS-specific migration evidence, not a new Canonical requirement.

Production Kotlin route/parser probe passed, including real MatroskaReader video-only bytes. Nine changed/new Kotlin files parsed with PSI. Source review fixed a stale debug Host callback and same-URI early return preceding prior-request cancellation. Authored Android lifecycle regression is not executed. No APK, generic-media playback or emulator result claimed.
