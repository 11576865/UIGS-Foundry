# Bug: CVS administrator token bootstraps non-atomically across processes; server binds all interfaces by default

Status: **Source-audited Bug / repair PR #31 / CI Pending**
Date: 2026-10-11
Project: `11576865/Character-Voice-Service`
Source: https://github.com/11576865/Character-Voice-Service/pull/31
Baseline main: `2d842f8e64ef199532cea61685da0179ffa6ccfd`
Audit: `docs/foundation-audit-2026-10-11.md` on PR branch

## Concrete source-derived defects

1. The original `server/config.py::_admin_token()` looked for
   `data/admin-token.txt`; if absent, generated a secret and wrote it
   using ordinary `Path.write_text`. Independent CVS Python server
   processes could both observe the missing file, each generate a
   different in-memory token, and overwrite one shared file. This can
   produce servers with inconsistent admin authentication despite
   sharing a configured data root. No actual user-machine race has
   been demonstrated yet; this is a source-derived TOCTOU defect.
2. POSIX file creation with ordinary `write_text` obeys the process's
   umask. Under common permissive settings, the admin token can be
   group/world-readable to local accounts. This is a local file
   permission risk, not proof of unauthorized access.
3. The default `CVS_HOST=0.0.0.0` binds the HTTP server on all host
   interfaces. Public `/v1/audio/speech` is intentionally
   unauthenticated by v1 API design, so this expands unintentional
   network reach and resource-exhaustion attack surface when no
   firewall is present. Admin mutations still require `X-CVS-Token`.

## Submitted patch

[CVS PR #31](https://github.com/11576865/Character-Voice-Service/pull/31):

- Atomically create a single token using `os.open(O_CREAT|O_EXCL)`.
  Concurrent losers wait for the committed token and do not overwrite.
  Flush and fsync the successful writer's file.
- Create new data root with owner-only permissions and token file mode
  0600 on POSIX; repair overly broad permissions on a preexisting
  token without rotating its content. Reject symbolic links and
  non-regular token paths.
- If an interrupted creator leaves a nonempty file uncommitted, the
  current contract is only flush/fsync on the successful path; the
  reader accepts nonempty content, which is a conservative but not a
  two-phase durable commit protocol. A completely empty file causes
  bounded wait then fail-closed error. Future improvements may use
  a fully staged immutable token handoff if crash-consistency proof
  is required; do not overstate it.
- Default network binding changes to `127.0.0.1`; explicit
  `CVS_HOST=0.0.0.0` remains a supported operator opt-in to LAN
  access (requires firewall / network controls and secure transport).
- Seven tests including eight simultaneous independent interpreters,
  private permissions, preserved old token, damaged empty file,
  symlink rejection and explicit LAN binding; Linux full and Windows
  targeted CI configured.

## Open foundation risks from same audit (not fixed by PR #31)

- Public TTS `/v1/audio/speech` currently has no explicit bounded
  request text length/tenant quotas or app-level rate limiting;
  adding admin auth unilaterally would break the v1 client contract.
- `requirements.txt` uses lower bounds rather than a resolved
  lockfile; test environment reproducibility cannot be guaranteed.
- Windows job tests are manually listed while Linux runs all pytest
  tests, so coverage drift is possible.
- Model Registry transactional locking and checksum evidence exist,
  but real power/fault injection and GPU/System Supervisor deployment
  acceptance remain outside simulated CI.

## Deduplication and evidence boundary

Foundry queries `admin token concurrent creation`,
`CVS admin-token.txt race`, `umask world readable admin secret`,
`default bind 0.0.0.0`, `public speech endpoint quota`, and
`requirements dependency pinning` returned no existing matching
Bug. This is recorded as a concrete **Bug**, not a premature
Canonical change.

CI for the PR was still Pending at intake. No real network exposure,
unauthorized access or corrupted host admin tokens are claimed.


## Repair refinement: readers must hold the same bootstrap lock (2026-10-11)

During review of PR #31's initial patch, a second source-level race
was identified: `O_CREAT|O_EXCL` alone prevents a second token writer,
but a reader may observe a **nonempty, incompletely flushed** token
while the winner still holds its open file. The patch was corrected to
use the existing cross-platform `acquire_runtime_slot("admin-token",
DATA_DIR)` OS lease for **both token creation and token reading**.
The lock file is persistent and must not be deleted. The creator also
uses O_EXCL and fsync; the second process waits for release and reads
the completed shared token. If the only stored token is empty after
exclusive acquisition, bootstrap fails closed rather than rotating it.

An **eighth** regression test creates a separate process that holds
the exact bootstrap lock, writes only half an admin token and pauses;
a second independent interpreter must remain blocked until the
writer finishes and releases the lock, then read the complete token.

Latest PR #31 head at this observation:
`cdb4bc68534f5fa3cc010cd9d9618f25ea535a8e`.
The new Linux and Windows GitHub CI jobs were **in progress** at the
time of this appended evidence. Continue to treat field tests as
distinct from CI and do not promote to Canonical.
