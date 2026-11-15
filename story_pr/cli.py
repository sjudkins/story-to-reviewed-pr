import argparse
import json
from pathlib import Path
from .core import WorkflowError, walkthrough, read_story
from .analysis import analyze, fingerprint
from .github import GitHub


def main(argv=None):
    parser = argparse.ArgumentParser(description="Story to Reviewed PR")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Credential-free fixture walkthrough")
    demo.add_argument("--story", default="stories/free-shipping.json")
    plan = commands.add_parser("plan", help="Analyze without executing; review the resulting JSON")
    source = plan.add_mutually_exclusive_group(required=True)
    source.add_argument("--story")
    source.add_argument("--issue", type=int)
    plan.add_argument("--repo", help="Explicit GitHub Issue source owner/name")
    plan.add_argument("--mode", choices=["fixture", "real"], default="fixture")
    plan.add_argument("--out", default=".runs/plan.json")
    execute = commands.add_parser("execute", help="Explicitly approve and verify in an isolated sample copy")
    execute.add_argument("--plan", required=True)
    execute.add_argument("--approve", required=True, help="Full SHA256 digest from reviewed plan")
    execute.add_argument("--root", default=".")
    execute.add_argument("--runs", default=".runs")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            result = walkthrough(args.story)
        elif args.command == "execute":
            from .execution import execute
            result = execute(json.loads(Path(args.plan).read_text(encoding="utf-8")),
                             args.approve, args.root, args.runs)
        else:
            if args.issue and not args.repo:
                raise WorkflowError("--issue requires an explicit --repo")
            story = GitHub(args.repo).issue(args.issue) if args.issue else read_story(args.story)
            proposal, usage = None, None
            if args.mode == "real":
                from .provider import propose
                proposal, usage = propose(story)
            result = analyze(story, proposal, args.mode, usage)
            result["approval_digest"] = fingerprint(result)
            path = Path(args.out)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8") as output:
                json.dump(result, output, indent=2)
        print(json.dumps(result, indent=2))
        return 1 if result.get("status") in ("failed", "blocked", "needs_clarification") else 0
    except (WorkflowError, OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 2
