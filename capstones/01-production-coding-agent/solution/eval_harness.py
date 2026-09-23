"""Capstone 1: eval harness scoring the coding agent across the sample-repo
set. Reference solution. See ../README.md.

Generic over the agent implementation (Module 16's evaluate_dataset shape:
the agent function is injected, not imported), so this harness can score
any coding-agent function with a compatible signature.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

SAMPLE_TASKS = [
    {"repo": "calculator", "task": "Fix the failing test in test_calculator.py."},
    {"repo": "strings", "task": "Fix the failing test in test_stringutils.py."},
    {"repo": "numbers", "task": "Fix the failing test in test_numberutils.py."},
]


async def run_eval(run_coding_agent_fn, client_factory, sample_repo_root: Path, tasks=None) -> dict:
    tasks = SAMPLE_TASKS if tasks is None else tasks
    results = []
    for item in tasks:
        with tempfile.TemporaryDirectory() as tmp:
            repo_copy = Path(tmp) / item["repo"]
            shutil.copytree(sample_repo_root / item["repo"], repo_copy)
            client = client_factory()
            outcome = await run_coding_agent_fn(client, repo_copy, item["task"])
            results.append({"repo": item["repo"], "status": outcome["status"]})

    passed = sum(1 for r in results if r["status"] == "success")
    total = len(tasks)
    return {"total": total, "passed": passed, "pass_rate": passed / total, "results": results}
