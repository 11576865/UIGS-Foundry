# Observation: professional ASS UI control grammar must follow semantic operands, not imitate an editor shell

Date: 2026-10-13
Status: Observation / review recommendation, not user-tested UX acceptance
Product: ASS Workbench main FIXED and independent SPATIAL_EXPERIMENTAL
Review basis: shipped offline UI prototype v5, its screenshots and HTML source; Designing Interfaces 3rd ed supplied PDF; repository WorkbenchToolCatalog and established FIXED/SPATIAL Host separation; Aegisub official ASS tags.

## Findings
An interface can pass many screenshot, routing and basic gesture regressions and still have major design uncertainty or wrong affordances. v5 visibly has six tasks and 18 searchable tool keys but discovery/accessibility does not mean professional direct operation or correct ownership. Task tabs combine different conceptual levels: '资源与检查' inventory vs evaluation, '批量与交付' destructive scoped transformation vs file output, and experimental Host belongs to global workspace selection. A narrow 'current parameters' inspector can become form-heavy rather than native editor.

The book's Canvas Plus Palette discussion legitimizes visible icons alongside canvas and grouped panels, but it does not authorize icon-only hidden discovery for specialized commands. Its dynamic-query guidance distinguishes single-value slider, paired-range slider and exact numeric input. Its animation-transition pattern emphasizes maintaining spatial orientation, short local transitions, minimal latency and avoids prolonged chains. Its hover-tool discussion notes touch has no hover: context tools are revealed on object tap. These are design-pattern guidance, not results of measuring ASS users.

## Reusable recommendation / constraints for experiments
1. Separate layers: product Host (FIXED stable vs SPATIAL experimental), user task (author/edit, timing, typesetting, effects, inspection, batch review), domain tool (18 keys), scoped commands, and field control. Do not merge MKV delivery with batch rules as one permanent editing task; put PROJECT and output alongside project/file lifecycle.
2. Visible functional affordances: immediately display focused Event identity, document time, Style/Override effective source, dirty/preview/commit, write target and primary action. Explanations can be accessed via longpress/help, but **the existence of dangerous or important actions must not depend on longpress**. A searchable 18-tool catalog is a safety net, not the only route for real frequent specialist actions. Contextual quick-access on selected objects plus discoverable task subtool chooser.
3. Control semantics: a time playhead gets continuous scrub + precise PTS/frame step; fades use two related interval boundaries plus exact times; \\t uses t1/t2 interval handles, accel as custom numeric plus presets and same ruler; coordinate x/y use direct-manipulation plus numerical nudge rather than a 0..1920 slider; scale/angle/alpha can use bounded manipulation sliders paired with unrestricted valid numeric values; karaoke uses proportional boundary editor, explicit duration vs \\kt onset differences; static fields belong to static inspector, not a fake time track.
4. Two different uses of animation: subtitle-authored animation must be renderer-backed or explicitly labeled simulation; interface transitions should be small, interruptible, visually explain containment/focus and honor reduced-motion preference. Dynamic previews, readouts, timeline, graph and playback must derive from one semantic time/state model.
5. Different screen content priority by task: event grid+raw text for editing; long aligned tracks for timing; video for placement; temporal parameter graph and properties for effects; request→resource→glyph evidence for font/QC; before/after + scope + explicit commit for batch. Tablet landscape ≠ compact portrait; never force every secondary panel into a fixed column or hide essential capabilities behind general settings.
6. Actual acceptance battery should measure: tool reachability with non-search paths, screenshot/task fit, gesture hit target sizes in Android dp, precise numeric operations, time-axis coherence, schema-faithful serialization, microinteraction transitions, state/Undo provenance and target-specific device performance. These are proposed checks pending production evidence.

## Dedupe
Related Foundry material: prior ASS v3/v4/v5 Case records production-like prototypes and limited browser checks; 2026-10-13 ASS product Host/tool taxonomy Observation covers the hierarchy separation. This new Observation is specifically about **control type and motion/visibility grammar** and does not duplicate the v5 semantic Bug.

No Canonical promotion; Android project untouched.
