# Trust boundaries and isolation

V1 changes exactly one pure function: `sample/shipping.py`. It supports only a
single-line Python conditional expression, `subtotal`, numeric constants, `<` and
`>=`. No arithmetic, calls, attributes, imports, loops, assignments or filesystem
access. Inputs: nonnegative finite numeric order subtotals; other domains are out
of scope. Constants <= 1,000,000, expression <= 200 characters and <= 50 AST nodes.

The target file must match the application-owned template and cannot be a symlink
or escape the operator-selected repository. The workspace copies only that file
into a temporary directory. It never runs repository tests, hooks or generated
Python. Trusted application code interprets allowed AST nodes against six catalog
examples. This verifies examples rather than universally proving business intent.
Extending arbitrary generated Python execution requires a separate hardened runner
with no secrets, network disabled, resource limits, read-only trusted tests and
reviewed mounts. It is **disabled in this version**; no unsafe execution override.

Issue text and model output cannot select targets, commands, tests or publication
policy. Exact catalog criteria bound what can be verified. Human review remains
necessary for unknown requirements, even when a model claims confidence.
The plan digest is an explicit approval binding, not authentication or a signature.
A local operator able to edit application code/config/artifacts is trusted. Do not
accept run directories from untrusted parties or expose this CLI as a service.

Runs preserve failed evidence under `.runs/`; an exclusive lock prevents overlap.
No automatic repair loop or automatic plan approval. HTTP responses/time/tokens
are bounded; redirects carrying secrets are rejected. Raw provider errors are not
logged. Never put keys in story files or arguments. `.runs` and `.env` are ignored.
