# Candidate — Per-field parameter provenance and write-intent preview in professional editors

Date: 2026-10-14
Status: Candidate / design proposal from ASS UI review, NOT approved Canonical, NOT production implementation, NOT native screenshot evidence
Product: 11576865/ASS-Workbench-Android
Trigger: User requested improvement to parameter provenance and write semantics in a 1534×960 pending-review ASS tablet concept screenshot.
Related source: `core/domain/src/main/kotlin/io/github/assworkbench/domain/AssEffectiveInspector.kt`, `app/src/main/kotlin/io/github/assworkbench/app/ui/workspace/WorkspaceEditScope.kt`, project UI constitution (2026-10-01) and tablet report (2026-10-14).

## Problem
A single top-level “局部覆盖” tab or “来自 Style: Opening” label for an entire Event inspector misrepresents multiple independent parameter sources. The sample Raw includes `\\pos(960,720)\\fs48`, i.e. Event-local tags, while unoverridden typography may come from Style `Opening`. An Event without `\\pos` is positioned by alignment/margins/layout, not a fictitious Style.Position. `\\r` and `\\t` can cause property source/value to depend on text span and media time. “Read this value” and “modify this owner” are separate choices.

## Existing project authority / non-novel base
The UI constitution already requires Read Source vs Write Target, WHO/WHERE/HOW MANY, Focus/Selection/Binding separation, true renderer semantics, raw preservation, explicit commits. `AssEffectiveInspector` already exposes styleValue, direct override and effectiveValue for the first rendered span plus `spanDependent`. `WorkspaceEditScopeResolver` already distinguishes SHARED_STYLE, EVENT_TEXT, EVENT_FIELDS, EVENT_OVERRIDE, Karaoke and BATCH. These underlying principles are **not new** and must not be re-introduced as a newly discovered Canonical law.

## Incremental Candidate
- Put a compact **per-field source marker** adjacent to each resolved parameter instead of a global provenance chip; visible value and source can refer to different owners than the pending write target.
- The inspector keeps one compact **target/scope receipt** showing the bound object, intended write layer and affected-object count, with no implicit switch from read source to write target.
- On field expansion expose an origin chain (event style baseline; preceding `\\r` reset; Event tag; animation `\\t`; time/span sensitivity and unsupported ambiguity). Never collapse unsupported/mixed values into false single scalars; check source-derived status independently from visual libass authority.
- Treat editing a shared Style as a distinct explicit transaction. A Style's referencing Event count is not automatically the count of visibly changed Events (local overrides may mask changes), and `\\pos` has no editable Style.Position equivalent.
- Before Apply, show a concise **write plan receipt** with owner, field/tag destination, computed impact scope, source revision and Raw diff. Disallow mixed shared-Style and Event writes in one silent transaction; check target identity and baseline again in the domain's actual commit transaction, preserve unrelated/unknown tags and drafts on rejection.
- Do not make source-view chips trigger mutations, do not auto-commit from gestures, and keep Undo document history separate from workspace layout.

## Verification / falsification
1. Event #39 with local `\\fs48` and `\\pos(960,720)`; other Style fields inherited: provenance must differ by row.
2. Remove `\\pos`: display calculated alignment/margins or unresolved layout, not Style.Position.
3. A leading or later `\\rStyle` plus `\\t` should show span/time caveat, and actual libass output is independently checked.
4. Editing shared Style referenced by N Events with masked overrides: label referencing count and visual impact separately, and never silently write to Event text.
5. Raw edits between draft and Apply: source conflict inhibits old proposal, preserves user draft, and creates no false Undo entry.

This is a review candidate; the image generated in chat remains an illustrative concept rather than proof of exact typography, source correctness or Native implementation.

## Dedupe
Searched Foundry for 'field-level effective value source write target dynamic span-dependent provenance per property', 'ASS shared style event override write scope inspector who where how many', 'parameter source provenance write intent preview commit conflict' and 'per-field origin Style reset r transform t source inspector'. No exact reusable interface treatment was found. The foundational read/write distinction already exists in project constitutions and `inbox/observations/2026-10-14-ass-video-first-tablet-concept-screenshot.md`; this entry records the **field-level visual contract and pre-commit scope receipt** only. Do not promote Canonical from this one proposal.
