# Evaluation

Run `python -m story_pr evaluate`. Ten synthetic cases cover a successful change,
two failing implementations (including reversed boundary), missing criteria,
ambiguity, unsupported scope, prompt injection, unsafe syntax, changed approval,
and duplicate criteria. Each fixture explicitly approves only a synthetic plan.
All ten outcomes must match expectations; only the success case allows publication.
This is **safety-case agreement**, not a 100% model task-completion claim.

Captured results: [evaluation-fixture.json](evaluation-fixture.json). Latency is
local wall time for planning and verification, not remote/model latency. Zero API
calls and zero API cost. Real-model results are unavailable until an API key is
provided; repeat real planning plus approval/execution separately and retain usage.

Tests: `python -m unittest discover -s tests -v`. Additional delivery tests prove
failed/tampered evidence makes no publication and existing PRs are reused.

Publication needs explicit operator config: repository/base branch and enabled
flag in `demo.toml`. Its default points at this portfolio repo's development branch.
The demo changes only `sample/shipping.py` on a `demo/story-...` branch and opens a
draft PR to that development branch, separate from the project PR targeting main.
Use `GITHUB_TOKEN` with contents and pull-request write permissions (Issues write
only for the optional issue creation script) or opt into stored Git credentials
with `--git-auth`. No force updates or merges. Publication rechecks trusted evidence
and remote source hash. Network failure may leave an orphan commit/branch; rerun
finds the deterministic branch and PR rather than creating new deliveries.

For this synthetic demonstration only:
```sh
python scripts/github_demo.py --approve-synthetic-fixture --publish
```
This creates/reuses the explicitly named synthetic issue in this repository, loads
it via GitHub, records a fixture plan/approval, verifies, and publishes. It never
approves a real issue automatically. Ensure the development branch has been pushed
with the sample file first. Review `demo.toml` before any network writes.
