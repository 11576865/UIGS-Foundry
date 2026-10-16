# Bug — R3 ASS style-reset JVM fixture contains double ASS backslashes

Date: 2026-10-16
Status: **Fixture correction committed / post-fix CI Pending**
Product: https://github.com/11576865/ASS-Workbench-Android
Draft PR: https://github.com/11576865/ASS-Workbench-Android/pull/149
Validation run: https://github.com/11576865/ASS-Workbench-Android/actions/runs/38888581101
Validation job ID: `116932661298`
Prior tested HEAD: `77ed585480bea5510ee23ff54612e9bb4f748b38`
Scoped fixture repair: `ca71cbb007ed0af60d7d6b212d4d2da3cc4bb447`
Durable task checkpoint: `b192b61a7499183d84c80e5111bd00cbb944768f`

## Actual failing evidence
The FIXED V1.1 Branch Validation workflow run #38888581101 confirmed **SUCCESS** of the Android Kotlin compilation and AndroidTest Kotlin source compilation step. This was the first external successful compile after repairing `BoxWithConstraints.maxHeight` receiver errors. The subsequent `:app:testDebugUnitTest` failed: **261 tests completed, 1 failed**, `R3WriteSourceDetailsTest.styleResetRetainsTruthfulEventStyleBaseline`, assertion at line 65 `assertNotNull(summary)`. No production ASS issue was established.

Read `app/src/test/kotlin/io/github/assworkbench/app/ui/R3WriteSourceDetailsTest.kt`: the STYLE-reset source case contained four physical backslashes before the `rAlternate` tag and before `fs52`, e.g. Kotlin source `"{\\\\rAlternate}"`, which creates two literal backslashes at runtime rather than the one ASS override delimiter the semantic inspector expects. The test's fixture was therefore malformed for its intended valid-style-reset scenario. A separate malformed/invalid ASS path already has a test and the source inspector correctly fails closed.

## Scoped correction
In only the method `styleResetRetainsTruthfulEventStyleBaseline`, changed three over-escaped tag occurrences from four physical Kotlin source backslashes to two, resulting in valid ASS `\\rAlternate` and `\\fs52` at runtime. Did not alter any production ASS parser, `AssEffectiveInspector`, `r3WriteSourceSummary`, assertions, edit state or SPATIAL sources. The expected existing assertions remain in place (styleLabel Opening, effective reset 24, draft 52).

**Important proof boundary:** Committing a corrected test fixture is not proof the entire suite passes. The post-fixture head run was not polled in the same development unit, per async-CI execution boundary. Kotlin compile success pertains only to the prior tested SHA; next task is to inspect the next authoritative exact-head CI result, then take emulator/real inspector tests if green.

## Generalizable observation, bounded to one failure
When Kotlin source embeds another language's escape syntax (ASS override blocks, JSON string payloads, regexes), distinguish source-layer backslashes from runtime-language delimiters. A test intended as a valid example can inadvertently become a malformed negative fixture, producing a `null` result under correct fail-closed production behavior. Document actual character counts before loosening assertions or modifying parsers.

## UIGS governance
Foundry search for `R3WriteSourceDetailsTest style reset fixture double escaped ASS backslash test failure`, `ASS Workbench CI 38888581101 261 tests one failed malformed rAlternate fixture`, `ASS Kotlin text ass style reset source attribution test fixture backslash` produced no matching prior Bug. Adjacent earlier CI receiver-scope Bug is different. **No Canonical changes; Pending post-fix verification.**
