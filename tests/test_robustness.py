import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from story_pr.analysis import analyze
from story_pr.cli import main
from story_pr.core import WorkflowError, read_story
from story_pr.execution import trusted_target, TEMPLATE, verify
from story_pr.provider import propose


class RobustnessTests(unittest.TestCase):
    def test_invalid_provider_shapes(self):
        for result in ({}, [], {"expression": 5}, {"expression": "5", "questions": [5], "summary": "x"}):
            with self.assertRaises(WorkflowError):
                analyze(read_story("stories/free-shipping.json"), result)

    def test_changed_file_structure(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root)/"sample"/"shipping.py"
            path.parent.mkdir()
            path.write_text("import os\n"+TEMPLATE.format(expression="5"))
            with self.assertRaises(WorkflowError):
                trusted_target(root)

    def test_human_review_evidence(self):
        r = verify("5", [{"id": "AC1", "text": "Unknown requirement"}])
        self.assertEqual(r[0]["status"], "needs_human_review")

    @patch.dict("os.environ", {"OPENAI_API_KEY": "synthetic-test-key"})
    @patch("story_pr.provider.request")
    def test_provider_contract_success(self, request):
        request.return_value = {"status": "completed", "output": [{"content": [{"type": "output_text", "text":
            json.dumps({"expression": "0 if subtotal >= 50 else 5", "questions": [], "summary": "Change fee"})}]}],
            "usage": {"input_tokens": 100, "output_tokens": 50}}
        proposal, usage = propose(read_story("stories/free-shipping.json"))
        self.assertEqual(analyze(read_story("stories/free-shipping.json"), proposal)["status"], "awaiting_approval")
        self.assertEqual(usage["input_tokens"], 100)
        self.assertIsNone(usage["cost_usd"])
        body = request.call_args.args[2]
        self.assertFalse(body["store"])
        self.assertEqual(body["max_output_tokens"], 1200)
