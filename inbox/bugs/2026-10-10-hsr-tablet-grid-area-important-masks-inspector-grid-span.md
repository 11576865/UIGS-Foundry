# Bug: Legacy grid-area !important defeats responsive inspector spanning

Date: 2026-10-10
Status: Bug (fix implemented in unmerged PR; browser regression passed)
Scope: Responsive CSS / grid cascade / interaction layout / browser evidence
Source: 11576865/HSR-Voice-Archive-Builder PR #132

## Symptom

The HSR subtitle studio uses a 3-column desktop workbench and a 2-column tablet
layout. At **768 × 1024 Chromium viewport**, the Inspector was expected to span
both tablet grid columns in a lower row. It actually rendered at **x=7px,
width=240px**, occupying only the narrow left navigation column, while the
main cue editor occupied the wider center column. The page had no horizontal
overflow, so ordinary overflow-only responsive tests falsely appeared green.

The discrepancy was measured from production HTML/CSS/JS rendered in Chromium
with a deterministic project fixture and recorded in a browser screenshot.

## Cause

A legacy inspector rule declared **grid-area:auto!important**. A later tablet
media rule declared only **grid-column:1/-1** and **grid-row:2**, without
overriding the entire shorthand's important cascade. The older important
grid-area shorthand therefore controlled final placement. The rendered page
exposed the conflict even though static CSS inspections and Node interaction
tests had passed.

## Fix

At the tablet breakpoint (760px to 1360px), the specific owning selector sets:

- `grid-area: 2 / 1 / 3 / -1 !important`
- `width: 100% !important`
- `justify-self: stretch !important`

The generated workbench now places the inspector across the full tablet grid.

## Evidence and regression

- Initial successful fixture browser run: Actions `38033430499`, Chromium
  geometry and image `tablet_768_studio.png` captured the narrow inspector.
- Regression fix: branch `feat/subtitle-style-workbench-evidence-v15`,
  HSR PR #132.
- Corrected browser run: Actions `38033568592`, job **chromium-ui** successful.
  The browser test now rejects an inspector narrower than 85% of a tablet
  viewport or one that fails to span from the left navigation column through
  the right edge of the preview column.
- Both successful browser runs use **the actual checked-out application HTML,
  CSS and JavaScript in Chromium** with **fixture API responses**. They are not
  real FFmpeg/libass renders, live-server dataset proof, or physical device tests.

## Reusable lesson

An inspector may fail to occupy its intended region even when there is no
horizontal overflow and no JavaScript exception. In a layered stylesheet,
`grid-area` shorthand precedence and `!important` cannot be inferred reliably
from a later `grid-column` source declaration alone. Assert computed geometry
of major regions at breakpoint widths and retain screenshot evidence.

This is a verified instance-level Bug. It does not modify a UIGS Canonical
rule; broader CSS specificity guidance would require cross-project evidence.
