import unittest
from story_pr.core import walkthrough


class FoundationTests(unittest.TestCase):
    def test_fixture_never_claims_implementation(self):
        result = walkthrough("stories/free-shipping.json")
        self.assertEqual(result["mode"], "fixture")
        self.assertEqual(result["status"], "planned_only")
        self.assertEqual(result["publication"], "disabled")
