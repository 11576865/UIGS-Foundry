# Candidate: Dual-channel motion extraction plus runtime evidence for Figma-to-app handoff

Date: 2026-10-15
Status: **Candidate / documentation-verified API capabilities and proposed workflow, not yet validated in user Figma file or target product**
Domain: interface-grammar, animation, design-to-code, verification
Context: User questions whether AI can faithfully implement self-authored Figma animation instead of re-guessing from image; related software: MKV-Fast-Muxer / ASS Workbench.

## Technical distinctions grounded in documented APIs

Figma has at least two distinct inspectable animation sources:

1. Keyframe/timeline motion: official `get_motion_context` MCP tool after `get_design_context` supplies animated-node inventory, keyframe tracks, easing curves, precomputed CSS `@keyframes` / motion.dev code and coordination hints; supports `recursive: true` for animated descendants. Evidence: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/ .
2. Interactive prototype transition specifications: Figma Plugin API node `reactions` includes trigger, actions, destination, and transitions (e.g. `SMART_ANIMATE`, easing, duration), including variable/conditional prototype actions. Evidence: https://developers.figma.com/docs/plugins/api/properties/nodes-reactions/ and https://developers.figma.com/docs/plugins/api/Reaction/ .
3. Visual effects and static geometry are separate design properties (fills, opacity, transforms, blurs, auto layout). A raster image alone does not contain editable structural/timing provenance.

`get_design_context` by itself should not be assumed to deliver every interactive reaction, and `get_motion_context` should not be misrepresented as covering every Figma Prototype connection. Supported plugin permissions/seat, selection, file links, prototype type and effect compatibility must be checked before claiming complete retrieval.

## Proposed handoff + acceptance (not yet executed)

- Capture **static/design context** for target components and variants.
- Capture **motion context** for animated nodes and **prototype reactions** for trigger/action/transition details, when connection permissions allow.
- Build a normalized *motion/interaction specification*: source state, target state, trigger, destination, duration, easing/curve, animated properties, layering/backdrop/scroll policy, cancellation/interrupt/keyboard and reduced-motion behavior. The designer keeps authority; do not invent unobservable fields.
- Attach a real recorded run of the Figma prototype (or direct playback) to resolve effects the structured APIs do not describe completely. Recording provides observed pixels/timing but is not a substitute for source metadata.
- Implement the motion in production components using CSS/Web Animations/Motion/JS as appropriate, keeping application domain state separate from transitions.
- Browser-test multiple frames across time + final state and user-triggered outcomes; screen-record and compare actual run against the reference, including reduced-motion/accessibility and interruption paths. Record unresolved differences instead of auto-accepting an approximation.

## Dedupe / scope

Related `inbox/candidates/2026-10-15-executable-ui-design-source-for-codebase-integrated-products.md` addresses executable design source and pixel-drift, **not** separate motion-vs-reaction API channels. `inbox/candidates/2026-10-03-generated-layer-relative-animation.md` addresses relative animation of generated layer stacks, not design-file handoff. `inbox/cases/2026-10-13-ass-v6-semantic-temporal-editor-and-stateful-prototype-evidence.md` establishes browser-verified temporal model tests, not Figma extraction.

No user Figma animation file was inspected yet, no target implementation was tested, and no Canonical rule should be changed based on this discussion.
