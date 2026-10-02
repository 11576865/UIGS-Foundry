# Candidate: Completed artifact identity must survive changes to the current configuration

Status: candidate
Date: 2026-10-03
Domains: interface-grammar, workflow, reliability
Evidence type: state-matrix audit and implemented regression

## Summary

A verified or saved artifact belongs to the task configuration that produced it, not automatically to whatever configuration the editor currently shows.

If the user changes mode or parameters after completion, the artifact should remain recoverable while the UI clearly distinguishes it from the next task.

## Evidence

In Quick-Automatic-Hardsub-Encoder, a completed transcode could remain in `verified/saved` state while the user switched the current operation to another mode. The action label could still say “重新压制” even though pressing it would execute a different current operation.

PR #35 keeps the completed artifact available but marks it as a previous-task artifact when current settings diverge. Save actions become “保存上一成品 / 重试保存上一成品 / 再次保存上一成品”, while the run action reflects the current mode.

## Candidate rule

- bind completed artifacts to the configuration/task identity that produced them;
- changing current settings must not silently relabel an old artifact as the result of the new settings;
- do not discard a verified unsaved artifact merely because the next task is being configured;
- expose an explicit “previous result” distinction when current configuration diverges;
- save/retry operations continue to target the completed artifact until a new task supersedes it;
- execution controls must describe the current configuration, not the previous artifact;
- state-transition tests should cover configuration changes between verify/save/retry states.

## Scope

Applies to encoders, renderers, exporters, build systems, report generators, model runs, and other workflows where a completed output can coexist with preparation of the next run.

## Provenance

- source project: `11576865/Quick-Automatic-Hardsub-Encoder`
- implementation: PR #35
- evidence level: state audit plus automated transition regression

This is a Candidate only. It is not Canonical.
