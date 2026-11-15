# Story to Reviewed PR

A focused Python CLI portfolio prototype: user story to reviewed plan, controlled
sample change, trusted verification evidence, and gated draft PR.

Requires Python 3.11+. No third-party runtime packages needed from a checkout:

```sh
python -m story_pr demo
python -m unittest discover -s tests -v
```

The demo is a **deterministic fixture**, not an AI performance claim. It loads
stories/free-shipping.json and shows a plan without making changes. The controlled
target is a small shipping-fee function in sample/shipping.py.

Optional installed CLI: `python -m pip install -e .`, then `story-pr demo`.
See [project plan](PROJECT_PLAN.md) for architecture and milestone scope.
