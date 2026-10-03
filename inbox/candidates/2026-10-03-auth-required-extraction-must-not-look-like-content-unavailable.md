# Candidate: Authentication-required extraction must not look like content unavailability

Status: candidate
Date: 2026-10-03
Domains: reliability, extraction, interaction-state
Evidence type: troubleshooting observation

## Summary

When an extractor fails because a source requires an authenticated session, the product should distinguish that condition from “content unavailable”, “no subtitles”, or generic extraction failure.

## Candidate rule

- model unauthenticated, authenticated-required, authorization-denied, unavailable, and extractor-failure as distinct states;
- when the user already has legitimate browser access, prefer an explicit browser-session handoff such as cookies/session import rather than encouraging credential re-entry inside the tool;
- do not claim subtitles or media are absent until the authenticated extraction path has been attempted when the source requires login;
- expose retry after authentication refresh;
- warn that session cookies are sensitive credentials and should not be shared or persisted casually;
- when upstream platforms introduce additional attestation requirements, report that separately from ordinary login failure.

## Provenance

- troubleshooting an age-restricted YouTube subtitle extraction failure
- evidence level: general extraction workflow observation

This is a Candidate only. It is not Canonical.

## Follow-up implementation evidence

A standalone Windows subtitle-grabber wrapper was implemented around yt-dlp using this state split:

- normal/default extraction;
- authenticated extraction via browser session cookies;
- automatic retry with a different YouTube client when age/login/403 symptoms indicate a client-specific path;
- explicit distinction between authentication failure, PO Token / 403 attestation failure, no matching subtitles, browser-cookie access failure, and generic extractor failure;
- browser cookies are handed directly to yt-dlp rather than exported or persisted by the wrapper.

This reinforces the Candidate and adds one practical refinement:

- client fallback is a recovery action, not evidence that authentication or attestation requirements disappeared; if fallback also fails, the UI/CLI must preserve the more specific failure class rather than collapsing back to “download failed”.
