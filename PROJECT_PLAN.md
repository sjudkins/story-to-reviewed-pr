# Story to Reviewed PR

## Purpose and scope

A Python CLI turns a synthetic story or GitHub Issue into an approved, bounded
change in an explicitly configured Python sample repository, with verification
evidence and conditional draft PR publication. Fixture runs are always labeled;
they do not measure model performance. No customer or production claims.

## Architecture

Story loader -> structured analysis -> ambiguity gate -> plan and verification
mapping -> explicit approval -> isolated implementation workspace -> trusted
verification runner -> criterion evidence report -> publication gate -> draft PR.

Use Python's standard library where practical, one model adapter, and JSON run
artifacts. The application owns repository targets, file allowlists, limits,
verification commands, and publication policy. Issue text and model output cannot
change those controls. Scope v1 to small edits to a pure Python sample function;
reject dependency, infrastructure, credential, and arbitrary command changes.
Generated code execution remains disabled without trustworthy isolation; a Git
worktree alone is not a security boundary. Select the model adapter after checking
current official documentation and available API access. Never infer API access
from a chat subscription. Record usage and cost only when measurable.

## Setup gates (before milestone 1)

- [x] Inspect local folder: empty; no Git repository or parent instructions found.
- [x] Inspect runtimes: Git and Node available; bundled Python discovered.
- [x] Inspect GitHub access: connector profile sjudkins; organization installation
  ShayneJudkins; no local Git Credential Manager accounts; gh absent.
- [x] Inspect scheduling: supported Codex automation tool available; no existing
  automation files found.
- [x] Create public personal repository story-to-reviewed-pr, verify push access,
  establish default branch, then create codex/story-to-reviewed-pr.
- [x] Obtain start date/time in America/Chicago and create one project schedule.

## Daily milestones

Complete at most one milestone per scheduled run. Resume incomplete work next day;
record delays honestly. Do not backdate, merge, force-push, or publish failed work.

- [ ] 1. Foundation: package/configuration, sample app, synthetic stories, fixture
  walkthrough, tests, CI, setup README. Gate: clean checkout demo/tests without keys.
- [ ] 2. Analysis: local/GitHub loaders, structured criteria/plans/clarifications,
  one real model adapter, error tests. Gate: fixture and real smoke evidence;
  ambiguous stories stop. Missing API access is a blocker, not a passing smoke test.
- [ ] 3. Execution: isolated changes, approval, bounds, diff inspection, trusted
  checks, criterion evidence. Gate: observed success and visible failing check;
  failure blocks publication.
- [ ] 4. Delivery: explicitly configured demo repository, idempotent draft PRs,
  eight or more synthetic evaluations, latency/usage/cost reporting. Gate: actual
  end-to-end draft PR and reproducible evaluation; fixtures separate from AI results.
- [ ] 5. Portfolio: architecture diagram, demo capture/script, troubleshooting,
  decisions/limits/AI contribution, clean environment validation, final handoff.
  Gate: final checks pass; one review-ready project PR with milestone commits;
  disable schedule through supported tool; never merge.

Application demo PRs must be separate from the final project PR. Each milestone
records changes, checks and outcomes, remaining work, blockers, commit and PR links.
Use an exclusive run lock; inspect existing commits/PRs before retrying publication.

## Final handoff requirements

Include repository/project PR URLs, evidence-backed status, working features and
limits, fixture versus real demonstrations, actual evaluation results/reproduction,
architectural decisions, two AI Solutions Architect resume bullets and two Forward
Deployed Engineer bullets. Do not invent adoption, savings, customers, or results.

## Setup log

2026-11-15: Initial inspection complete. No implementation started. Schedule awaits
user's start date/time. Repository creation and unattended push access unresolved.
Confirmed personal account: sjudkins. Created public repository
https://github.com/sjudkins/story-to-reviewed-pr with initial README on main.
Local origin is connected and main fetched/checked out. Push dry-run passed;
codex/story-to-reviewed-pr created and setup plan committed/pushed successfully.
Requested schedule: November 16, 2026 at 8:13 PM America/Chicago, targeting
November 16–20. Active automation: story-to-reviewed-pr-daily-milestone.
Created through the supported Codex scheduling tool, daily at 20:13 local time.
The direct-create tool rejects anchored DTSTART, so a mandatory prompt guard exits
without work before November 16 (there may be a no-op November 15 invocation).
Continue beyond November 20 only if unfinished; disable after milestone 5 passes.
Do not activate the earlier unsaved proposal or create a duplicate schedule.
Bundled interpreter found under the CodexPrimaryRuntime dependencies/python folder;
the Python command on PATH points to an inaccessible Windows Store alias.
