import argparse
import json
from .core import WorkflowError, walkthrough


def main(argv=None):
    parser = argparse.ArgumentParser(description="Story to Reviewed PR")
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Credential-free fixture walkthrough")
    demo.add_argument("--story", default="stories/free-shipping.json")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(walkthrough(args.story), indent=2))
        return 0
    except (WorkflowError, OSError, ValueError) as exc:
        print(f"Error: {exc}")
        return 2
