# Validation record

## Foundation

Python 3.12.14: documented fixture demo and unittest discovery passed locally.
No model credentials required. CI covers Python 3.11–3.13; a local pass does not
claim remote CI passed.

## Analysis

Local fixture planning and ambiguity/provider-failure tests passed on Python
3.12.14. Real Responses API adapter implemented using official documentation.
Live smoke test **blocked: OPENAI_API_KEY unavailable**. Milestone 2's external
acceptance remains unverified; no fixture or mock is presented as real AI evidence.

## Implementation and verification

11 tests passed. Synthetic explicit approvals demonstrated a passing expression
and a constant-fee expression with unmet criteria; failed evidence blocks
publication. Repeated execution returns the same run, source bytes are unchanged,
modified plans fail approval, unsafe syntax is rejected and concurrent locks fail
closed. Verification interprets a bounded AST; generated Python is never executed.

## Delivery and final checks

19 tests pass on Python 3.12.14. Ten fixture safety cases matched expected outcomes;
only success permits publication (see evaluation-fixture.json). Real GitHub fixture
run loaded Issue #1 and created draft demo PR #2; rerun reused the same issue/run/PR.
Project PR #3 is separate and unmerged. The GitHub connector lacked repository write
permission; the application used explicitly opted-in existing Git credentials,
held only in process memory, for the demonstration.

`python scripts/clean_check.py` passed in a fresh venv without pip or third-party
packages: tests, basic demo, evaluation, and approved synthetic success/failure
walkthrough. Captured terminal output is in terminal-demo.txt. `git diff --check`
passed. Remote CI results must be checked on GitHub; no claim follows from local
tests alone. Live model smoke remains unverified due to unavailable API credentials.
