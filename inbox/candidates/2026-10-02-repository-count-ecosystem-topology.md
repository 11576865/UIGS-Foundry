# Candidate: Repository-count asymmetry reflects task granularity and ecosystem topology

Status: candidate
Date: 2026-10-02
Domains: product-research, software-ecosystems, tooling

## Summary

A large difference in GitHub repository counts between two software domains should not be interpreted directly as a difference in user demand or technical importance.

Repository count is strongly shaped by **task granularity** and **ecosystem topology**.

Container/media infrastructure domains such as Matroska/MKV naturally generate many independent repositories because useful projects can be narrowly scoped: parser, muxer, demuxer, metadata editor, transcoding wrapper, batch GUI, server component, language binding, test corpus, Docker image, track utility, chapter tool, and format specification.

Specialized authoring domains such as ASS subtitle editing tend to concentrate functionality into a small number of integrated editors. A minimally credible editor requires a renderer, media preview, timing, audio waveform, font/style semantics, undo/history, project persistence, interaction design, file preservation and often scripting. Once a mature incumbent with an extension ecosystem exists, incremental innovation often appears as scripts/plugins/forks around that incumbent instead of new full editors.

Search discoverability amplifies the asymmetry: infrastructure projects often advertise stable format terms such as “MKV” or “Matroska” in repository names/descriptions, while ASS-related work may be filed under “Aegisub”, “typesetting”, “subtitle editor”, “SSA”, “libass”, “karaoke”, or project-specific names.

## Candidate rule

When using repository counts as ecosystem evidence:

- compare task granularity before comparing raw counts;
- distinguish infrastructure libraries/utilities from integrated authoring applications;
- search by format names, incumbent product names, domain vocabulary, renderer/library names and extension ecosystems;
- treat plugins/scripts/forks as part of an authoring ecosystem rather than counting only standalone editors;
- do not infer market demand directly from GitHub repository count.

## Evidence

A GitHub repository search on 2026-10-02 showed:
- broad MKV/Matroska results spanning specifications, libraries, muxing, conversion, servers, metadata tools and wrappers;
- “ass subtitle editor” returning comparatively few dedicated editors;
- “aegisub” returning many scripts, forks and automation repositories around the incumbent editor;
- “advanced substation alpha editor” concentrating heavily on Ameko forks;
- “samaku subtitle” returning essentially the single experimental samaku project.

This is observational evidence from one search surface, not a census of all software.

## Provenance

- source discussion: ASS-Workbench-Android ecosystem research
- evidence level: current GitHub search observation + architectural interpretation
- status rationale: reusable cross-project research heuristic, but not yet validated across many domains

This is a Candidate only. It is not Canonical.
