# Story to Reviewed PR — implementation plan

Python CLI -> analysis -> ambiguity gate -> plan -> explicit approval -> isolated
sample workspace -> trusted verification -> criterion evidence -> gated draft PR.
Application policy owns targets, permissions, verification and publication rules.
V1 supports only sample/shipping.py via a restricted expression language. Unknown
criteria need human review. Fixtures are separate from real-model performance.

- [x] 1. Foundation: package, sample/story, fixture walkthrough, CI, setup README.
- [x] 2. Analysis implementation: local/GitHub loading, structured plan, ambiguity, real adapter.
- [x] 3. Implementation: approval, workspace, bounds, trusted evidence.
- [ ] 4. Delivery: draft PRs, rerun safety, evaluations, measured results.
- [ ] 5. Portfolio: demo capture, diagram, decisions, clean setup, handoff/project PR.

Acceptance evidence and limitations: docs/VALIDATION.md. This checklist does not
imply unavailable external checks passed.
