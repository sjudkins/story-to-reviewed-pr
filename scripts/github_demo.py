"""Operator-invoked synthetic GitHub demo; explicit fixture approval required."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from story_pr.analysis import analyze, fingerprint
from story_pr.delivery import git_token, publish
from story_pr.execution import execute
from story_pr.github import GitHub

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--approve-synthetic-fixture", action="store_true", required=True)
parser.add_argument("--publish", action="store_true")
args = parser.parse_args()
repo = "sjudkins/story-to-reviewed-pr"
client = GitHub(repo, git_token())
title = "Synthetic demo: free shipping on qualifying orders"
issues = client.api("issues?state=all&per_page=100")
matches = [i for i in issues if i["title"] == title and "pull_request" not in i]
if len(matches) > 1:
    raise SystemExit("Multiple matching demo issues; review manually")
issue = matches[0] if matches else client.api("issues", {"title": title, "body":
    "Independently authored synthetic portfolio demonstration; no customer data.\n\n"
    "As a shopper I want free shipping on orders of at least 50 dollars.\n\n"
    "## Acceptance criteria\n- Orders below 50 dollars pay 5 dollars shipping.\n"
    "- Orders of at least 50 dollars pay no shipping."})
story = client.issue(issue["number"])
plan = analyze(story)
plan["approval_digest"] = fingerprint(plan)
Path(".runs").mkdir(exist_ok=True)
Path(".runs/github-plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
report = execute(plan, plan["approval_digest"], ".", ".runs")
print(json.dumps({"mode": "fixture", "issue": issue["html_url"], "run_id": report["run_id"],
                  "status": report["status"], "criteria": report["criteria"]}, indent=2))
if args.publish:
    print(json.dumps(publish(Path(".runs")/report["run_id"], "demo.toml", True), indent=2))
