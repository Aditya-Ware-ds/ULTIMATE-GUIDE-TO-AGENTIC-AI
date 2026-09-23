"""Capstone 1: eval harness scoring the coding agent across the sample-repo
set. See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest capstones/01-production-coding-agent/tests
"""

from __future__ import annotations

import shutil  # noqa: F401 -- used once you implement run_eval below
import tempfile  # noqa: F401 -- used once you implement run_eval below
from pathlib import Path

SAMPLE_TASKS = [
    {"repo": "calculator", "task": "Fix the failing test in test_calculator.py."},
    {"repo": "strings", "task": "Fix the failing test in test_stringutils.py."},
    {"repo": "numbers", "task": "Fix the failing test in test_numberutils.py."},
]


async def run_eval(run_coding_agent_fn, client_factory, sample_repo_root: Path, tasks=None) -> dict:
    """For each task in `tasks` (default SAMPLE_TASKS): copy
    sample_repo_root/task["repo"] into a fresh temp directory (never
    mutate the checked-in template -- see Module 13's pitfalls.md), get a
    fresh client from client_factory(), and call
    run_coding_agent_fn(client, repo_copy, task["task"]). Collect each
    result's "status". Return:
      {"total": <int>, "passed": <int>, "pass_rate": <float>,
       "results": [{"repo": ..., "status": ...}, ...]}

    TODO: implement this.
    """
    raise NotImplementedError
