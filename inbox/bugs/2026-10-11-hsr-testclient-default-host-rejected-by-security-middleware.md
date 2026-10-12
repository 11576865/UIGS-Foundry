# Bug: TestClient default Host violates the application's loopback security contract

Date: 2026-10-11
Status: Fixture repair committed on unmerged HSR PR #133; exact new-head CI pending
Lifecycle: validation-pending
Product: HSR-Voice-Archive-Builder
Scope: security middleware / API integration tests / Python FastAPI

## Observed failure

HSR PR #133's first unit matrix run [38117537332](https://github.com/11576865/HSR-Voice-Archive-Builder/actions/runs/38117537332) had one concrete failing test out of 420 executed: `test_fastapi_project_route_reports_the_same_audit` returned 400 instead of 200. The test used `TestClient(app)`, whose default request host is `testserver`. The HSR `control_surface_guard` correctly enforces `host_allowed(request.url.hostname)` and rejects this synthetic host to protect the local control API from DNS rebinding.

This was not proof that the new archive audit handler rejected a valid project; the fixture request was rejected before the handler.

## Repair

Update the test fixture to use `TestClient(app, base_url="http://127.0.0.1:8765")` and the authorized `X-HSR-Token`, consistent with established tests elsewhere in the same repository. Do not relax the middleware to accept `testserver` in production.

Commit: HSR PR #133 `b7d419ad40c80266e7a6a68fb4671160daa146d6`. Current PR has since advanced with feature work. The original failure and the code-level fix are evidenced; exact updated-head CI outcome remains asynchronous/pending, not claimed green.

## Reusable lesson

When security middleware validates Host/origin/CSRF/loopback identity, integration test clients must exercise a deliberately permitted host. A newly added test failing at the middleware boundary should report response body and distinguish fixture setup errors from handler behavior. Do not weaken production protections solely to accommodate a default synthetic test host.

## Intake

Bug recorded, no Canonical update from this single project.
