# Observation — Figma Android mobile browser is not a reliable authoring surface

Date: 2026-10-15
Status: Observation / user-reported friction + vendor documentation; not a Canonical rule
Domain: UI tooling, touch interaction, authoring workflow, evidence boundaries

## Trigger and observed symptom
In a first-use Figma Design workflow, the user reported that Figma in an Android phone browser is very difficult to operate, and without a physical keyboard is almost unusable for authoring. This is direct qualitative user experience, not a controlled cross-device usability test.

## Independent vendor boundary (verified 2026-10-15)
Figma's official system-requirements page states that on mobile devices users can access only a **View Only** version of Figma files; it also says the file browser is no longer supported in mobile phone web browsers. The official Figma mobile-app guide describes browsing, viewing, comments, prototype testing and desktop-frame mirroring rather than full Figma Design authoring.
Sources:
- https://help.figma.com/hc/en-us/articles/360039827194-What-are-the-system-requirements-for-Figma
- https://help.figma.com/hc/en-us/articles/1500007537281-Guide-to-the-Figma-mobile-app

## Interpretation and boundary
The reported failure should not be diagnosed merely as a keyboard-shortcut learning gap. Touch precision, canvas gestures, panel density and input-modality mismatch compound a product-support limit. Requesting a desktop website on mobile or connecting a keyboard must not be represented as restoring a supported full editing workflow. For the current user goal, create/edit Figma Design files from a supported desktop environment, and use Android for viewing, commenting, previewing and prototype testing. Remote desktop may provide desktop execution, but its phone-sized input experience is not verified here.

## Deduplication
Queried UIGS-Foundry for `mobile touch`, `Figma`, `input modality`, and `Figma mobile`; no exact prior Android-phone-browser authoring-support observation was found. Related Candidate `inbox/candidates/2026-10-02-touch-translation-modifier-key-visual-manipulators.md` covers translating modifier-key interactions into touch controls; it does not document this Figma vendor product-support boundary.

## Reuse condition
When advising about design tooling, verify whether the target device actually supports *authoring* versus only *viewing/prototype testing*, before teaching desktop hotkeys or promising a mobile workaround. Do not automatically promote this single report to a universal UI design Canonical rule.
