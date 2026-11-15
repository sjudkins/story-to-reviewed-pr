"""Explicit synthetic fixture approvals; no GitHub writes or model calls."""
import argparse
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from story_pr.analysis import analyze, fingerprint
from story_pr.core import read_story
from story_pr.execution import execute, TEMPLATE

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--approve-synthetic-fixture", action="store_true", required=True)
args = parser.parse_args()
story = read_story("stories/free-shipping.json")
with tempfile.TemporaryDirectory() as root:
    target = Path(root)/"sample"/"shipping.py"
    target.parent.mkdir()
    target.write_text(TEMPLATE.format(expression="5"), encoding="utf-8")
    for label, expression in [("success", "0 if subtotal >= 50 else 5"), ("failed_verification", "5")]:
        plan = analyze(story)
        plan["expression"] = expression
        plan["approval_digest"] = fingerprint(plan)
        print(f"\nFIXTURE {label}; explicit synthetic approval: {plan['approval_digest']}")
        report = execute(plan, plan["approval_digest"], root, Path(root)/"runs")
        print(json.dumps({k: report[k] for k in ("mode", "status", "publication_allowed", "criteria", "diff")}, indent=2))
