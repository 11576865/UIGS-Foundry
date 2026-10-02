# Cross-project Knowledge Inventory — Pass 3

Date: 2026-10-02

## Transactional output and recovery

HSR contributes two distinct reliability mechanisms:
- **last-known-good publication rollback** for a multi-file archive rebuild;
- **integrity-checked recovery generations** for text/checkpoint recovery, including checksums, bounded package size, latest/previous generations, post-write reread validation, and compatibility-aware import.

These are related but not merged: rollback protects a published artifact set; recovery packages preserve recoverable state across damage or relocation.

## Runtime reconciliation

CVS contributes a concrete declared-vs-discovered reconciliation mechanism. It compares Runtime/Engine/Model declarations with a host inventory and reports structural drift such as missing dependencies, private dependencies with multiple owners, registered engines lacking runtimes, unclaimed runtime candidates, and conflicting PATH-visible versions.

## Long-job ownership and native bridges

Quick Automatic Hardsub Encoder contributes:
- single-owner lifecycle for long native jobs;
- foreground-service ownership independent of Activity/WebView lifetime;
- structured Native Bridge requests instead of arbitrary FFmpeg/shell command execution;
- explicit cleanup for success/failure/cancel/timeout.

## E2E recovery grammar

MKV Fast Muxer contributes product-path tests that deliberately:
- fail one job and immediately run another;
- cancel and immediately restart;
- run two successful jobs and check metadata isolation;
- switch the main input and require stale scanned state to disappear;
- audit container semantics with independent ffprobe evidence.

## New Bug Museum item

**BUG.HSR.FAILED_REBUILD_PUBLISHED_SET** records the historical reason HSR added multi-file rollback around rebuilds.

## Harvest automation foundation

A machine-readable `harvest/targets.json` now lists repositories and high-value source signals. This is intentionally an indexing/triage layer, not an automated Canonical promotion mechanism.
