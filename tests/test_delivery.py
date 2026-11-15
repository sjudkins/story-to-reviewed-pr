import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
from story_pr.core import WorkflowError
from story_pr.delivery import publish
from story_pr.execution import execute, TEMPLATE
from story_pr.evaluation import evaluate
from test_execution import plan


class DeliveryTests(unittest.TestCase):
    def test_evaluation(self):
        result = evaluate()
        self.assertEqual(result["expectations_met"], result["count"])
        self.assertEqual(sum(c["publication_allowed"] for c in result["cases"]), 1)

    def setup_run(self, root, expression=None):
        target = Path(root)/"sample"/"shipping.py"
        target.parent.mkdir()
        target.write_text(TEMPLATE.format(expression="5"), encoding="utf-8")
        p = plan(expression)
        r = execute(p, p["approval_digest"], root, Path(root)/"runs")
        config = Path(root)/"config.toml"
        config.write_text('repository="owner/demo"\nbase_branch="main"\npublication_enabled=true\n')
        return Path(root)/"runs"/r["run_id"], config

    def test_failed_report_never_calls_github(self):
        with tempfile.TemporaryDirectory() as root:
            run, config = self.setup_run(root, "5")
            client = Mock()
            with self.assertRaisesRegex(WorkflowError, "Publication blocked"):
                publish(run, config, client=client)
            client.api.assert_not_called()

    def test_existing_pr_reused(self):
        with tempfile.TemporaryDirectory() as root:
            run, config = self.setup_run(root)
            client = Mock()
            client.api.return_value = [{"html_url": "https://github.com/owner/demo/pull/1", "base": {"ref": "main"}, "state": "open"}]
            self.assertTrue(publish(run, config, client=client)["reused"])
            self.assertEqual(client.api.call_count, 1)

    def test_tampered_report_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            run, config = self.setup_run(root)
            path = run/"report.json"
            report = json.loads(path.read_text())
            report["criteria"][0]["cases"][0]["observed"] = 999
            path.write_text(json.dumps(report))
            with self.assertRaises(WorkflowError):
                publish(run, config, client=Mock())
