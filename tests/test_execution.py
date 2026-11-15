import copy
import tempfile
import unittest
from pathlib import Path
from story_pr.analysis import analyze, fingerprint
from story_pr.core import read_story, WorkflowError
from story_pr.execution import execute, parse_expression, TEMPLATE, lock


def plan(expression=None):
    p = analyze(read_story("stories/free-shipping.json"))
    if expression is not None:
        p["expression"] = expression
    p["approval_digest"] = fingerprint(p)
    return p


class ExecutionTests(unittest.TestCase):
    def test_success_failure_and_rerun(self):
        with tempfile.TemporaryDirectory() as root:
            target = Path(root)/"sample"/"shipping.py"
            target.parent.mkdir()
            target.write_text(TEMPLATE.format(expression="5"), encoding="utf-8")
            before = target.read_bytes()
            for expr, status in [(None, "passed"), ("5", "failed")]:
                p = plan(expr)
                r = execute(p, p["approval_digest"], root, Path(root)/"runs")
                self.assertEqual(r["status"], status)
                self.assertEqual(r["publication_allowed"], status == "passed")
                self.assertEqual(execute(p, p["approval_digest"], root, Path(root)/"runs"), r)
                self.assertEqual(target.read_bytes(), before)

    def test_approval_is_bound(self):
        p = plan()
        p["expression"] = "5"
        with self.assertRaisesRegex(WorkflowError, "Approval"):
            execute(p, p["approval_digest"], ".", ".runs")

    def test_dangerous_expressions(self):
        for expr in ["__import__('os').system('x')", "subtotal ** 999", "[x for x in []]", "subtotal.foo", "True", "1e999", "subtotal + 1"]:
            with self.subTest(expr=expr), self.assertRaises(WorkflowError):
                parse_expression(expr)

    def test_lock(self):
        with tempfile.TemporaryDirectory() as root:
            with lock(root):
                with self.assertRaises(WorkflowError):
                    with lock(root):
                        self.fail("lock bypassed")
