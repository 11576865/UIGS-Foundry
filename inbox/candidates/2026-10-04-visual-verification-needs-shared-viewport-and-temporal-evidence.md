# Candidate: Visual output verification needs shared spatial viewport and temporal evidence

Date: 2026-10-04
Status: Candidate
Scope: media verification / image comparison / codec inspection

## Observation

A full-screen wipe comparator is substantially better than two small side-by-side images for subtle image differences, but a single fit-to-screen frame still hides fine codec artifacts and cannot reveal temporal defects.

## Candidate principle

A verification surface intended for subtle media-quality inspection should preserve a shared comparison coordinate system:

- zoom both reference and candidate to the same scale;
- pan both through the same image-space viewport;
- keep the wipe divider independent from zoom/pan;
- expose 100% / 200% / 400% or equivalent deterministic inspection scales;
- make reset restore both viewport and divider state.

For video, static frame evidence is necessary but insufficient. Temporal artifacts such as pumping, flicker, cadence errors, motion-compensation residue and transient ringing require short time-window evidence or multi-frame inspection.

## Suggested progression

1. shared zoom/pan on the existing authoritative frame comparator;
2. multiple timestamp sampling / inspection rail;
3. short synchronized temporal A/B around a selected timestamp;
4. objective metrics and difference visualizations only after reference alignment semantics are stable.

## Limits

This is a design candidate based on one media-verification workflow. It should not be promoted to Canonical without implementation evidence across more than one project or verification surface.
