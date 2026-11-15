"""Bounded JSON HTTPS; never follow redirects carrying credentials."""
import json
import urllib.request
import urllib.error
from .core import WorkflowError


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request(url, token=None, data=None, method=None):
    headers = {"Accept": "application/json", "User-Agent": "story-to-reviewed-pr"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = None if data is None else json.dumps(data).encode()
    if body:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=30) as response:
            raw = response.read(256_001)
        if len(raw) > 256_000:
            raise WorkflowError("Remote response exceeds 256 KB")
        return json.loads(raw)
    except urllib.error.HTTPError as exc:
        raise WorkflowError(f"Remote request failed (HTTP {exc.code}); check access/rate limit") from None
    except (urllib.error.URLError, TimeoutError):
        raise WorkflowError("Remote request timed out or could not connect") from None

