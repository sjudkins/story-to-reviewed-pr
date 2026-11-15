import os
import re
from urllib.parse import quote
from .http import request
from .analysis import extract_issue
from .core import WorkflowError


def validate_repo(repo):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", repo):
        raise WorkflowError("Repository must be owner/name")
    return repo


class GitHub:
    def __init__(self, repo, token=None):
        self.repo = validate_repo(repo)
        self.token = token or os.environ.get("GITHUB_TOKEN")

    def api(self, path, data=None, method=None):
        return request(f"https://api.github.com/repos/{self.repo}/{path}", self.token, data, method)

    def issue(self, number):
        if number < 1:
            raise WorkflowError("Issue number must be positive")
        story = extract_issue(self.api(f"issues/{number}"))
        story["source"] = f"https://github.com/{self.repo}/issues/{number}"
        return story
