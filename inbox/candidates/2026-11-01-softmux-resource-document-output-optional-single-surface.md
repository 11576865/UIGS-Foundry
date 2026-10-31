# Candidate — Content-first Matroska workbench: optional output, no implicit primary MKV, explicit membership and preview provenance

Date: 2026-11-01
Status: **Candidate / UX-domain hypothesis, user scenarios but no UI or runtime acceptance**
Product: `11576865/MKV-Fast-Muxer`
Owner input: mixed-file and multiple-MKV drag, unused/wrongly imported assets, no-MKV creation, source vs target preview, independent choice among multiple subtitles; the owner explicitly asks whether a “主件 + 待加入” scheme is valid and whether a simpler single surface exists.

## Problem, not a decided UI

The previously proposed “one source MKV as principal + other files as awaiting addition” rule fails with multiple MKVs, unattached or never-used imports, source-only inspection, and no-source Matroska creation. “Every imported file goes into an output draft” also wrongly equates import with inclusion/export. Content-first classification, selected object, composition authority, and eventual export are different axes.

## Candidate model

- **Resource inventory**: all imported external File objects and scanned source-container resources, with stable identity and provenance. Import is observation/access, never a persistent output membership grant.
- **Active document view**: one focused source MKV or an unsaved prospective Matroska composition, selected for inspection without implying any write. Multiple MKVs remain independent, inspectable sources; source focus must not silently assign “primary output”.
- **Optional target plan**: immutable-source, mutable-intent draft made on an explicit composition/export operation or unobtrusively presented as an *unsaved candidate* for file-only creation. No output is required for inspection. The main surface may project either the active source or target without duplicating writable state.
- **Per-target per-object membership**: imported/available, proposed included, deliberately excluded from output, or unsupported/uncertain. “Unused” is not a file error and does not mean removed from the workspace. A source MKV may contribute only selected tracks/attachments. One resource may have different roles across multiple output plans. Distinguish `remove from imported session`, `exclude from this output`, `remove source member from proposed output`, and `delete physical file` (not allowed).
- **Contextual preview**: each ASS file (including unselected alternatives) can be examined separately with its own source identity; selecting a subtitle/track changes preview content, not output membership. A subtitle without video can preview against a neutral/test canvas within supported renderer limits. Preview of source, simulated planned composition, and independently examined real exported output must be labeled distinctly; a composition display does not prove output was generated.
- **Multiple MKVs**: opening each for inspection is the default, no auto-merge, auto-concatenation, or first-MKV-as-master writer authority. If the user requests combination, identify a destination plan and selected object contributions; if many outputs are intended, make separate output plans / a batch matrix. Source-to-output mapping must be explicit when ambiguous.
- **No MKV**: show an empty virtual target document or a candidate newly constructed composition; classify ordinary media into supported tracks and unrelated files into attachments only under a transparent rule. File inclusion is draft and cancelable. A no-track attachments-only output is non-playback Matroska as distinct from an encoded still video.
- **Single-surface proposal (not a 3-workspace mandate)**: a central current-document/target composition tree, contextual selected-object inspector + preview, small collapsible source inventory/unused resources tray and clear action/save area. For existing MKV unedited inspections, no mandatory “create project”/output setup. For target edits, show source vs proposed differences. No input-before-type questionnaire or multi-step mode gate.

## Falsifiable interaction scenarios

1. Drop one existing MKV only, browse internal tracks/font/chapters, close without export. No output plan or file write is forced.
2. Drop MKV A + MKV B. Both inspectable, none implicitly merged or reclassified as “added extras”. After explicit selection, add exactly one subtitle track or attachment from B to target based on A, retaining independent source identities. Reject unverified unsafe writes.
3. Drop MKV + three ASS. Preview each independently; only one selected for output; others remain in source inventory without error indicators. Changes to preview selection must never silently change included subtitle track.
4. Drop MP4+ASS+TTF+PNG. Create a candidate Matroska with known track/attachment roles, preserve original subtitle/font workflow; show output intent separately from source truth.
5. Drop PNG+PDF only; show previewable selected asset and draft non-playback Matroska membership; on explicit export, produce a valid Matroska, then independently extract PNG and PDF and compare hashes.
6. Drop wrong file. `Remove import` releases session reference (if no active dependent operation); `Exclude from output` leaves asset in inventory; removing an original source track from output never changes original source bytes; Undo restores plan intent.
7. Drop 2 MKVs plus episode subtitles; distinguish inspect independently, one combined output, or N separate outputs without prematurely forcing these choices at import time.
8. Source preview vs plan preview vs generated output audit report show unambiguous evidence labels; no fake “final MKV preview” for unrendered composition.

## Dedupe / supporting prior Foundry material

- `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md` establishes imported identity vs task role and ambiguous source selection; this candidate adds *no mandatory primary*, per-target membership, unused-resource semantics, and optional export.
- `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md` establishes composition-focused presentation and avoidance of duplicate three-panel object views; this candidate explicitly allows *source-only inspection without prospective output* and tests multi-MKV semantics.
- `inbox/candidates/2026-10-12-orthogonal-product-dimensions-not-navigation-destinations.md` establishes A/B/C/D as non-peer UI destinations; this candidate formalizes source/document/target relations and evidence labels for multiple subtitles/target preview.
- `inbox/candidates/2026-10-12-legacy-capability-migration-and-document-plan-batch-queue.md` already separates multi-source single output versus multi-output batch.

These are preexisting **research Candidates**, not approved UI. Product `src/output-composition.js` remains a read-only projection over legacy state as of `main@36f71dc9ae80a4e0b463de51d2f3aa2edae64c02`; neither a general no-video writer nor actual one-surface UX is proven by this entry.

## Next evaluation

Paper/prototype test against all eight scenarios, particularly the four distinct remove/exclude operations and subtitle source/plan preview identity. Then implement a bounded vertical task using current handlers and real Chromium artifacts, measuring mistaken auto-inclusion, accidental source reassignment, navigation/focus loss, and operator understanding. Do not replace existing user-approved scopes or automatically modify Canonical from an untested proposal.

**Pending:** owner selection of view/role semantics; UI implementation, real-device proof and runtime acceptance.


## 2026-11-01 follow-up: resolve "主件 + 资源库" combinatorial complexity through virtual per-target references

New owner design scenario: all imported inputs go into “资源库”, an MKV may be the open main document or—if no MKV—an automatic proposed output; when A/B/C/D.mkv are present, user may copy selected nested objects of A into the intended outputs based on B, C and D. Owner explicitly questioned where A’s object should live, whether to pre-extract it, whether move should erase A, whether B’s edited copy is another resource, and how to avoid combinatorial interaction complexity. The owner rejects video concatenation as an invented task outside intended scope.

### Refined candidate (owner has not approved)

**UI:** one active document surface with a source/library browser and context inspector. “主件” is reframed as **current open document / virtual output composition**, not a privileged physical original. Model C’s provenance, object membership and optional output underpin model A’s simple UI; they need not appear as three separate pages.

**Data semantics:**
- Keep exactly one imported source identity per original File and its scanned nested items. Do not implicitly extract or reify a Matroska member as a separate uploaded file merely to make it selectable.
- A nested member is referenced by a stable tuple of **source File identity + source container object/track identity + any necessary byte/time/format constraints**. A target draft can hold a *reference intent* to this object, not a duplicated payload. The same source object can be selected for several target documents independently; output bytes are written only at explicit execution.
- Opening B without modifications shows *actual source* B. Editing it produces an in-memory B* plan, displaying inherited B objects plus any selected external sources; the original B File remains unchanged. B* is not a new imported file; after explicit export it creates a distinct MKV artifact (unless a separately approved replacement operation is designed). The exported result does not silently become an input source; importing or using it again requires explicit user action.
- Multiple possible targets can retain separate per-target unsaved plans. One target is active at a time. Selecting/viewing A's member should not silently change B* output membership or create a target plan.
- **No “move” required initially**. Moving bytes/objects between real MKV sources would imply writing two files; present addition to one target and exclusion from another as distinct non-destructive operations, and preserve original file(s).
- **No MKV input**: show an unsaved virtual new Matroska with proposed recognizable contents, each inclusion editable before output; preview is of recognized input or planned composition, not generated final container. No export remains normal.
- **One MKV**: auto-open it for inspection, no output unless changes/export. **Multiple MKVs**: library selection determines which source is opened; importing does not auto-merge. For a cross-source add operation, default destination is currently active B* where unambiguous, otherwise ask to choose explicit target *at the action*.
- Wrongly imported file: removing it from session should not delete disk data; if referenced in any drafts, show dependent target(s) and require a safe decision. Removing a member from B* only edits the plan.
- Subtitle preview: select any standalone or embedded subtitle from source browser and preview independently of inclusion; preview selection never silently toggles output membership.
- Support restriction: referencing an A media track in B* does not prove a legal/common-timebase writer path; unsupported cross-container stream operations must be blocked or labeled unavailable. Attachments-only export remains a separately bounded writer capability.

### Acceptance thought experiments

1. A/B/C/D imported. Open B → no outputs. Choose A nested attachment → Add to current B* → inspect source A unchanged, source B unchanged, B* displays only a *pending* addition, no duplicate extracted A file.
2. Use the same A attachment in C* and D* without spawning duplicated source rows; independently export B*, C*, D* to distinct physical artifacts.
3. Deselect A object from B*, leave it in C*: only B* plan updates; A original and C* untouched.
4. Wrong-file removal with 2 active draft references produces a dependency-aware action (cancel/remove dependent intents); no implicit disk deletion.
5. Switch B* → inspect A → return B*: preserve B* drafts and selection; no automatic inclusion from preview click.
6. Without input MKV, show a provisional draft container from PNG/PDF and only create actual Matroska on explicit export.
7. Cross-container video concat is excluded from these tests: owner explicitly says it is not an expected function.

Deduped against this Candidate's earlier optional-output + per-target membership model, and `inbox/candidates/2026-10-11-mkv-composition-as-primary-ui-object.md`. This is a refinement, not a second product identity or a Canonical rule. No implementation/UI tests performed; owner-facing interaction and technical cross-container writer envelope remain **Pending validation**.

## 2026-11-01 owner correction: a local file relation model cannot integrate inherited capabilities

Owner explicitly rejects the idea that resource library + current document + plan refs solves the real product. Rendering, fonts, batch, identity, recovery and validation may each work in isolation while creating conflicting UI, state ownership and cross-cutting workflows. Integration and migration decisions (reuse, refactor, contextual hide, retire) are the missing tested design contract.

### Verified source evidence

The uploaded 2026-10-12 软封工程_未来规划总决议 already provides L-001–L-044 migration decisions (§4), A/B/C/D interactions (§5), document identity (§6), batch rules and Group font subsetting (§7), and object-based UI (§9). Thus the project does NOT lack conceptual plans; their actual integrated execution and UX evidence is insufficient.
- Current main src/container-document.js: explicitly read-only projection over legacy inputs, not full write authority.
- Current main src/container-target-draft.js: describes a no-video target but reports LEGACY_VIDEO_ROOT_REQUIRED for actual old writer.
- Current main src/live-container-workspace-authority.js: an existing shared immutable ContainerProject for bounded source/external changes; do not falsely assert no state integration.
- Current main src/batch-runner.js, src/batch-job-plan.js and src/batch-mux-context.js: an already real DOM-free frozen queue and explicit batch execution context. Do NOT repeat historical claim that batch still runs by simulating a click. The batch nevertheless requires video + subtitles in the job policy, and has separately scoped font plans.
- Current index.html: subtitle preview selector, font mode selector and batch group font scope are present; their existence does not prove that source vs target vs actual-output preview and shared fonts interact correctly.

### Candidate integration-contract audit

For each inherited behavior record its triggering context, resource/target/job ownership, dependencies, actual inputs, output effects, scope defaults and overrides, render or writer capability, reversibility, UI location, and exact real artifact acceptance. Avoid reducing the original-version question to a 44-item tally; that ledger also includes later features and historical UI internals.

Specific contracts to test:
1. Reuse ASS/SSA libass and timeline preview, but refactor its binding to explicit source subtitle/target subtitle/finished output identities. Previewing any candidate does not include it in the output; effective font sources (embedded, uploaded, target-selected) are visible and constrained.
2. Reuse font sniffing, alias matching, glyph coverage, HarfBuzz subsetting and hashing; refactor their input scope to target/job and subtitle binding. A shared cache for Group subset calculations does not mean every target carries identical font bytes. Keep original font policy visible only in applicable subtitle contexts.
3. Preserve low-friction video+ASS+font one-output use; do not force a special app mode. Reuse stream copy, compatibility gates, report and save mechanisms.
4. Preserve batch pairing, ambiguity guard, reviewed recipes, frozen queue, per-result audit/save semantics. Reconcile per-job overrides with single-job object inspection; changing focused source or globally selected preview cannot mutate running frozen jobs.
5. Contextually show technical chapter/tag checks, preview, group font subsetting, batch status; retire redundant 01/02/03 workflow gates, duplicate editable track views and already replaced hidden-DOM execution paths *only after equivalence evidence*. No user-facing capability removal without explicit owner approval.
6. Cross-source selection or copying an internal object into another target is a requested composition intent, not automatic extraction nor proof of writer support. Preview, plan, final artifact and saved file are distinct evidence.
7. True move across source MKVs, video concatenation, and arbitrary format edits are not implied by importing several MKVs.

### Minimum conflict demonstrations

A. Import 12 episode MKVs, 12 ASS, 30 fonts, one Group font scope; preview alternative EP07 ASS without auto-inclusion, change only EP07 font/subset override, run queue, ensure EP01 and other jobs remain unchanged. Inspect independent final MKV font attachments.
B. Import MKV A and B; preview A embedded subtitle with A attachments; inspect B target with different effective font set; inspect generated B artifact separately. No accidental silent font fallback.
C. Change imported resources while one target has unsaved edits and the batch has frozen/running jobs; assert stable source bindings, no inherited global font policy, no corrupt existing results.
D. Remove a font referenced by two target drafts. Show dependencies, do not silently remove or replace; deletion from session is distinct from output exclusion.
E. Regress old single video+ASS+fonts operation with no additional forced steps and a view-only MKV session with no output.

Recommendation: do not ratify final A/C or single-screen UI before this cross-capability conflict ledger and actual interaction tests. The unit of evaluation is a complete vertical task crossing multiple capabilities, not one locally elegant diagram. Candidate-only, no Canonical promotion or product code change, user/product validation PENDING.

## 2026-11-01 meta-correction: locally defensible possibilities silently become global product obligations

Owner observed that the design again “自我崩溃”, similar to repeated previous project discussions, and asked for a causal account and possible compromise. **Do not assume** either feature count alone or one wrong UI layout causes this.

Proposed mechanism, not yet experimentally demonstrated:
1. Assistant responds to one input ambiguity with several optional edge cases (e.g., two MKVs -> video concatenation, or cross-source member selection -> universal multi-target editing), although the owner did not request them.
2. Subsequent responses treat these invented possibilities as if their support were a requirement; local simplification (e.g., “resource library + current document + draft”) is then asserted to cover the entire product without cross-feature checks.
3. Existing subtitle rendering/font subset/Group batch/legacy interface and real writer constraints introduce contradictions, triggering more unapproved abstractions, gates and accepted-sounding plans.
4. A well-formed theoretical model or a complete-looking acceptance document can mask unresolved user value, implementation authority and artifact evidence. Even earlier comprehensive 2026-10-12 migration docs did not settle these interaction choices.

Existing deduplication and evidence:
- Cross-project goal drift already exists in `inbox/candidates/2026-10-14-agent-generated-next-units-goal-drift-guard.md`, including generated next-unit suggestions becoming task authority. This note adds a *pre-implementation conversational requirements promotion* failure, not duplicate code queue drift.
- `inbox/observations/2026-10-12-qhe-feature-growth-and-unresolved-product-identity.md` records that user specifically placed inadequate understanding of media fundamentals above mere feature growth; do not blame all complexity on over-featured design.
- `inbox/observations/2026-10-20-softmux-scope-vs-executable-release-contract.md` warns against treating assistant-generated S01–S14 proposal as owner-approved.
- Existing current Candidate section already documents the real code and cross-feature integration conflicts.

Proposed mitigation to test (not normative):
- Classify each discussed idea as **owner requirement**, **necessary consequence of confirmed use case**, **candidate design**, **speculative edge case**, or **explicitly excluded**. Only first two may constrain the near-term implementation. An AI-generated possible use case is not an approval.
- Establish an explicit *extension cost*: what original user task it makes possible, what existing operations it changes, what it forces to be verified, what it delays; do not exhaustively enumerate all conceivable uses.
- Prefer the minimum independently useful feature *subset*, not a universal hypothetical UX with every possible combination. Keep old verified subtitle+font functionality; focus generic attachment/no-source creation and inspect-only as owner-rooted paths; advanced cross-MKV copy only where tested; move of source data and media concatenation not implied.
- One product may expose different contextual task scales (single document, batch) over shared lower-level services; **one screen, one universal mutable state, and one backend need not coincide**.
- Prevent hidden correctness regressions through independent output validation scoped to *claimed* operations; owner should arbitrate product value, not be forced to discover invisible bugs.
- Run a limited set of high-collision real user journeys, including ASS preview vs inclusion and Group font subsetting vs per-output overrides, before asserting a candidate UI is integrated.

A useful established software-design comparison is D. L. Parnas, *Designing Software for Ease of Extension and Contraction* (IEEE TSE 1979; DOI 10.1109/TSE.1979.234169): minimal useful subsets and modular interfaces avoiding system-wide uses dependencies, **not** maximal abstract generality. This source supports the general architecture principle, not the project-specific causal attribution.

**Status:** Candidate hypothesis based on user corrections and inspected code/docs; owner has not approved a product rewrite, alternate delivery contract or Canonical policy. The 2026-11-01 owner feedback is a legitimate counterexample to prematurely declaring any single UI model “solved.”

## 2026-11-01 owner tactical scope concession: manual repetition may substitute for integrated batch

User explicitly reevaluated the batch feature: for a personally used tool, manual repetition may be sufficient; batch primarily removes repeated actions, and tactical inconvenience is acceptable if this makes the project tractable. This is a **proposed prioritization tradeoff**, not a confirmed authorization to delete previously delivered batch behavior, historical feature requirements, or all tests.

Key distinction: **feature retention / UI salience / generalized cross-feature integration / first-release acceptance priority** are separate decisions. Present code already has a DOM-free frozen queue, job planner, batch font policy and actual-output checks; discarding this completed work is not equivalent to declining to generalize it. A bounded legacy batch can remain available and tested as a secondary, scope-limited convenience while general Matroska composition and inspect-only work are built and verified primarily through single-target flows.

Proposed smallest viable integration scope (Candidate):
- Develop generic resource observation and optional Matroska output for **one active target at a time**. For separate B, C, D outputs, user may deliberately repeat open/add/inspect/export, without first designing simultaneous multi-target drafts, batch cross-source object distribution, multi-job preview/font overrides or automatic repair.
- Reuse the existing individual stream-copy mux, ASS renderer, font identity/subset functions and artifact verification. Keep single-target operations short and continuous; reuse previously chosen files/settings only where exact resource identity and explicit choices remain valid. Avoid creating a new 'lightweight batch' abstraction that recreates the same ownership problem.
- Keep existing batch code and user-visible legacy capability insulated from generic workflow rewrites, with regression and safety checks, but temporarily **do not promote every new general container operation to batch support**. An unsupported operation in batch must be explicitly unavailable, not silently omitted.
- A feature may be **contextually hidden** from general work without being removed; no unannounced retirement of existing user promises. If formal S10 / L-032–L-037 release commitments need altering, obtain owner approval and modify the actual product contract separately; archived candidate planning is not automatically authoritative.

Decision rule to test: compare the *real repetitive user cost* of an individual task against the *additional integrated development, feature-interaction testing and maintenance cost* of batching it. Include the owner's actual frequency and tolerance; do not use one universal efficiency slogan. Functional necessity and automatic repetition savings are not equivalent priorities.

Falsifiable tests:
1. Import A.mkv + external subtitle + font, preview and export, repeat for B.mkv; draft/preview/source identity must not silently bleed between outputs, and steps should remain comprehensible.
2. Existing supported batch recipe still generates two independently verifiable results with correct font and subtitle assignment, even if newly generalized operations are explicitly unsupported.
3. Mixed unknown and multiple-MKV input can be viewed without mandatory creation of batch jobs.
4. Batch-specific Group font setting and queue lifecycle do not become global single-target state.
5. Inspect-only input, including multiple MKVs, never silently creates output jobs.

Dedup: existing Oct 12 legacy batch Candidate covers preservation and the historical queue; earlier sections of this Nov 1 Candidate cover interaction complexity. This addition captures the owner's **tactical willingness to accept repeat work** as a way to prevent premature cross-feature integration, rather than proposing duplicate batch architecture.

Status: Candidate, pending owner decision on *which* batch feature changes are authorized; current MKV-Fast-Muxer source and Canonical scope unchanged. No real usability cost measurement yet.

## 2026-11-01 decision convergence: stop expanding the question inventory

Owner said the original aim was to clarify Softmux but repeated discussion made its identity more obscure, and asked which remaining decisions actually require owner tradeoffs.

Stabilized owner-rooted product description for review: file-import-first Matroska inspection and bounded composition; inspect-only has no export; optional output is always Matroska; source-MKV and new non-video container are both valid entry contexts; existing professional ASS/font actions are contextual, not separate app identities; mature batch behavior can remain but owner permits tactical manual repetition and does not require generalizing every new action into batch. These are user-expressed purposes; they do not constitute full acceptance of a new UI or an unbounded writer.

Avoid posing all technically possible edge cases as owner questions. The remaining *high-leverage* choices requiring explicit owner adjudication are:
(1) multi-source operation scope in first usable generic version: view multiple MKVs and individually edit with external loose files vs also transferring selected embedded tracks/attachments from MKV A into B, which substantially changes writer/identity/verification scope;
(2) modification envelope for source MKV: existing supported track/attachment edits + bounded proven writer; complex Chapters/Tags and unknown structure as inspect/read-only or fail-closed vs a mandate to support broader arbitrary structural modifications before first release.
The proposed low-risk default for input handling is one MKV auto-opened, multiple MKVs remain separately selectable, zero MKVs show prospective unsaved Matroska; external files are recognized, inspectable and not silently included in an existing source output. For a new target, recognizable input files may be presented as a proposed default membership with explicit inclusion status. This default should be tested, not assumed approved.

Only after these choices, run real legacy subtitle/preview/font and multi-input UX regression; do not require owner to choose layouts, internal model classes, batch queue mechanisms or speculative media concat/move tasks before seeing evidence. Distinguish product intent, testable UX hypothesis, actual implemented main state, and future scope. No Canonical/product contract update or code change authorized here.

Status: Candidate refinement; the owner-facing selection and real UI/engine tests are PENDING.

## 2026-11-01 concrete repository crosswalk and limited Chromium interaction pilot

Product evidence was inspected and captured as **draft research PR #206**, branch `research/softmux-user-flow-integration-audit-20261101`, commit `eefc39eba0bd459de4e6a592b468e93cb2612712`, document `docs/research/softmux-user-flow-integration-audit-20261101.md`. No product source, release contract or Canonical changed.

Verified connector source observations from product default branch:
- `src/asset-intake.js:resolveImportedRoles`: one container becomes selected primary, multiple containers require primary choice. This is execution role, not free source viewing.
- `src/asset-intake.js:classifyAssetBytes`: unknown file type -> UNSUPPORTED, not automatically a Matroska attachment; ordinary PNG/PDF generic attachment intake is missing.
- `src/output-composition.js:buildOutputComposition`: all already selected external subtitle/audio tracks and chosen fonts have `included: true` in plan projection, making independent candidate preview vs target membership a genuine seam.
- `src/main.js:refreshSubtitlePreview`: requires `videoInput.files[0]`, uses `selectedSubtitleTracks()` and global `selectedFonts()/fontMode`. Existing ASS preview is real and valuable, but *standalone unselected subtitles without video* are not currently independently previewable.
- `src/container-target-draft.js:resolveLegacyTargetCapability`: non-video target projection yields `LEGACY_VIDEO_ROOT_REQUIRED`.
- `src/batch-runner.js`, `src/batch-mux-context.js`: frozen DOM-free queue already exists; preserve it without generalized batch expansion.
- Reviewed owner-approved 2026-10-12 historical L-001–L-044 migration decisions and new Nov 1 tactical concession for manual repetition.

A **separate, nonproduction single-HTML interaction prototype** `softmux-interaction-study-20261101.html` was created in this conversation. It uses **explicit mock MKV members**, no actual EBML/ffprobe parsing, no real libass/HarfBuzz, no output writer; local user file selection is *extension-based demonstration only*. Chromium Playwright `set_content` interaction exercised: multiple MKV initial no-current document; open B; create B draft; choose alternate ASS without automatic inclusion; explicit add/exclude; PNG/PDF-only new target; inspect-only output disabled; no JS errors. This is **behavior-prototype evidence only**, not product integration or a successful real MKV task. Direct file:// page load was blocked by the test environment; test used browser set_content instead.

New falsifiable distinction: a content-first importer may coexist with still role-bound preview and automatically included external subtitles. Therefore adding a generic resource list alone does not make preview/inclusion independent, and adding a no-video target representation does not enable output. The four integrated user jobs J1 old ASS/font, J2 view-only source and multiple MKVs, J3 PNG/PDF attachment-only actual output, J4 multiple ASS candidate preview vs chosen inclusion are specified in PR #206.

Status: **candidate-level evidence extension**; production runtime and real media verification for the new behavior remain PENDING. Do not raise this to a Canonical rule or claim the user selected a final UI.

## 2026-11-01 correction: non-mandatory output is not a separate “inspect-only feature”

Owner explicitly rejected the assistant's PR #206 framing: “只查看不是一个功能。你打开游戏，看了看主菜单，然后关闭了游戏，这个游戏有查看主菜单功能吗？” This is a sharp counterexample to *feature reification*: an ordinary consequence of opening a document and not invoking output was promoted into a separate J2 use case and “inspect-only” task/mode, generating unnecessary architecture, testing and feature-management obligations. Do not make the mirror-image mistake of removing valuable **content inspection capabilities** such as viewing actual tracks and attachments: those are data presentation operations, but closing a document without generating output is not a specialized product feature.

Minimal statement: **open inputs → present their actual contents where supported → allow contextual operations → only write MKV when requested**. “No output” is an absent command, not a new mode. Allow no-write regression assertions as safety checks without presenting a distinct viewing workflow. Do not prescribe dedicated inspection interface or additional task state solely to implement that absence.

Action: corrected product research PR #206 document on `research/softmux-user-flow-integration-audit-20261101` at commit `651fdf0c2653e720032ce04276f49cceff429940`: changed “J2 只查看” to a **normal opening/switching regression condition**, corrected scope tables, and explicitly ruled out specialized inspect-only mode. Existing product main remains unmodified, and this is not a final UI endorsement.

Dedup: append to existing Nov 1 Candidate rather than new Canonical, Bug, or another independent Candidate. Link to broader possible-to-required drift previously recorded in this same document. Evidence level: owner correction + direct text artifact rectification; no real-user product runtime evidence.

## 2026-11-01 owner complaint: consequential assumptions were silently ratified; owner asked to confirm mostly ordinary matters

Owner explicit correction: “说到底是你默认确认了很多很多东西，而且交给我确认的东西相对来说很普通。”

Mechanism to investigate: **decision-authority inversion / asymmetric confirmation**. The assistant tacitly selected high-impact product semantics (the main file/draft/library ontology, automatic import membership policy, model A/C, whether a unified surface is preferable, non-destructive editing semantics, batch isolation and deferral priorities), embedded these as “reasonable defaults” in subsequent architecture and PR acceptance narratives, but asked the owner to approve lower-level binary scope alternatives (e.g., whether to implement arbitrary cross-MKV transfer now, whether complex EBML structures should be read-only first). This is not simply excess options or over-engineering: it shifts ownership of value-sensitive decisions to the assistant and burden of confirmation to the owner.

Important distinction:
- **Domain facts**: what Matroska permits, what current FFmpeg/native writer can do, actual legacy behavior; investigate and report with evidence.
- **Unavoidable technical constraints and reversible engineering tactics**: agent may decide with explicit impact/rollback.
- **Contested product semantics**: what “importing” means to user, desired automation vs manual control, expected behavior when files overlap, whether selection implies inclusion, relationships between old and new capabilities, intended priority of capabilities; cannot be inferred as user approval from mere theoretical elegance.
- **UX hypotheses**: UI structure, library vs current document, draft projections, direct operations; prototype as competing options and show tradeoffs rather than asserting one as the chosen framework.
- **Optional edge cases**: AI-generated examples must never silently become requirements.

New falsifiable process candidate: a **consequential-decision audit** before final architecture claims, asking “Which choices most change the user's product experience if wrong, and who authorized them?” Record origin, alternatives, effect on existing functions, reversibility, evidence and approval status for ONLY the high-impact choices. Do not ask owner to decide implementation trivia that engineering/testing can settle, and do not convert this into another gigantic decision ledger or questionnaire. Seek owner input through a few whole-task, lived behavior examples *before* committing a conceptual model. Treat assistant preferences as unapproved hypotheses. Prefer showing two real interactive variants/contradictions with accessible tradeoffs over asking owner to endorse broad or artificial scope dichotomies.

Concrete retrospective from prior turns:
- The assistant reified *absence of mandatory output* into a new “inspect-only functionality / mode” and PR #206 J2, later corrected after owner game-main-menu counterexample.
- The assistant interpreted source/target separation as a mandate for an explicit add operation, silently imposing friction on the original one-click video+ASS+font flow.
- The assistant proposed a final one-screen A/C hybrid while remaining uncertain how existing font preview and batch interact; approval sought on comparatively obvious deferral questions.
- Owner's tactical willingness to repeat some tasks does not retroactively approve deleting batch or hiding a user function.

No product code changed for this observation. Existing product PR #206 is a Draft **research artifact** and is not evidence that the owner approved its underlying choices. This is an extension to the same candidate, no new Canonical rule. Status: candidate, method and actual UX results PENDING.
