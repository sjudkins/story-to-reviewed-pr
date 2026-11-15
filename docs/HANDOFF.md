# Portfolio handoff

Repository: https://github.com/sjudkins/story-to-reviewed-pr

Project PR: https://github.com/sjudkins/story-to-reviewed-pr/pull/3 (unmerged).
Application demonstration: [Issue #1](https://github.com/sjudkins/story-to-reviewed-pr/issues/1)
and [draft PR #2](https://github.com/sjudkins/story-to-reviewed-pr/pull/2).

**Status: demonstrated fixture-backed application, with an unverified real-model
adapter.** Not deployed or production-adopted. It plans from local JSON/GitHub
Issues, rejects ambiguous/unsupported criteria, requires explicit digest approval,
changes one isolated sample file, verifies six trusted examples, reports criterion
evidence, and conditionally publishes an idempotent draft PR.

All observed end-to-end demonstrations/evaluations used deterministic fixtures.
Real adapter transport/contract tests used mocks. No live model run occurred
because API credentials were unavailable. Model quality, real latency and billed
cost remain unmeasured. Fixtures made zero API calls at zero API cost. See
[real smoke instructions](MODEL.md).

Actual results: 19 local tests passed; ten synthetic safety cases matched ten
expected outcomes, including two failed verifications and blocked unsafe requests.
Only the success case was publication eligible. Live GitHub fixture run verified
both criteria against six examples and opened draft PR #2; rerun reused it.
Captured per-case local latencies are in evaluation-fixture.json, not model latency.
Fresh Python 3.12.14 venv without third-party packages ran tests, demo, evaluation
and success/failure walkthrough successfully. Reproduce via README, EVALUATION.md
and `python scripts/clean_check.py`.

Decisions: standard-library CLI, single Responses adapter, explicit plan/approval/
evidence artifacts, exact criterion catalog, application-owned tests, restricted
expression interpretation instead of arbitrary generated Python execution, remote
source-hash checks and deterministic delivery branches. See ARCHITECTURE.md for
diagram/tradeoffs and SECURITY.md for trust boundaries.

Limitations: only the shipping-fee function/two canonical criteria; finite examples
are not exhaustive proof; operator/local config trusted; no multi-user service, UI,
general coding agent, dependency changes or production adoption. Additional domains
need reviewed adapters/tests. A hardened external runner is required for arbitrary
generated Python execution. Live API smoke is the outstanding external validation.

Proposed AI Solutions Architect resume bullets:
- Designed a bounded story-to-PR workflow separating model proposals, explicit
  approval, application-owned verification and evidence-gated GitHub publication.
- Documented trust boundaries and deployment tradeoffs; evaluated ten synthetic
  safety cases and demonstrated a credential-free workflow with an optional
  Responses API adapter, separating model performance claims from fixtures.

Proposed Forward Deployed Engineer resume bullets:
- Built and demonstrated a Python CLI that loads GitHub Issues, proposes a shipping
  rule change, verifies acceptance examples and opens an idempotent draft PR.
- Implemented plan-digest approval, isolated sample changes, failure-preserving
  reports and 19 automated tests; validated workflows in a clean virtual environment.

AI assisted code/test/documentation drafting. The author should review and explain
the decisions and evidence. No customers, savings, adoption or business outcomes
have been measured or claimed.
