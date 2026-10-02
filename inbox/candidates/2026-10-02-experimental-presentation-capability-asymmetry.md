# Candidate: Experimental presentations may trade capability reachability for semantic integrity

Status: candidate
Date: 2026-10-02
Domains: interface-grammar, product-architecture, reliability

## Summary

Multiple experimental presentation hosts do not need complete feature-entry parity while they are still serving as competing UI experiments.

The hard invariant is **semantic integrity**, not identical reachability:

- one canonical domain/editor authority;
- no duplicated business implementation per presentation;
- presentation changes do not mutate domain meaning;
- Focus / Selection / Binding / Write Target / history continuity remain valid;
- save/recovery and destructive actions remain safe.

A capability may be absent from one experimental host's visible navigation or interaction surface as an explicit cost of experimentation. Missing presentation-level reachability is not automatically a defect if the capability remains available through the product's primary/reference presentation and the experimental host is not being represented as feature-complete.

## Why this matters

Requiring every new capability to be surfaced immediately in every experimental presentation turns presentation exploration into an N-way feature-parity tax. That pressure encourages either:

1. duplicated UI/business implementations;
2. rushed low-quality entry points added only to satisfy parity;
3. blocking domain progress on experimental UI maintenance;
4. abandonment of useful presentation experiments.

Separating **semantic parity** from **entry-point parity** preserves the architectural value of multiple presentations without multiplying every feature change by the number of hosts.

## Candidate rule

For products with multiple experimental presentation hosts:

- require shared canonical semantics and state invariants across all hosts;
- allow incomplete capability reachability in experimental hosts;
- keep at least one primary/reference presentation capable of reaching the complete supported workflow;
- do not infer business-logic absence from presentation-level entry absence;
- do not silently claim an experimental host is feature-complete when it is not;
- when an experimental presentation is promoted to a primary/default/release-supported presentation, capability reachability becomes part of its promotion/release acceptance criteria.

This rule does **not** relax safety, persistence, undo/history, write-target, or canonical-state requirements.

## Relationship to existing Foundry knowledge

This refines, rather than replaces, `UIGS.NAVIGATION.CAPABILITY_CATALOG`. The catalog remains useful when one capability should be discoverable from multiple hosts, but cross-host discovery is not required merely because multiple experimental hosts exist.

It also complements the presentation invariant candidates: canonical state continuity is mandatory even where visible tool coverage differs.

## Provenance

- source project: `11576865/ASS-Workbench-Android`
- discussion context: multiple UI presentations already share the same canonical editor/workspace boundaries; user explicitly accepts incomplete new-capability entry coverage as the cost of preserving experimental UI diversity
- evidence level: design decision / project observation; not yet a cross-project canonical rule

This is a Candidate only. It is not Canonical.
