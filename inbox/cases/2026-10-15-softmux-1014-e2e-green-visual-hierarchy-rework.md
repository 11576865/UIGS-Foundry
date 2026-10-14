# Case: 软封10.14版本 — full Chromium E2E green did not prove a composition-centred visual hierarchy

Date: 2026-10-15
Status: **Case / two actual E2E browser runs passed; final duplicate-editor polish CI pending**
Product: `11576865/MKV-Fast-Muxer`
Authority PR: https://github.com/11576865/MKV-Fast-Muxer/pull/153
Contract: `docs/软封10.14版本_完整UI合同与原子切换.md` on the PR branch
Product baseline: `main@8b8ec0e30908a3960da5f9f26f6acf7444ecb60c`; existing release `package.json.version=1.2.2`.
User-approved target name: **软封10.14版本** (not an inferred Semantic Version).

## Verified first visual failure despite passing browser regression

A coherent `?ui=10.14` candidate originally rehosted actual production DOM nodes under source / output composition / selected inspector, preserving handler/File identity and leaving main unchanged. Exact-head complete Chromium E2E run [38633000885](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38633000885) **passed**. Real screenshot artifact [11927156950](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38633000885/artifacts/11927156950) (desktop 1440, batch 1440, tablet 800, phones 390/360) nonetheless showed that:
- the central prospective-MKV region was visually dominated by an always-expanded external-audio/subtitle checkpoint/recovery form;
- after the imported source changed, the legacy `sourceFilesDetails` auto-collapsed because the model deemed no source choice necessary, yielding an apparently empty source area despite a real source and displayed output plan;
- the inspector displayed a very large empty subtitle preview even when no previewable subtitle was selected;
- narrow viewports had under-styled focus buttons and excessive continuous controls;
- batch import dominated left-side geometry while the real output job matrix was narrow.

**Automated correctness ≠ layout/information hierarchy quality.** Do not call that first candidate design accepted solely because the E2E run was green.

## Implemented candidate rework, preserving the real backend

The single PR made these bounded changes only in its own layout/visual/test files:
1. Move the actual checkpoint/recovery controls into `details#sf14Recovery`, visible on demand and automatically opened for relevant JSON imports. Never remove their event listeners or treat their form state as project authority.
2. Keep `sourceFilesDetails` intentionally open in the 10.14 persistent source pane by setting its existing `data-user-toggled` presentation flag. This prevents the legacy role-selection auto-disclosure from hiding actual source inventory in a different presentation.
3. Put the real subtitle preview and existing global editor controls into separate contextual disclosures; the same actual `.editor-grid`, preview node and inputs survive.
4. Reorient the existing batch view so the Job Matrix and selected task inspector are primary; no second runner/recipe is created.
5. Add proper mobile focus controls and tablet source drawer; preserve DOM, File grants, selection and in-memory edits across display transitions.
6. Switch the visual test from `base.mp4` with sparse output to independently provided `source-multitrack.mkv` with actual video/audio/subtitle rows and two real batch plan outputs. The DOM selectors/evidence come from the production implementation, not invented E2E fixtures.

The second exact-head Chromium run [38634629092](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38634629092) on `1216a7fd99c9a95c08e3cdbde3a40be6d08e3b2e` **passed** complete E2E and independent back-end checks. Actual screenshot artifact [11928036002](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38634629092/artifacts/11928036002) visibly showed 4 real source streams, container risk, selected source Opus properties, two real batch target rows, and tablet/phone focus layouts.

## Follow-up not yet proven by this case

The second screenshots still showed an extra legacy bulk-editor drawer expanded when a source track was selected, and a duplicate mobile back control. A third, small same-PR correction keeps bulk settings closed for source-owned track selections (actual inspector stays visible), hides the legacy back control and changes outer heading to Inspector. Regression assertion was added. **CI result and new screenshots for that final head are pending; do not borrow the earlier green run as final acceptance.**

Even a green final head will prove only bounded media+UI regression at tested screen sizes, not every product requirement, ideal aesthetics, every browser/device, or full P0–P6 release acceptance.

## Relationship and deduplication

- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md` already proposes composed output as primary object; this case **adds a later actual implementation/visual failure and a concrete DOM rehosting migration fix**, not a competing normative principle.
- `inbox/candidates/2026-10-03-presentation-density-state-continuity-by-stable-component-identity.md` already discusses retaining semantic component identity; this case does not repeat its general rule.
- `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md` already distinguishes verification from requirement completion; this case contributes a real visual counterexample to treating whole-suite E2E as UI acceptance.
- `inbox/cases/2026-10-13-ass-ui-design-freeze-rc-prototype-honesty-and-handoff-gates.md` records a separate offline design/production distinction.

Scope: one product-specific Case. **No Canonical revision**.

## 2026-10-15 continuation: explicit user-authorized UI cutover

The product owner authorized the assistant to choose a new layout and merge the UI into `main` without waiting for additional aesthetic signoff. This is not a declaration of final design approval.

The sole pre-existing PR #153 was revised to make the proposed output composition the dominant desktop region, with an explicit `tracks / attachments / chapters / tags` entry strip, accessible tab selection and clear copy when a dedicated editor is not yet supported. The sidebar continues to rehost live source/asset identity, the right inspector live selected-object state and the bottom dock the original real execution/audit lifecycle. This remains an incremental presentation layer over existing DOM, **not** the fully realized executable-design-source approach proposed in the separate Candidate.

To avoid making unverified future features look operational, unsupported dedicated attachment/chapter/tag composition tabs lead to informational capability panels and a route back to the existing source evidence or track workspace. Such panels do not claim attachment rewrites or UID preservation. Non-UI legacy regression tests explicitly use `?ui=legacy`; a new default-path browser scenario verifies `/` mounts 10.14 and permanently exposes all four navigation entries.

Evidence:
- Exact pre-merge head `9c9d38335fec2db554a53572a0d2552b330cb43b`.
- Full Browser E2E **success** https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38646235461 ; browser screenshot artifact https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38646235461/artifacts/11933067038 (desktop 1440, tablet 800, phones 390/360, batch).
- Pages/build **success** https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38646235688.
- **Merged** https://github.com/11576865/MKV-Fast-Muxer/pull/153 with squash commit `a1f4e0aa3af33c2459d8a66569b9043e75feec21`. Main was independently read back at this SHA.
- Post-merge main E2E and Pages workflows were still **in progress** at the time this line was recorded (runs 38647059416 and 38647059252). Do not claim post-merge success until both finish.
- Independent earlier PR #151 Matroska subtitle timing issue #152 is not addressed by UI cutover; do not infer it is resolved.

This is implementation/evidence evolution of the **same Case**, not a new normative Pattern or Canonical modification. The visual result is a bounded candidate that the owner explicitly deferred further polish on, not a professionally accepted final mockup.
