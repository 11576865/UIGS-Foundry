# Candidate: Executable UI design as the production presentation source for app-specific redesigns

Date: 2026-10-15
Status: Candidate / workflow proposal, **not demonstrated as a completed production redesign**
Domain: interface-grammar, engineering-process, visual-evidence
Motivation: 软封10.14版本 Matroska object-centric redesign, authority PR https://github.com/11576865/MKV-Fast-Muxer/pull/153

## Trigger

The user found that a visually appealing rendered concept image did not constrain the actual implementation: natural-language retelling of a PNG plus DOM rehosting led to different layout density and information hierarchy, even with successful browser E2E. The proposed corrective mechanism is not a second image, more narrative instructions, or purchasing another design plugin.

## Proposed workflow (not yet validated)

For a codebase-integrated, interaction-rich product where design-tool API plans/costs obstruct iteration:

1. Author a **runnable responsive design prototype in the same presentation technology the product will ship** (HTML/CSS/JS or stable framework components). Treat it as design authority, not throwaway demonstration.
2. Store design tokens, component hierarchy, tested responsive constraints and entry-manifest IDs in version-controlled code; screenshot evidence is an output of that source. Do not use unstructured image generation as the only layout contract.
3. Ensure even unimplemented planned actions have **honest, inspectable capabilities** (planned/available/guarded/read-only/blocked); UI must never claim real Matroska remux or persistence before actual output evidence.
4. During implementation, **reuse the reviewed presentation components unchanged** and adapt their data/events to existing domain capabilities through a thin, tested adapter. Avoid re-describing a raster mockup to reimplement a visually different DOM.
5. Review real Chromium screenshots at fixed viewports and representative populated/empty/error/batch states; run actual-media tests separately. Do not infer UI quality from green functional E2E.
6. Complete one cohesive release cutover after exact-head visual+functional verification; intermediate branches/commits are not public product versions. Do not create another canonical business store.

**Caution:** A coded prototype is itself susceptible to poor design; it must still receive visual review. Keeping its components is not a guarantee of usability, accessibility, or code maintainability. The approach requires separating view-only prototype fixtures from authorized production state and avoiding two concurrent rendering authorities.

## Related Foundry entries (dedupe)

- `inbox/cases/2026-10-15-softmux-1014-e2e-green-visual-hierarchy-rework.md`: observed code/UI screenshot hierarchy failure despite green E2E.
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md`: output composition is the main product object (not duplicated input/edit/output lists).
- `inbox/candidates/2026-10-15-version-vector-and-atomic-ui-cutover-gate.md`: full-version cutover with a single authority.
- `inbox/candidates/2026-10-02-ui-requirement-evidence-traceability-ledger.md`: test/evidence state separate from implementation completeness.
- `inbox/candidates/2026-10-03-presentation-density-state-continuity-by-stable-component-identity.md`: preserving one semantic component identity across presentation changes.

The new narrow proposal is **the executable production presentation as the design artifact, avoiding repeated image-to-prose-to-code translation**. It is not a claim that the already submitted #153 implements this new strategy: that PR used rehosting, which remains unaccepted visually.

## Validation gap

Requires an actual implementation showing (1) reviewed editable/executable UI components reused in product, (2) full entry completeness, (3) actual browser visual comparisons and media-output regressions, and (4) no divergent domain authorities. Until demonstrated, retain Candidate only; no Canonical changes.
