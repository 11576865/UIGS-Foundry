# Observation: A responsive presentation override can reintroduce high-glare light surfaces into a dark workbench

Date: 2026-10-16
Status: Observation (user-reported, source-confirmed palette mismatch; direct `main` color correction; push CI not yet independently verified)
Project: https://github.com/11576865/MKV-Fast-Muxer
Change: `908cab8f6dead9352959b126404e2bffc75341d9`
CI test follow-up: `6532c885e0fa7642e72140d07ccbf7d9e6320f19`

## Evidence / mechanism

The 10.14 workbench base styling (`src/softmux-10.14.css`) already uses deep slate / teal surfaces; the Figma tablet-specific CSS (`src/softmux-figma-tablet.css`, active at 681–1365px) overrode key panels, header, object rows, actions, batch matrix and container tools with repeated literal `#fff`, `#f3f6fa`, dark ink and `color-scheme: light`. Because the overrides were CSS declarations rather than only tokens, changing token values alone could not remove the glaring white across large tablet panels. The user explicitly reported that the white was too bright and authorized changing `main` directly.

Applied a coherent low-glare slate/blue palette **within the existing tablet media queries**, distinguishing CSS foreground, surface and semantic accent properties, covering borders, warnings, selected rows, buttons, and native fields. Kept desktop/phone styling, DOM identities, media backend, batch executor and responsive layout unchanged. A new Chromium E2E assertion tests computed dark color-scheme, sub-80-RGB surface channels for four major areas, and contrast >=4.5 for title on header.

## Reusable learning

When applying design mockup skins over a functioning dark application, audit *all final computed background colors* at relevant responsive breakpoints, not only top-level design tokens. Property-aware replacements matter: the same `#fff` may be a panel background or a button label, and a single accent hex may be text in one selector but a filled primary action in another. Maintain semantic status contrast; automated screenshot/geometry tests can all pass while the presentation becomes unpleasant to use. Add at least one computed-style brightness/contrast guard for major surfaces after user-driven palette corrections.

## Evidence boundary

The code was written directly to main with explicit user authorization. Latest test commit was confirmed present in main via GitHub; push-triggered Actions result and deployed Pages render were not independently verified in this interaction. The observation does not claim acceptance or update Canonical UX standards.

## Dedupe

Foundry search for CSS responsive dark/light override theme regressions and glare screenshots yielded no matching item. Existing `inbox/cases/2026-10-15-softmux-1014-e2e-green-visual-hierarchy-rework.md` concerns composition hierarchy regression, not literal palette/theme inversion in a responsive override.
