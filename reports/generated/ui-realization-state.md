# UI Production Realization State

| Realization | Platform | Revision vs HEAD | Immutable blobs | Current source content | Current validation content |
| --- | --- | --- | --- | --- | --- |
| REALIZATION.ANDROID_COMPOSE.ASS_WORKBENCH.WORKSPACE_KERNEL | android-compose | older revision | verified | current | current |
| REALIZATION.WEB.HSR.SUBTITLE_STYLE_WORKBENCH | web | older revision | verified | current | current |
| REALIZATION.WEB.MKV_FAST_MUXER.ADAPTIVE_OUTPUT_HUB | web | older revision | verified | current | current |

## Evidence boundary

- Immutable verification proves the recorded historical evidence.
- Revision-vs-HEAD is repository-level currentness only; unrelated commits can move HEAD.
- Current source content compares declared implementation paths at current HEAD to recorded blob identities.
- Validation content is reported separately because tests can change without implementation source changing.
- Source currentness is not production visual evidence.
