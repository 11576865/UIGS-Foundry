# QHE workbench plan order and save-method disclosure

Status: Observation, runtime acceptance pending.

[QHE PR #149](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/pull/149) moves the planned output before the processing range for hard subtitle and transcode, while Stream Copy keeps its cut range first. The DOM order follows the visual order so sequential navigation uses the same priority. The planned-output UI reports the delivery method, distinguishing browser download from a Native save picker available at delivery time. It does not imply that a destination is already selected.

Evidence: source review and syntax checks at `4d87e47`. The [desktop/tablet Chromium regression](https://github.com/11576865/Quick-Automatic-Hardsub-Encoder/actions/runs/41885543439) covers mode-specific order and browser wording; its result and visual review are pending. Scope is the QHE desktop/tablet workbench. No Canonical change.
