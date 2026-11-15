import hashlib
import json
import re
from .core import WorkflowError

# Trusted examples, never supplied by the model or issue. Deliberately narrow v1.
CATALOG = {
    "Orders below 50 dollars pay 5 dollars shipping.": [(0, 5), (10, 5), (49.99, 5)],
    "Orders of at least 50 dollars pay no shipping.": [(50, 0), (50.01, 0), (1000, 0)],
}


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def extract_issue(issue):
    if "pull_request" in issue:
        raise WorkflowError("Expected an Issue, not a pull request")
    body = issue.get("body") or ""
    criteria = []
    active = False
    for line in body.splitlines():
        if re.match(r"^#{1,6}\s+Acceptance criteria\s*$", line, re.I):
            active = True
        elif line.startswith("#"):
            active = False
        elif active:
            match = re.match(r"^\s*[-*]\s+(?:\[[ xX]\]\s*)?(.+)$", line)
            if match:
                criteria.append(match[1].strip())
    return {"title": issue["title"], "body": body, "criteria": criteria}


def analyze(story, proposal=None, mode="fixture", usage=None):
    if len(json.dumps(story)) > 32_000:
        raise WorkflowError("Story exceeds 32 KB limit")
    title = story.get("title")
    criteria = story.get("criteria", [])
    if not isinstance(title, str) or not title.strip() or len(title) > 300:
        raise WorkflowError("Provide a nonempty title of at most 300 characters")
    if not isinstance(criteria, list) or len(criteria) > 20 or any(
        not isinstance(c, str) or not c.strip() or len(c) > 500 for c in criteria
    ):
        raise WorkflowError("Criteria must be a list of at most 20 nonempty strings (500 characters each)")
    questions = []
    if not criteria:
        questions.append("Provide explicit acceptance criteria.")
    if len(set(criteria)) != len(criteria):
        questions.append("Remove duplicate acceptance criteria.")
    mapped = []
    for index, text in enumerate(criteria, 1):
        supported = text in CATALOG
        if not supported:
            questions.append(f"Criterion AC{index} is ambiguous or outside the v1 shipping catalog; clarify scope.")
        mapped.append({"id": f"AC{index}", "text": text,
                       "verification": "trusted shipping examples" if supported else "human review required"})
    # Fixture is deliberately authored; no story-provided expressions are accepted.
    proposal = {"expression": "0 if subtotal >= 50 else 5", "questions": [],
                "summary": "Change the shipping fee at the 50 dollar boundary."} if proposal is None else proposal
    if not isinstance(proposal, dict) or set(proposal) != {"expression", "questions", "summary"}:
        raise WorkflowError("Provider returned an invalid plan shape")
    if not isinstance(proposal["expression"], str) or len(proposal["expression"]) > 200:
        raise WorkflowError("Provider expression exceeds limit or has invalid type")
    if not isinstance(proposal["summary"], str) or len(proposal["summary"]) > 1000:
        raise WorkflowError("Provider summary invalid")
    if not isinstance(proposal["questions"], list) or len(proposal["questions"]) > 20 or any(
        not isinstance(q, str) or len(q) > 500 for q in proposal["questions"]
    ):
        raise WorkflowError("Provider questions invalid")
    questions.extend(proposal["questions"])
    plan = {"version": 1, "mode": mode, "story": story, "criteria": mapped,
            "questions": questions, "status": "needs_clarification" if questions else "awaiting_approval",
            "summary": proposal["summary"], "expression": proposal["expression"],
            "target": "sample/shipping.py", "verification": "shipping-catalog-v1",
            "usage": usage or {"model": None, "api_calls": 0, "cost_usd": 0}}
    return plan

