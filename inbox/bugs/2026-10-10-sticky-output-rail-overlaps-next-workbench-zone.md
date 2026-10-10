# Bug: Sticky single-task output rail overlaps a later batch workspace section

Status: **Bug / screenshot-reproduced, PR fix under Chromium revalidation**  
Date: 2026-10-10  
Project: `11576865/MKV-Fast-Muxer`  
PR: https://github.com/11576865/MKV-Fast-Muxer/pull/69 (Draft)  
Related issue: https://github.com/11576865/MKV-Fast-Muxer/issues/68

## Observable evidence

The content-first batch intake Chromium evidence artifact from run `38051335261` contains `mkv-container-tree-batch-desktop-1440.png`. Opening and visually inspecting this actual populated **1404px-wide** `.batch-workspace` screenshot reveals the previous single-task `.output-hub` visually intruding into the top-right batch settings/queue area. The same screenshot shows actual content-identified batch video/subtitle/font rows and a prepared batch MKV plan; the screenshot exists even though the run's Browser E2E is otherwise green.

Root-cause layout context: wide desktop `.workspace` uses a three-column grid with `.workbench-grid { display: contents }` for the single-task editing/output rail. The output rail had `position: sticky; top: 12px; max-height: calc(100dvh - 24px); overflow-y: auto`. The batch workspace follows in the grid's second row. Sticky scroll positioning allowed visual occlusion of controls in the later task zone. Prior E2E asserted overall page width and successful mux outputs but did **not** assert non-overlap of adjacent task zones.

## Fix and acceptance requirement

On the Draft PR's phase 7 branch, the desktop output rail is returned to **normal grid flow** (`position: static`, unconstrained overflow) rather than remaining sticky across a later task region. The MKV primary action remains at the top of the output rail; same task IDs and mux logic remain unchanged. A real Chromium E2E assertion checks that the output rail's bottom boundary is not below the batch workspace's top boundary at desktop width, in addition to existing real MKV mux and mobile overflow checks.

The CSS/geometry revision is source-confirmed, but its **latest-head Chromium CI is pending** as of initial intake. Do not claim a verified fix until the latest run is green. A valid alternative future solution may use an explicitly bounded sticky container within a single workbench region; this one-PR case does not justify declaring all sticky rails forbidden.

## Reuse boundary

A sticky primary-action sidebar that looks correct in a viewport screenshot may physically overlay **later independent workflow regions** in full-page or element screenshots. Visual evidence must include scrolled boundary crossings, not just page top and horizontal overflow. Real geometry assertions should cover inter-region occlusion separately from task correctness.

Dedup: searched UIGS Foundry for `sticky sidebar overlaps following section grid`, `sticky output rail batch section`, `position sticky next grid row overlay`, and `scroll capture overlapping workbench sections`. No existing Bug/Case duplicate was found. Candidate for future UI contract review only; do not alter Canonical standards from this observation.
