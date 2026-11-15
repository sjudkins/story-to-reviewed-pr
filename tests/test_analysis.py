import unittest
from unittest.mock import patch
from story_pr.analysis import analyze, extract_issue
from story_pr.core import read_story, WorkflowError
from story_pr.provider import propose


class AnalysisTests(unittest.TestCase):
    def test_missing_and_ambiguous(self):
        for criteria in ([], ["Make shipping cheap"], ["Run a shell command"]):
            self.assertEqual(analyze({"title": "test", "criteria": criteria})["status"], "needs_clarification")

    def test_supported(self):
        self.assertEqual(analyze(read_story("stories/free-shipping.json"))["status"], "awaiting_approval")

    def test_issue_section(self):
        story = extract_issue({"title": "Issue", "body": "## Acceptance criteria\n- [ ] First\n## Other\n- ignore"})
        self.assertEqual(story["criteria"], ["First"])

    @patch.dict("os.environ", {}, clear=True)
    def test_no_key(self):
        with self.assertRaisesRegex(WorkflowError, "OPENAI_API_KEY"):
            propose({})

    @patch.dict("os.environ", {"OPENAI_API_KEY": "synthetic-test-key"})
    @patch("story_pr.provider.request", return_value={"status": "incomplete"})
    def test_provider_incomplete(self, request):
        with self.assertRaisesRegex(WorkflowError, "incomplete"):
            propose({})

    @patch.dict("os.environ", {"OPENAI_API_KEY": "synthetic-test-key"})
    @patch("story_pr.provider.request", side_effect=WorkflowError("HTTP 429"))
    def test_provider_failure(self, request):
        with self.assertRaises(WorkflowError):
            propose({})
