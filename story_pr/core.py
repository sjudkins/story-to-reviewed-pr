import json
from pathlib import Path


class WorkflowError(Exception):
    pass


def read_story(path: str) -> dict:
    p = Path(path)
    if p.stat().st_size > 32_000:
        raise WorkflowError("Story exceeds 32 KB limit")
    story = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(story, dict) or not isinstance(story.get("title"), str):
        raise WorkflowError("Story must be an object with a title")
    return story


def walkthrough(path: str) -> dict:
    story = read_story(path)
    return {
        "mode": "fixture", "title": story["title"],
        "criteria": story.get("criteria", []),
        "plan": ["Review shipping rule", "Request explicit approval", "Verify trusted examples"],
        "status": "planned_only", "publication": "disabled",
        "notice": "Deterministic fixture; no model call or implementation executed.",
    }
