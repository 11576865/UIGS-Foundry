# Candidate: Imported resource metadata must separate intrinsic semantics from destination policy

Status: **Candidate / implementation-backed engineering observation**  
Date: 2026-10-04  
Project evidence: `11576865/ASS-Workbench-Android` PR #113

## Observation

When importing a resource from one container/workspace into another, not every source metadata field has the same semantic ownership.

The Matroska Track import flow exposed a concrete split:

- fields such as language identity, forced status, accessibility/disposition meaning and commentary/original semantics describe the imported Track itself;
- the Default flag participates in the destination container/player's automatic selection policy.

Blindly copying every source field therefore conflates **resource semantics** with **destination policy**. Blindly resetting every field loses meaningful resource metadata.

## Candidate rule

For cross-container or cross-project resource import:

1. Classify metadata before choosing import defaults:
   - **intrinsic/semantic metadata**: describes what the resource is;
   - **destination-policy metadata**: describes how this destination should prefer, select, route, surface or activate the resource.
2. Preserve intrinsic semantic metadata by default when the destination format can represent it.
3. Do not silently inherit destination-policy values when doing so can change the target project's behavior. Start from a neutral destination default or require explicit confirmation.
4. Present the distinction in the import UI instead of collapsing every field into an undifferentiated metadata form.
5. Persist the user's resolved destination values in the mutation plan and verify those exact values after output generation.
6. Keep source provenance separate from destination identity; imported objects may receive fresh destination IDs while retaining semantic metadata.

## Implementation evidence

ASS Workbench PR #113 applies this to Matroska Track import:

- `Name`, legacy `Language`, `LanguageIETF` / BCP 47, `FlagForced`,
  accessibility dispositions and Original/Commentary are inherited as editable defaults;
- `FlagDefault` starts disabled because automatic track selection is destination policy;
- imported Tracks still receive fresh destination TrackNumber / TrackUID;
- output verification checks the resolved metadata after remux.

## Evidence boundary

This is implementation-backed by one Matroska workflow. Other formats and resource types may classify individual fields differently; for example, a field that is intrinsic in one domain may be destination policy in another.

Do not promote to Canonical from this evidence alone.
