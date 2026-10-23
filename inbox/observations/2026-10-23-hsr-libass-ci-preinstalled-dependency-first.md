# Observation — Prefer verified preinstalled media tools before hosted-runner apt fallback

Date: 2026-10-23
Scope: GitHub Actions Ubuntu HSR real-media acceptance
Level: **Observation / single-project CI delay and test evidence; not Canonical**
Project: `11576865/HSR-Voice-Archive-Builder`
Primary PRs: [#204](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/204), [#205](https://github.com/11576865/HSR-Voice-Archive-Builder/pull/205)
Status: **SOURCE-FIXED; PR-CI VERIFIED; exact merged-main CI in progress**

## Observation

Two HSR workflows, `hsr-seven-ass-requirements.yml` and `tests.yml` real-libass-ink-evidence, ran `sudo apt-get update -qq` and `apt-get install` **unconditionally**, before even trying to use the hosted Ubuntu runner's already-available FFmpeg/libass and DejaVu. The first run spent substantial time in `Install real libass, FFmpeg and fonts`, while all unrelated test jobs completed, causing friction in exact-main release validation. The specific underlying package mirror / GitHub runner network cause is **not established**. No unsupported claim of outage or product regression.

## Actual repair and real-evidence gate

Both workflows now:
1. Test executable availability for `ffmpeg` and `fc-match`.
2. Require an actual `subtitles` or `ass` FFmpeg filter and successful DejaVu font matching (checking only command presence would miss absent libass/font assets).
3. Only when any prerequisite is absent: `sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg fonts-dejavu-core fontconfig`.
4. Always run the same unmodified real-media test suites and check real FFmpeg filters/font identity. No mock, skip or weakened output assertions.

After #204 changed seven ASS prerequisites, [exact PR-head seven ASS #39895934667](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39895934667) and [merged-main seven ASS #39896139995](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39896139995) passed. #205 transferred the proven dependency-first pattern to `tests.yml` real ink evidence: [exact PR-head `tests` #39896527289](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39896527289) successfully completed its genuine `test_libass_ink_layout` job as well as Python 3.11/3.12/3.13 and Termux-lite surface. [Seven ASS head #39896527304](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/39896527304), Windows, and cross-process suites also passed. #205 merged to `main@d5eaf369b241ba9def9e41e4050aaf3369742cc5`; exact-main post-merge verification was in progress at initial intake.

## Interpretation / decision

This supports a **bounded, test-backed optimization for this media-workflow environment**: check the genuine runtime prerequisite already on the hosted runner before using an external OS package mirror; keep conditional fallback and identical media validation. It does not prove that every Ubuntu runner already has a compatible FFmpeg/libass/font version; version/security updates may still justify explicit installation for other projects. No blanket rule should be promoted from one repository.

## Dedup

Foundry searches for `apt-get update repeated GitHub Actions FFmpeg libass fonts`, `preinstalled runner dependency check apt fallback`, `CI hosted Linux apt update blocked` returned no existing record. The product-specific Bug `inbox/bugs/2026-10-23-hsr-final-marker-commit-and-legacy-seal-preflight.md` documents PR #204's media publication integrity fix; this separate observation is about **CI execution prerequisites**, not user files or MKV receipt semantics.

**Pending:** exact-main post-merge job closure, actual physical Termux/Windows user-device runs, more runners and distribution versions. No Canonical modification.
