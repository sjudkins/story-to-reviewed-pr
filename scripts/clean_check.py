"""Validate documented commands in a temporary source copy and empty venv."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

source = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix="story-pr-clean-") as temporary:
    root = Path(temporary)
    checkout = root / "checkout"
    shutil.copytree(source, checkout, ignore=shutil.ignore_patterns(
        ".git", ".runs", ".venv", "__pycache__", "*.egg-info", "build", "dist", ".env"))
    subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(root / "venv")], check=True, timeout=60)
    python = root / "venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
    commands = [["-m", "unittest", "discover", "-s", "tests", "-v"], ["-m", "story_pr", "demo"],
                ["-m", "story_pr", "evaluate"], ["scripts/local_demo.py", "--approve-synthetic-fixture"]]
    results = []
    for command in commands:
        result = subprocess.run([str(python), *command], cwd=checkout, capture_output=True, text=True, timeout=60)
        results.append({"command": "python " + " ".join(command), "exit_code": result.returncode})
        if result.returncode:
            print(result.stdout, result.stderr)
            raise SystemExit(result.returncode)
    print(json.dumps({"python": sys.version.split()[0], "environment": "fresh venv without pip or third-party packages",
                      "checks": results}, indent=2))
