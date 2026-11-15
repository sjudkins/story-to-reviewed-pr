"""Interpret a tiny expression language; never exec/eval/import generated Python."""
import ast
import contextlib
import difflib
import json
import math
from pathlib import Path
import tempfile
import time
from .analysis import CATALOG, analyze, fingerprint
from .core import WorkflowError

TEMPLATE = ('"""Small controlled target: shipping fee in dollars for a nonnegative subtotal."""\n'
            '\n\ndef shipping_fee(subtotal):\n    return {expression}\n')
ALLOWED = (ast.Expression, ast.IfExp, ast.Compare, ast.Name, ast.Load, ast.Constant, ast.GtE, ast.Lt)


def parse_expression(expression):
    if not isinstance(expression, str) or len(expression) > 200 or '\n' in expression:
        raise WorkflowError("Expression must be one line, at most 200 characters")
    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, RecursionError):
        raise WorkflowError("Invalid expression") from None
    nodes = list(ast.walk(tree))
    if len(nodes) > 50:
        raise WorkflowError("Expression exceeds 50 AST nodes")
    for node in nodes:
        if not isinstance(node, ALLOWED):
            raise WorkflowError(f"Unsupported expression node: {type(node).__name__}")
        if isinstance(node, ast.Name) and node.id != "subtotal":
            raise WorkflowError("Only subtotal is allowed")
        if isinstance(node, ast.Constant) and (type(node.value) not in (int, float) or
                not math.isfinite(node.value) or not 0 <= node.value <= 1_000_000):
            raise WorkflowError("Only finite numeric constants between 0 and 1000000 allowed")
        if isinstance(node, ast.Compare) and len(node.ops) != 1:
            raise WorkflowError("Chained comparisons unsupported")
    return tree.body


def interpret(node, subtotal):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return subtotal
    if isinstance(node, ast.IfExp):
        return interpret(node.body if interpret(node.test, subtotal) else node.orelse, subtotal)
    if isinstance(node, ast.Compare):
        left, right = interpret(node.left, subtotal), interpret(node.comparators[0], subtotal)
        return left >= right if isinstance(node.ops[0], ast.GtE) else left < right
    raise WorkflowError("Unsupported expression")


def trusted_target(root):
    root = Path(root).resolve(strict=True)
    path = root / "sample" / "shipping.py"
    if path.is_symlink() or path.parent.is_symlink() or not path.resolve(strict=True).is_relative_to(root):
        raise WorkflowError("Sample target must be a regular file within configured repository")
    if path.stat().st_size > 4000:
        raise WorkflowError("Sample target too large")
    text = path.read_text(encoding="utf-8")
    prefix, suffix = TEMPLATE.split("{expression}")
    if not text.startswith(prefix) or not text.endswith(suffix):
        raise WorkflowError("Unsupported sample file structure; expected controlled template")
    parse_expression(text[len(prefix):-len(suffix)])
    return path, text


@contextlib.contextmanager
def lock(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / ".lock"
    try:
        with path.open("x") as output:
            output.write("Active workflow; remove only after confirming no process is running.\n")
    except FileExistsError:
        raise WorkflowError("Another run owns the lock; inspect it before retrying") from None
    try:
        yield
    finally:
        path.unlink()


def checked_plan(plan, approval):
    payload = {k: v for k, v in plan.items() if k != "approval_digest"}
    digest = fingerprint(payload)
    if approval != digest or plan.get("approval_digest") != digest:
        raise WorkflowError("Approval must match the reviewed plan digest; changed plans need reapproval")
    # Re-derive criteria and status from source, not model assertions or edited mappings.
    canonical = analyze(plan["story"], {"expression": plan["expression"],
                        "summary": plan["summary"], "questions": []}, plan["mode"], plan["usage"])
    if plan["status"] != "awaiting_approval" or plan["questions"] or canonical["questions"]:
        raise WorkflowError("Resolve clarification requests before implementation")
    if plan["criteria"] != canonical["criteria"] or plan["target"] != "sample/shipping.py" or plan["verification"] != "shipping-catalog-v1":
        raise WorkflowError("Plan changed trusted target or verification mapping")
    parse_expression(plan["expression"])
    return digest


def verify(expression, criteria):
    node = parse_expression(expression)
    evidence = []
    for criterion in criteria:
        cases = []
        for subtotal, expected in CATALOG.get(criterion["text"], []):
            observed = interpret(node, subtotal)
            cases.append({"subtotal": subtotal, "expected": expected, "observed": observed,
                          "passed": type(observed) in (int, float) and observed == expected})
        status = "needs_human_review" if not cases else "verified" if all(c["passed"] for c in cases) else "unmet"
        evidence.append({"id": criterion["id"], "text": criterion["text"], "status": status,
                         "code": "sample/shipping.py:5", "cases": cases,
                         "scope": "Trusted finite examples via restricted AST interpreter; not exhaustive proof"})
    return evidence


def execute(plan, approval, root, runs):
    digest = checked_plan(plan, approval)
    target, before = trusted_target(root)
    after = TEMPLATE.format(expression=plan["expression"])
    run_id = fingerprint({"plan": digest, "before": before})[:20]
    directory = Path(runs) / run_id
    with lock(Path(runs)):
        if directory.exists():
            existing = json.loads((directory / "report.json").read_text(encoding="utf-8"))
            return existing
        directory.mkdir()
        started = time.perf_counter()
        try:
            # Copy only the allowed file. No git hooks, repo code, tools or tests are executed.
            with tempfile.TemporaryDirectory(prefix="story-pr-") as workspace:
                isolated = Path(workspace) / "sample" / "shipping.py"
                isolated.parent.mkdir()
                isolated.write_text(after, encoding="utf-8")
                _, written = trusted_target(workspace)
                expression = written.split("    return ", 1)[1].strip()
                evidence = verify(expression, plan["criteria"])
            diff = "".join(difflib.unified_diff(before.splitlines(True), after.splitlines(True),
                                              fromfile="a/sample/shipping.py", tofile="b/sample/shipping.py"))
            if len(diff) > 8000:
                raise WorkflowError("Diff exceeds limit")
            passed = bool(evidence) and all(e["status"] == "verified" for e in evidence) and bool(diff)
            report = {"version": 1, "run_id": run_id, "mode": plan["mode"],
                      "plan_digest": digest, "approved": True, "expression": plan["expression"],
                      "base_file_sha256": fingerprint(before), "target": str(target),
                      "status": "passed" if passed else "failed", "publication_allowed": passed,
                      "criteria": evidence, "diff": diff, "usage": plan["usage"],
                      "verification_seconds": round(time.perf_counter()-started, 6),
                      "execution": "restricted AST interpretation; arbitrary generated-code execution disabled"}
        except WorkflowError as exc:
            report = {"version": 1, "run_id": run_id, "mode": plan["mode"], "status": "blocked",
                      "publication_allowed": False, "reason": str(exc),
                      "criteria": [{"id": c["id"], "text": c["text"], "status": "blocked"} for c in plan["criteria"]]}
        (directory / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        (directory / "plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
        (directory / "report.md").write_text(markdown(report), encoding="utf-8")
        return report


def markdown(report):
    lines = [f"# Acceptance report — {report['mode']}", "", f"Status: {report['status']}",
             "", "Finite trusted examples are evidence, not exhaustive correctness proof.", ""]
    for criterion in report["criteria"]:
        lines.extend([f"## {criterion['id']}: {criterion['status']}", criterion["text"],
                      f"Code: {criterion.get('code', 'not changed')}",
                      "```json", json.dumps(criterion.get("cases", []), indent=2), "```", ""])
    if "diff" in report:
        lines.extend(["```diff", report["diff"], "```"])
    return "\n".join(lines)
