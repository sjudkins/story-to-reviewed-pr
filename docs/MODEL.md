# Real model path

The single adapter uses OpenAI Responses API structured output, a 30-second HTTP
timeout, one call, 1,200 output tokens, no retries, no tools and `store: false`.
Story inputs are bounded to 32 KB. Set `OPENAI_API_KEY` outside the repository.
`STORY_PR_MODEL` selects a model; default `gpt-4.1-mini-2025-04-14` is a small pinned
model suitable for this narrow task. Access depends on your API account.

```sh
python -m story_pr plan --story stories/free-shipping.json --mode real --out .runs/real-plan.json
```

Review the plan and usage. A completed HTTP response alone is not proof the
expression is correct; subsequent trusted verification must pass. Failure/refusal
does not fall back to fixtures. Chat subscriptions do not imply API access.
No key was available during project validation, so **live real-model smoke test
has not run**. Mocked transport tests verify failures, not model quality.

Usage records observed input/output tokens and latency. Actual cost is unavailable
from the response and is left null; use the provider billing dashboard. Fixtures
make zero API calls and cost zero. Input and output caps bound exposure but are not
a dollar budget. No invented costs or assumed performance.

Official references checked during implementation:
- [Responses API](https://developers.openai.com/api/reference/resources/responses/methods/create)
- [Structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [GPT-4.1 mini](https://developers.openai.com/api/docs/models/gpt-4.1-mini)

GitHub Issue input:
`python -m story_pr plan --repo sjudkins/story-to-reviewed-pr --issue NUMBER`.
Issue body needs `## Acceptance criteria` followed by bullet points. Public reads
can be unauthenticated; use `GITHUB_TOKEN` for private reads or rate limits.
V1 recognizes only the two exact catalog criteria in the included synthetic story.
Unrecognized criteria stop for clarification, even if the model thinks them clear.
