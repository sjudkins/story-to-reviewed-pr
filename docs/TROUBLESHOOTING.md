# Troubleshooting

| Symptom | Action |
|---|---|
| Python missing / Store alias opens | Install Python 3.11+ and use that interpreter; on Windows try `py -3`. |
| Plan file already exists | Review/reuse it or choose another `--out`; plans are never silently replaced. |
| Clarification requested | Use the exact v1 criteria or extend the trusted domain adapter and tests after review. |
| Approval mismatch | Read the current plan and supply its complete digest; editing any field needs reapproval. |
| Unsupported target structure | Restore the controlled sample template; do not execute arbitrary repository code. |
| Lock exists | Confirm no workflow process is active, then remove that specific stale `.lock` manually. |
| HTTP 401/403 | Check token permissions/account and configured repository; no fallback to fixtures in real mode. |
| HTTP 429 / timeout | Resolve quota/network access and retry manually; no hidden automatic retry spend. |
| Model refusal/incomplete | Review story/model/output limit; no implementation or publication occurs. |
| Remote sample changed | Fetch current base, replan/reapprove and rerun; never force-push. |
| PR create failed after branch creation | Rerun with the same run/config; inspect branch if a conflict is reported. |
| Real smoke unavailable | Supply OPENAI_API_KEY securely and follow MODEL.md; do not label fixtures as real AI. |

Exit codes: 0 successful command (including planning awaiting approval); 1 visible
failed/blocked verification or clarification, or evaluation expectation mismatch;
2 invalid input, approval, access or configuration error. Publication failures keep
the run evidence. Inspect `.runs/RUN_ID/report.json` and `.md` locally.

This is a CLI on a trusted workstation, not a multi-user hosted service. Network
operations may require your execution environment's approval. Never disable those
controls or paste credentials into repository files to avoid an access problem.
