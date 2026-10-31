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

## 2026-11-01 owner correction: imported candidate content is already provisional; needless pre-inclusion approval

The assistant posed a question: when the user has an MKV open and drops alternative.ass, should it be immediately included in the *proposed output* or forced into a library pending an explicit Add? The owner replied: “既然都是拟输出，还有问的必要吗”.

Interpretation limited to the presented single-target examples: once the workspace is editing a *provisional output composition*, putting newly imported suitable content into that provisional composition is not an irreversible source modification, so a separate mandatory confirm-to-add gate may be gratuitous friction. The user may inspect, alter, exclude or remove prospective members before any explicit export. Existing source bytes remain unchanged. The assistant's earlier forced dichotomy between **auto-inclusion in an editable proposal** and **passive inventory pending approval** treated draft membership as if it required the same authorization as physical output.

Do not overgeneralize this correction into automatic merger of multiple source MKVs, automatic inclusion of unsupported assets, or silent creation of outputs. Provisional/undoable inclusion and actual writer support/output approval remain distinct, but a per-file Add click is not automatically justified by those facts. Revisit all prior model C and PR #206 assumptions about default exclusion and multiple ASS candidates. This is a user-facing design correction, not an implemented or Canonical rule; any production change still needs regression evidence for existing video+ASS+font flow.

## 2026-11-01 precise owner clarifications on writer, self-dependency, and product emphasis

Owner responded to four consequential questions:
1. Asked whether exact/limited Matroska mutation and full remux are materially different in implementation effort. Answer must be operation-specific: ordinary FFmpeg media remux is readily available but may lose nested chapters and targeted tags (#77); exact-value bounded EBML edits can sometimes be simpler than remux but general structure-preserving edits have much higher cost. A single product-wide “always remux” or “always patch” decision is not justified.
2. Explicitly said **自依赖检测** for subtitle/font delivery had already been discussed and was planned but apparently not generally shipped, asking why. Verify before inventing reasons: Oct 12 user-approved report assigns R-03 and T-008 final embedded ASS/font isolated render to P3; main `src/main.js:refreshSubtitlePreview` still consumes selected external ASS/selectedFonts plus a video, not arbitrary existing MKV internal tracks and attached fonts. `src/ass-font-rewrite.js` static font-use/glyph helpers, `src/output-font-payload-audit.js` new attachment SHA, and PR #118/#119 merged real-browser named-font CI fixtures are **partial evidence**, not a general self-contained subtitle dependency detector. Oct15 `docs/ten-round-sprint-20261015/acceptance-ledger.json` marks R-03 and T-008 **partial**. Round6 gap report explicitly says full source-embedded ASS + existing attachment closure remains outstanding, moved to future P3 work unit. No authoritative explicit project record establishing exactly *why* scope was not completed or abandoned; do not assert a causal motive or silently declare full feature absent.
3. Asked classification of same file having subtitle vs generic attachment/preview/font roles: a **domain resource identity vs contextual role/operation semantics** question, not intrinsically a new mode or UI workflow. Do not force user through per-file role questionnaires.
4. Explicitly chose **通用容器** as primary organizing orientation for the product. This is a new owner clarification; older Oct12 resolution did identify generic Matroska B as central domain core with A as flagship subtitle delivery. Do not rewrite or retire old subtitle/font/batch features nor unilaterally modify prior Canonical; record for owner-visible product direction reconciliation. New future UI proposals must not reinstall video+ASS+font as universal top-level task identity.

Dedupe: existing `inbox/cases/2026-10-12-mkv-self-contained-subtitle-rendering-acceptance.md`, `inbox/candidates/2026-10-12-structured-container-preservation-gate-before-mutating-writer.md`, and this Nov01 Candidate already cover technical gaps; this note records four *explicit owner responses*, current R-03 partial ledger evidence, and the constraint against repeating earlier discussion as new ideas. User/product validation of actual all-source self-dependency UI remains Pending. No source product code or Canonical changed.

## 2026-11-01 owner rejects default preservation concession; existing tools and category-context role selection

Owner objected to framing original-MKV preservation as intrinsically prohibitive and immediately requesting compromise: “保留原容器内容这么难？其他工具又是怎么做的，就不能参考吗？我服了。又要作什么妥协？” The user also supplied a concrete design mechanism for role ambiguity: existing preview/UI already has categories; content dropped into a relevant category adopts that purpose; users can select an alternate purpose for inclusion. User asked whether that is workable and wanted critical evaluation.

Independent external verification (2026-11-01):
- MKVToolNix official Matroska tools page identifies `mkvmerge` for remux, `mkvpropedit` for modifying track/segment properties, chapters/tags and adding/replacing/deleting attachments **without a complete remux**, plus `mkvextract` and `mkvinfo`: https://www.matroska.org/downloads/mkvtoolnix.html and https://mkvtoolnix.download/doc/mkvpropedit.html .
- RFC 9559 §6.1 expressly permits post-creation additions of attachments/chapters/tags, requires top-level SeekHead maintenance, discusses Void for minimizing relocations: https://www.rfc-editor.org/rfc/rfc9559.html . Matroska preservation has real structural complexity but is not uncharted engineering.
- Matroska foundation offers `libEBML` and `libMatroska` (C/C++, LGPL) and BSD C alternatives: https://www.matroska.org/downloads/libraries.html . Main obstacle to directly using native MKVToolNix in Softmux is its *current browser-local runtime*, not inability of external mature tools to preserve meaningful content. No proven browser-ready full MKVToolNix port was identified in this bounded search; Wasm porting and large local file access require actual feasibility tests, not blanket impossible claims.
- Product already has narrow structural writers, P2 append-one-attachment research, a 4-path bounded attachment writer router, and real independent MKVToolNix fixture comparisons. Do **not** claim it is a zero-knowledge/zero-code problem. Conversely existing FFmpeg remux reproduced nested-chapter/targeted-tag loss, and current bounded writers do not match mkvpropedit's general capacity; do not claim full preservation implemented.
- `mkvpropedit` edits an existing file in place; a source-unchanged UX needs a working copy or copy-on-write output. This has additional I/O cost but does not mean source-preserving container operations are infeasible.

Proposed project-specific product-review correction (Candidate, not approved architecture):
1. **No default concession of silent loss.** Investigate baseline operations versus mature MKVToolNix and related libraries before narrowing preservation; route eligible modifications by capability, keep honest fail-closed behavior for others. Distinguish *choice of operation support scope* from *accepting data loss in supposedly untouched contents*. Source bytes remain unmodified unless explicitly requested.
2. Treat user's category/preview drop targets as *contextual intent signaling*: drop ASS into subtitle = subtitle track intent; TTF into font = font resource/attachment intent; a TTF deliberately dropped into generic attachment = generic attachment intent. Alternate use can be chosen contextually; do not build a mandatory separate role-management workflow, or replace unified general import with four mutually exclusive forced gates. The content must still be validated for the selected operation; label is intent, not proof of codec support or writable ability.
3. Provenance can remain in internal model without user-visible resource-library bureaucracy. Imported asset provisionally appears in intended composition, and user can adjust/remove before output; the role choice does not itself write source files.
4. Only high-impact potential owner choice is *deployment/runtime constraint* (remain pure browser vs offer native/companion) **after** comparing evidence and costs, not prematurely presenting “accept corruption or delay general container” as a forced tradeoff.

Dedup: related `inbox/candidates/2026-10-15-mkv-multiple-bounded-writers-one-router-with-output-oracle.md` already covers writer route+artifact verification; `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md` already separates asset classification and task role. This addition captures owner's category-as-intent UX correction and explicit mature-tools-first alternative to premature scope compromise. No product or Canonical change. Implementation parity/UX tests remain PENDING.

## 2026-11-01 owner clarification: define *what* preservation preserves, not binary immobility

Owner asks: “所谓的保留内容究竟保留了什么？如果是重新构建但主要内容一样，又有什么改变了？在什么情况下很重要？” This challenges earlier assistant emphasis on “保留原容器结构” as an unqualified product objective.

Evidence and distinction:
- RFC 9559 explicitly permits alternative valid Matroska element ordering, recreated Cues/SeekHead offsets, Void/layout reorganization and added attachments/tags/chapters; ordinary layout/offset reorganization is **not by itself a harmful loss**. `SeekHead` and `Cues` must still remain valid and refer to current content.
- FFmpeg docs describe `-c copy` as forwarding coded media packets without decode/re-encode, **not** preserving all source EBML-level structure, metadata targeting or attachment relations. Some stream/format metadata mapping is automatic or optional and may differ.
- Existing `inbox/cases/2026-10-12-mkv-no-edit-preservation-scoped-independent-oracle.md` and issue #77 already document the project-specific failure where a playable remux drops nested chapters and UID-targeted tags. This Candidate adds the owner's **value/contract distinction**, not another bug.
- Proposed distinction, not unilaterally approved acceptance: **byte-for-byte source preservation** is a separate optional archival/integrity requirement; **content and relationship preservation** covers unmodified media streams (and timing), track identities/flags, ASS plus font attachments, chapters/edition structure, tags and UID referents, source-provided arbitrary attachments and other meaningful recognized content; **playback equivalence** is narrower than content/relationship preservation. If container byte layout, element offsets and index structure are regenerated validly without changing semantic relationships or playback, do not call that data loss or insist on exact original bytes.
- Importance is scenario-dependent: ordinary one-video/one-audio remux can have semantically harmless container re-layout; a multi-language subtitled archival MKV, nested editions/chapters, external linkages via segment UIDs or targeted tags, time-sensitive subtitles and preserved attachments expose high-impact silent loss. Correctly update related IDs when identity is rewritten, or preserve them if referenced.
- For product experience, describe a user-visible delta: **requested change**, **unchanged meaningful content**, **known normalization**, **unsupported/unverified semantic structures**. Do not treat FFmpeg exit, file playability, equal codec list, or whole-file SHA equality as a universal proof; use scope-appropriate independent finished-artifact reader/oracles. Also avoid absolutist “every unknown bit must remain intact” promises unsupported by existing browser runtime.

Status: candidate interpretation grounded in existing Foundry case and standards, **not** proof that every remux is safe or an owner-approved preservation contract. Product unchanged; no Canonical promotion.

## 2026-11-01 source-grounded implementation plan for semantic preservation (answering “但怎么实现？”)

This is a **bounded implementation proposal**, not an authorized product-wide writer rewrite. It builds on the owner's now-clarified distinction that the content, attributes and relationships must survive; normal EBML element layout and Cues/SeekHead regeneration need not match source bytes.

Actual product main evidence checked:
- `src/mux-command.js:buildMuxCommand` already maps streams, attachments, metadata and chapters and uses `-c copy`; this does not certify EBML semantic preservation.
- `src/mux-audit.js:auditMuxProbe` already compares stream groups/codecs/language/title/flags, chapter time/title/language with 2ms tolerance, attachment names/MIME, and format tags. Its FFprobe projection does **not** capture the complete nested ChapterAtom structure, UID tag targets, or full packet/attachment byte fidelity; do not replace it with a new isolated duplicative checker.
- `src/preservation-preflight.js:inspectMatroskaPreservation` already runs seek-based bounded source structure screening and returns `BLOCKED_RISK`, `BLOCKED_UNKNOWN`, `UNVERIFIED_REFERENCES`, `NO_KNOWN_HAZARD`; last result is not preservation certification.
- `src/matroska-attachment-relation-graph.js`, `src/matroska-attachment-reader.js` already inspect source attachment UIDs and tag targets in a bounded way.
- `src/p2-existing-mkv-writer-router.js` already chooses four attachment FileData-only copy/patch backends (`same-size`, `adjacent-void`, `tail-resize`, `seekhead-relay`), each independently constrained, with raw-byte, unchanged attachment hash and target-edge checks. It currently imposes 60 MiB source / 4 MiB replacement; not a general writer.
- `src/p2-matroska-inline-metadata-writer.js` can safely replace one same-encoded-byte-length ChapString/TagString under restrictive preconditions.
- `src/container-project.js` and `src/live-container-workspace-authority.js` own bounded user intents; existing batch queue should remain independent of any new writer implementation.
- `src/output-font-payload-audit.js` verifies new font attached bytes, not existing embedded resources. The existing known #77 loss is a real nested chapter/ChapterUID-targeted tag failure; neither the existing FFmpeg nor generic mkvmerge is assumed fully preserving.

Proposed engineering slices:
1. **Expected semantic manifest**: `Expected = observed source + explicit editIntents/additions/removals`, preserving all unedited recognized facts. Track identity may be remapped when the new UID and every reference are consistently updated. Distinguish exact packet bytes/timings, track metadata, attachment SHA, chapter hierarchy/times, edition membership, tag graph targets/values, and explicitly unrecognized EBML coverage. Do not infer all of this from FFprobe.
2. **Diff-oriented capability dispatch**: (a) metadata/attachment changes use tested existing bounded direct writers when eligible, (b) track topology changes use a remux engine only when a fidelity preflight and expected manifest can cover it, (c) new blank/attachment-only containers use existing candidate new writers once independently validated. No unsupported writers fall back to FFmpeg unsafely.
3. **Output oracle**: compare both input and actual output using the same semantic projection, preferably independent backend in CI (mkvmerge JSON, mkvextract chapters/tags/attachments/tracks, FFmpeg/FFprobe timestamp and ASS checks), plus necessary in-browser bounded readers at runtime. `PASS/FAIL/UNVERIFIED` should be per facet; report allowed changes separately, never global green for a partially observed output.
4. **Representative operation**: original MKV with video, 2 audio, original ASS/TTFs, nested ChapterAtom and ChapterUID-targeted Tag; user adds ASS. Before writing, expect exact old audio/video and subtitles/font bytes + timing, same chapter hierarchy & tag target relationships, new subtitle. A writer that drops chapter structure fails even if playback succeeds. Choose alternative native/ported engine or preserve structure via verified patch; unsupported operations don't produce a falsely verified export.
5. **Feasibility experiment**: run one realistic known-hard independent source through existing FFmpeg remux and native `mkvmerge` with explicit chapter/tag options; compare actual output XML, track demux, attachments, time/UID graph. Use this to determine whether an MKVToolNix/Matroska-library backend genuinely closes coverage; do not promise WebAssembly port before build-and-memory feasibility. MKVToolNix official docs confirm `mkvpropedit` edits properties/attachments without full remux and `mkvmerge` handles track topology; source `mkvpropedit` operates in place, so a copy/output plan is needed to preserve originals.

Key invariant: **nonmodified semantically meaningful data and relations are preserved, not necessarily byte-identical file layout**; source files remain untouched; failure/unknown status is transparent and does not automatically become a successful artifact. Scope, performance and browser availability require actual independent tests. This is consistent with existing `inbox/candidates/2026-10-15-mkv-multiple-bounded-writers-one-router-with-output-oracle.md` and `inbox/cases/2026-10-12-mkv-no-edit-preservation-scoped-independent-oracle.md`; do not create duplicates or promote Canonical.

## 2026-11-01 verified browser-access MKVToolNix deployment distinction

Owner asked if MKVToolNix has a browser version. Official https://mkvtoolnix.download/ and https://www.matroska.org/downloads/mkvtoolnix.html publish native Windows/macOS/Linux tools, no identified official full MKVToolNix WebAssembly browser-local distribution (negative discovery claim limited to this search). **Third-party browser-access systems do exist**, notably https://github.com/jlesage/docker-mkvtoolnix (Docker-hosted native GUI exposed via browser/PWA) and https://github.com/linterista22/mkv-maximus (self-hosted Docker web UI orchestrating MKVToolNix). Neither establishes true client-only processing; server-side execution and filesystem access remain. This is crucial for future Softmux backend discussions: “browser interface” is independent of “browser-local runtime”; do not falsely present native/cloud self-hosted tools as infeasible, or assert a complete wasm port is readily available. Check deployment, local-file privacy, streaming/copy overhead and license before proposing a switch. Related to prior mature-tools-first note; candidate-only, no product code or Canonical changes.

## 2026-11-01 owner critique: ideal user scenarios were staged feature demonstrations, not believable use

After a long assistant-produced “ideal browser Softmux user journey” enumerating one scenario per feature (source MKV, ASS/font dependency, multi-MKV, attachment-only, 20-job batch, oversized files, cost matrix), owner responded: **“太理想太刻意了。”** This is feedback on the *method of scenario construction*, not a rejection of browser-only operation or feature coverage.

Reusable observation, not elevated to Canonical: a product narrative is not an empirical user journey when the fictional user conveniently performs every architecture capability in designer-chosen sequence; every friction appears as a neatly resolved feature, and “integration” is performed for demonstration rather than emerging from one credible primary task. Separate **feature coverage demonstrations** from **user job narratives**. Anchor scenarios to one ordinary goal and actual files, allow nonsequential events, unused imports, aborted attempts, missing capabilities, ambiguous inputs, and user exit at any point; do not assume user consciously knows the product's internal container model. Show true browser cost during task, not exclusively in a separate apologetic checklist. “Eclectic integration” means features coexist and cooperate as relevant, not all must appear in one flow or one UI.

Product implication under investigation: one MKV+ASS user may only import, preview if desired, output; complex structural user may explore advanced object operations separately; both can be same person. Do not invent confirmation gates, standalone inspect-only mode, or replace already-working quick path to make story appear unified. Existing work `inbox/candidates/2026-10-10-mkv-content-first-intake-metadata-role-separation.md` and current candidate address task-role semantics and inflated approval flow; this note captures **scenario validity / feature-parade anti-pattern** without duplicating product implementation claims. Specific user behavior remains hypothetical until observed; no UI design approved; no Canonical promotion.

## 2026-11-01 owner correction: same feature names do not prove same planned behavior

Owner challenged assistant response claiming the previous idealized user narrative differed little from the current Softmux plan: “胡说八道，有”. The assistant had equated matching scope terms (“导入”, “预览”, “容器组成”, “保真”, “批量”) with actual equality of runtime behavior/UX and even denied differences it had already documented.

Cross-check against product current `docs/softmux-1.0-scope-b-1gb-decision-20261020.md`, `docs/softmux-1.0-product-acceptance-contract-20261020.md`, and research PR #206 (exact branch `research/softmux-user-flow-integration-audit-20261101`):
- Existing `resolveImportedRoles`: principal source role and main writer selection; proposed user task: category drop expresses intent with no redundant re-approval; this is not proved by an existing content classifier.
- Current `refreshSubtitlePreview` requires `videoInput.files[0]` and selected subtitles, global font selection; proposed preview of unselected candidates without toggling output membership requires actual dataflow work (and no-video standalone preview remains unproven).
- Existing FFmpeg main writer needs `mainInputPath`; existing no-video target projection and experimental attachment-only writers are not a production generic no-video write path.
- Current planned single primary execution source plus separate source inspector is not actual cross-source reuse of embedded tracks/attachments in a new target. The latter changes writer/identity scope and is beyond the original 1.0 guarantee.
- Existing fail-closed complex Chapters/Tag response is safe but is not the proposed actively pursued multiple browser-writer execution that can preserve semantics rather than routinely stop. Not an immediate guarantee to complete arbitrary inputs.
- Existing batch is already real and preserved; the ideal scripted journey of all general operations automatically batch-integrated would actually **increase** scope relative to the owner's tactical acceptance of manual repetition. Do not present this as already agreed.
- Browser-first native-companion optionality in earlier AI suggestions is superseded by owner's now explicit pure-browser constraint. It excludes quietly assuming an installable daemon as a baseline.

Correct methodology for claims “same as plan”: compare **input and user intent → state transition → execution preconditions → output and failure behavior → actual tests**, not feature labels or old abstract principles. Distinguish (A) already owner-approved direction, (B) current implementation, (C) research-only user-facing behavior, (D) unverified long-term capability. Substantive UX behavior differences should not be dismissed as trivial; likewise assistant's hypothetical narrative is not automatically owner-approved change.

Dedupe: existing Nov01 Candidate already contains most individual implementation gaps (J1/J3/J4 etc); this addition documents the comparative reasoning failure and corrected definition of a genuine delta, not a duplicate product requirement, and does not update Canonical or production code.

## 2026-11-01 owner challenges assistant's false “no difference” claim — reconcile declared plan, actual code, and new owner decisions

After an idealized feature-by-feature user-journey proposal and its subsequent critique, assistant claimed little substantive difference from existing Softmux planning. Owner explicitly rejected: “胡说八道，有”. The prior answer conflated feature *mentioned* in requirements with its *interaction contract*, *implementation route*, and *prioritization/cost* being settled.

Source-verified substantive contrasts:
1. **Browser-only permanence**: 2026-10-20 scope B sets *Chromium desktop/tablet verified 1.0 environment*, excludes native from 1.0 but does NOT set permanent no-native-execution product boundary; 2026-11-01 owner explicitly insists pure browser even in long term and wants uncompensated costs tracked. This does not imply wasm limitations become browser-wide exclusions.
2. **From “safe refusal as acceptable 1.0 endpoint” to “refusal as provisional unresolved engineering debt”**: old S08 / scheme B accepts reject-on-unknown/complex chapter as 1.0 formal boundary; owner wants maximum safe realization in browser, investigating mature Matroska remux/structural technology rather than normalizing refusal or permanent tradeoff. Fail-closed remains non-negotiable until proof, and short-term 1.0 scope is not silently revoked; but future priority/accepted compromises differ.
3. **Byte-structure proof vs user-relevant semantic output**: bounded P2 attachment router explicitly requires preserved top-level byte/offset commitments for all protected elements to authorize a writer; this is one valid implementation tactic, not universal product meaning of “preserve”. Owner clarified byte layout/seek/cues regeneration acceptable when contents, flags, chapter/tag UID relations, timestamps and actual dependencies survive.
4. **Interaction burden introduced by research/implementation**: current P2-M browser attachment creation exposes experimental separate form, mandatory explicit inclusion review checkbox, generate/check then separately download; P2 router has advanced drawer and requires explicit review. User's category-context drag intent, direct prospective inclusion and contextual editing conflict with promoting every internal engineering gate to mandatory normal user workflow. Keep mandatory high-risk approvals; remove redundant normal-case confirmations after verified semantics.
5. **Source/output composition vs single video source execution**: old approved core says no video root, but `src/output-composition.js` and `src/container-document.js` remain projected from a single `video`; `src/asset-intake.js:resolveImportedRoles` chooses one source and stores other containers in `unassignedContainers`; the UX scenario with multiple MKV source tracks composing one proposed output is a significant unimplemented domain→executor/interaction extension, not “same because generic Matroska was mentioned”.
6. **Scope and integration evidence**: S01-S14 1.0 candidate focuses bounded simple source+ASS and independent experimental tools; actual user wants seamless task-driven context and preservation of legacy quick path, not “one page/section per function”. Existing approved docs allow reuse, but no complete visual/real user proof. Do not claim the owner has approved a new screen design or arbitrary multi-source execution.

The new information is **the owner’s rejection of plan-equivalence**, not a complete ratification of every assistant-authored ideal scenario. The appropriate response is a claim-diff table grounded in plan text, code state, and explicit owner intent. Candidate status only; no product changes or automatic Canonical promotion.
