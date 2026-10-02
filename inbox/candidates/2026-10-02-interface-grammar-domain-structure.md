# Candidate: Interface Grammar domain structure

Status: candidate
Date: 2026-10-02

## Purpose

The hundreds of reusable UI designs, their exact implementation methods, expected effects, platform variants, visual evidence, and known failures should live as a first-class domain inside Foundry rather than in the top governance layer.

## Proposed structure

domains/interface-grammar/
  grammar/
  registry/
    primitives/
    controls/
    patterns/
    compositions/
  realizations/
    web/
    android-compose/
    windows/
  showcases/
    reference-demos/
    interaction-recordings/
    visual-baselines/
  validation/
    behavior-contracts/
    visual-regression/
    accessibility/
    performance/
  evidence/
    cases/
    screenshots/
    recordings/
  compatibility/
    platform-matrix/
    fallbacks/
  aliases/
  schema/

## Separation of concerns

A UI entry should separate:
- semantic identity: what the UI means and when to use it;
- interaction contract: states, transitions, input, ownership, dismissal, scroll behavior;
- visual contract: hierarchy, geometry, typography, transparency, blur, motion;
- platform realization: concrete CSS / Compose / Windows implementation recipe;
- reference effect: screenshots, recordings, golden baselines, demo pages;
- validation: behavior, visual regression, performance, accessibility;
- failure knowledge: linked Bug Museum cases and anti-patterns.

## Core principle

Foundry should let a human or agent resolve:

natural-language intent
-> UIGS pattern ID
-> composition
-> platform realization
-> reference effect
-> validation contract
-> known failures

The implementation code in product repositories remains authoritative for shipped products. Foundry may host reference implementations and demos, but should not become a second copy of every product implementation.

## Example

UIGS.WORKSPACE.STICKY_SUPPORTING_PANE

registry:
- intent
- anatomy
- states
- constraints
- aliases

realizations/web:
- CSS Grid / sticky / overflow recipe
- translucent and opaque variants
- fallback rules

realizations/android-compose:
- layout / scroll / surface recipe
- WindowInsets and touch considerations

showcases:
- reference screenshot
- short interaction recording
- demo fixture

validation:
- scroll behavior
- viewport resize
- narrow-layout fallback
- nested overflow regression
- readability and contrast

known failures:
- linked Bug Museum entries

## Promotion rule

A screenshot or one successful implementation is evidence, not Canonical grammar. Promotion should require stable semantics plus repeatable implementation/validation evidence.
