# Bug: Cancel→new media task can reuse stale external-resource authority inventory

Date: 2026-10-14  
Status: **bounded repair submitted, latest exact-head Chromium CI Pending**  
Product: `11576865/MKV-Fast-Muxer`  
PR: [#133](https://github.com/11576865/MKV-Fast-Muxer/pull/133)

## Exact CI evidence

- First PR #133 head `ab11a3488421c14cc1dff1de2a305a8e31afb051`: Browser E2E [run 38509102937](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38509102937) failed. Node unit tests, Vite build, fixtures and most Chromium scenarios passed. Chromium **scenario 10** (cancel active FFmpeg task, reselect source+subtitle+font, immediately mux another source) stalled for 180 seconds with product status `EXTERNAL_DOMAIN_INVENTORY_CHANGED` before starting the second mux.
- First fix `5c85ff720d126502aba3ba9c077b30dddb04a8b3` invalidated the domain session on primary source selection and recreated when none was present. Browser E2E [run 38510103407](https://github.com/11576865/MKV-Fast-Muxer/actions/runs/38510103407) **still failed at exactly the same scenario and status**, although Node/build passed. That means invalidation alone was insufficient: selection events or async resource inspection could establish an inventory snapshot before the new task's final FileList selection was complete.
- Latest bounded fix `4861400920a04c8fea54e319b14e187cba79089d` adds an explicit **new-primary-task rebind allowance**. On a real primary-video change, mark the previous external-domain session invalid and set a single-use task-rebind flag. At the next single-job mux preflight, if this flag exists, resynchronize actual current audio/subtitle File/sidecar references (without transferring prior metadata to different File object references), create one current domain authority and clear the flag before checking editor/executor consistency. **Ordinary same-task File or metadata drift still refuses authorization**. The independent frozen batch executor is not changed.

## Scope / evidence status

The latest fix is an informed bounded hypothesis; its own exact-head CI must be observed. Do not report this bug fixed or #133 merge-ready without Chromium green. Explicit scenario 10 already supplies the actual regression oracle, along with later scenarios that test same-metadata File replacement. The failure is a production workbench recovery blocker, **not** a test harness artifact.

## Reusable hypothesis

An immutable domain owner bound to one browser FileList generation must distinguish ordinary unauthorized mutation from an explicitly authorized **new-task** session boundary. Merely nulling the old domain instance at the first change event can still be insufficient in a UI with asynchronous format/font inspection and multiple sequential file inputs; derive the new authority at a well-defined task commit boundary and preserve exact `File` identity checks. Record as Bug only; do not promote a single recovery attempt into Canonical.

See prior Case `inbox/cases/2026-10-14-mkv-external-assets-live-domain-file-identity-and-stale-form-epoch.md` for the source-neutral editor migration.
