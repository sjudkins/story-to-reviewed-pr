# Story to Reviewed PR

A focused Python CLI portfolio prototype: user story to reviewed plan, controlled
sample change, trusted verification evidence, and gated draft PR.

**Status: demonstrated fixture-backed application.** A real-model adapter is
implemented; its live smoke test is unverified because no API key was available.
This is not deployed or production-adopted software.

Requires Python 3.11+. No third-party runtime packages needed from a checkout:

```sh
python -m story_pr demo
python -m unittest discover -s tests -v
```

The demo is a **deterministic fixture**, not an AI performance claim. It loads
stories/free-shipping.json and shows a plan without making changes. The controlled
target is a small shipping-fee function in sample/shipping.py.

Run the complete local success/failure demonstration and evaluation:

```sh
python scripts/local_demo.py --approve-synthetic-fixture
python -m story_pr evaluate
```

For an operator-reviewed plan:

```sh
python -m story_pr plan --story stories/free-shipping.json --out .runs/my-plan.json
# Review JSON, then replace DIGEST with its full approval_digest:
python -m story_pr execute --plan .runs/my-plan.json --approve DIGEST
```

Inspect `.runs/RUN_ID/report.md` and `report.json`. Execution changes a temporary
copy only; failed checks remain visible and block publication. The model never
chooses tests. Arbitrary generated Python execution is disabled; the application
interprets a small allowlisted expression language. V1 supports the two exact
shipping criteria in the included story, not general repository coding tasks.

Public evidence: [synthetic Issue #1](https://github.com/sjudkins/story-to-reviewed-pr/issues/1)
and [draft demonstration PR #2](https://github.com/sjudkins/story-to-reviewed-pr/pull/2).
The PR includes six observed examples and a one-file diff. Rerunning reused it.

| Read next | Purpose |
|---|---|
| [Demo script](docs/DEMO.md) | Interview walkthrough and captured output |
| [Architecture](docs/ARCHITECTURE.md) | Diagram, decisions and tradeoffs |
| [Security](docs/SECURITY.md) | Trust boundaries and isolation limits |
| [Model setup](docs/MODEL.md) | Real API smoke command, bounds, usage and costs |
| [Evaluation](docs/EVALUATION.md) | Ten fixture cases and GitHub publication |
| [Validation](docs/VALIDATION.md) | Observed results and unverified checks |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Errors and recovery |
| [Handoff](docs/HANDOFF.md) | Portfolio status and proposed resume bullets |

`python scripts/clean_check.py` repeats checks in a fresh venv with no third-party
packages. Python 3.11–3.13 CI runs tests and the demo on pushes/PRs.

Optional installed CLI: `python -m pip install -e .`, then `story-pr demo`.
See [project plan](PROJECT_PLAN.md) for architecture and milestone scope.
