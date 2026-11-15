import base64
import json
import os
from pathlib import Path
import subprocess
import tomllib
from urllib.parse import quote
from .analysis import fingerprint
from .core import WorkflowError
from .execution import checked_plan, verify, TEMPLATE, markdown, lock
from .github import GitHub, validate_repo


def git_token():
    # Opt-in only; never print/persist helper output. No shell or URL interpolation.
    try:
        result = subprocess.run(["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n", text=True, capture_output=True,
            timeout=30, env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"})
    except (OSError, subprocess.TimeoutExpired):
        raise WorkflowError("Git credential helper unavailable; use GITHUB_TOKEN") from None
    values = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    if result.returncode or not values.get("password"):
        raise WorkflowError("No stored GitHub credential; authenticate Git or use GITHUB_TOKEN")
    return values["password"]


def publish(run_dir, config_path, allow_git_auth=False, client=None):
    directory = Path(run_dir)
    config = tomllib.loads(Path(config_path).read_text(encoding="utf-8"))
    if config.get("publication_enabled") is not True:
        raise WorkflowError("Publication disabled in operator configuration")
    repo = validate_repo(config["repository"])
    base = config["base_branch"]
    if not isinstance(base, str) or not base or len(base) > 200 or base.startswith("-"):
        raise WorkflowError("Invalid base branch")
    with lock(directory.parent):
        plan = json.loads((directory / "plan.json").read_text(encoding="utf-8"))
        report = json.loads((directory / "report.json").read_text(encoding="utf-8"))
        digest = checked_plan(plan, plan.get("approval_digest"))
        evidence = verify(plan["expression"], plan["criteria"])
        if (report.get("plan_digest") != digest or report.get("approved") is not True or
            report.get("status") != "passed" or report.get("publication_allowed") is not True or
            report.get("criteria") != evidence or not evidence or
            any(c["status"] != "verified" for c in evidence)):
            raise WorkflowError("Publication blocked: approval and verified evidence must pass")
        if client is None:
            token = os.environ.get("GITHUB_TOKEN") or (git_token() if allow_git_auth else None)
            if not token:
                raise WorkflowError("Publication requires GITHUB_TOKEN or explicit --git-auth")
            client = GitHub(repo, token)
        branch = f"demo/story-{report['run_id']}"
        # Query all states; a closed PR is a prior delivery, never create another.
        pulls = client.api(f"pulls?state=all&head={quote(repo.split('/')[0]+':'+branch, safe='')}&per_page=100")
        if pulls:
            if len(pulls) != 1 or pulls[0]["base"]["ref"] != base:
                raise WorkflowError("Conflicting existing demonstration PR; human review required")
            return {"url": pulls[0]["html_url"], "reused": True, "state": pulls[0]["state"]}
        base_ref = client.api(f"git/ref/heads/{quote(base, safe='')}")
        parent = base_ref["object"]["sha"]
        remote = client.api(f"contents/sample/shipping.py?ref={quote(parent, safe='')}")
        if remote.get("type") != "file" or remote.get("encoding") != "base64":
            raise WorkflowError("Remote sample must be a regular file")
        before = base64.b64decode(remote["content"]).decode("utf-8").replace("\r\n", "\n")
        if fingerprint(before) != report["base_file_sha256"]:
            raise WorkflowError("Remote sample changed since approval; replan and reapprove")
        after = TEMPLATE.format(expression=plan["expression"])
        if after == before:
            raise WorkflowError("No code change to publish")
        # A branch may remain after an interrupted publish. Reuse only exact content.
        branches = client.api("branches?per_page=100")
        existing = next((b for b in branches if b["name"] == branch), None)
        if existing:
            content = client.api(f"contents/sample/shipping.py?ref={quote(existing['commit']['sha'], safe='')}")
            actual = base64.b64decode(content["content"]).decode("utf-8")
            if actual != after:
                raise WorkflowError("Existing demo branch differs; refusing to overwrite")
        else:
            commit = client.api(f"git/commits/{parent}")
            tree = client.api("git/trees", {"base_tree": commit["tree"]["sha"], "tree": [
                {"path": "sample/shipping.py", "mode": "100644", "type": "blob", "content": after}]})
            created = client.api("git/commits", {"message": f"demo: verified shipping rule ({plan['mode']})",
                                  "tree": tree["sha"], "parents": [parent]})
            client.api("git/refs", {"ref": f"refs/heads/{branch}", "sha": created["sha"]})
        pr = client.api("pulls", {"title": f"Demo: verified shipping rule [{plan['mode']}]",
             "head": branch, "base": base, "draft": True,
             "body": "Synthetic application demonstration; separate from the portfolio project PR.\n\n" + markdown(report)})
        result = {"url": pr["html_url"], "reused": False, "state": pr["state"]}
        (directory / "publication.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result
