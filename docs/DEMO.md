# Three-minute interview demo

1. Explain the problem: a story-to-code agent can claim success without proving
   acceptance criteria. Here application-owned examples produce inspectable evidence.
2. `python -m story_pr plan --story stories/free-shipping.json --out .runs/interview.json`
   Show exact criteria, questions, expression and approval digest. No implementation
   happens during planning. Read and approve the plan before proceeding.
3. `python -m story_pr execute --plan .runs/interview.json --approve DIGEST`
   Replace DIGEST with the full value you reviewed. Show `.runs/RUN_ID/report.md`:
   six observed examples, per-criterion statuses and one-file diff. The source
   checkout remains unchanged.
4. `python scripts/local_demo.py --approve-synthetic-fixture` shows success and
   a failed constant-fee change. The flag is explicit approval of synthetic tests,
   not a bypass for real plans. Show the failed criterion blocking publication.
5. `python -m story_pr evaluate` shows ten fixture safety cases. Explain that 10/10
   expected outcomes is not a model benchmark. Open [demo PR #2](https://github.com/sjudkins/story-to-reviewed-pr/pull/2)
   and [Issue #1](https://github.com/sjudkins/story-to-reviewed-pr/issues/1).
6. Explain the real path: `OPENAI_API_KEY`, optional `STORY_PR_MODEL`, and `--mode real`.
   It produces the same artifacts and faces the same checks. Live model quality is
   unmeasured in this project because no API key was available for validation.

Optional network step after reviewing config:
`python -m story_pr publish --run .runs/RUN_ID --config demo.toml --git-auth`.
This uses a stored Git credential; use GITHUB_TOKEN instead if preferred. It creates
a **draft**, does not merge, and refuses failed evidence. The synthetic GitHub
helper in EVALUATION.md is restricted to the named synthetic issue/repository.

Captured local run: [terminal-demo.txt](terminal-demo.txt).
