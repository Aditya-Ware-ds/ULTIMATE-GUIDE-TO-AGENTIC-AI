"""Capstone 1: production coding agent. See ../README.md and
../ARCHITECTURE.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest capstones/01-production-coding-agent/tests
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from shared.llm import Message, Role  # noqa: F401 -- used once you implement run_coding_agent below
from shared.llm.types import ToolCall, ToolDefinition, ToolResult
from shared.sandbox.shell_sandbox import (  # noqa: F401 -- used once you implement run_tests below
    ShellResult,
    run_shell,
)


def resolve_within_repo(repo_root: Path, relative_path: str) -> Path:
    """Resolve `relative_path` against `repo_root` and raise ValueError if the
    resolved path is not inside `repo_root`.

    TODO: implement this.
    """
    raise NotImplementedError


def read_file(repo_root: Path, relative_path: str) -> str:
    """TODO: implement this using resolve_within_repo."""
    raise NotImplementedError


def write_file(repo_root: Path, relative_path: str, content: str) -> str:
    """TODO: implement this using resolve_within_repo. Return a short confirmation string."""
    raise NotImplementedError


def run_tests(repo_root: Path) -> ShellResult:
    """Run `pytest -q` in `repo_root` via shared.sandbox.shell_sandbox.run_shell.

    TODO: implement this.
    """
    raise NotImplementedError


READ_FILE_TOOL = ToolDefinition(
    name="read_file",
    description="Read a file's contents, given a path relative to the repo root.",
    parameters={
        "type": "object",
        "properties": {"relative_path": {"type": "string"}},
        "required": ["relative_path"],
    },
)

WRITE_FILE_TOOL = ToolDefinition(
    name="write_file",
    description="Overwrite a file's contents, given a path relative to the repo root.",
    parameters={
        "type": "object",
        "properties": {
            "relative_path": {"type": "string"},
            "content": {"type": "string"},
        },
        "required": ["relative_path", "content"],
    },
)

RUN_TESTS_TOOL = ToolDefinition(
    name="run_tests",
    description="Run the repo's test suite and return its output.",
    parameters={"type": "object", "properties": {}, "required": []},
)

TOOLS = [READ_FILE_TOOL, WRITE_FILE_TOOL, RUN_TESTS_TOOL]


def build_tool_registry(repo_root: Path) -> dict[str, Callable]:
    """Return {"read_file": ..., "write_file": ..., "run_tests": ...}, each a
    callable that takes only the model-supplied arguments (repo_root bound
    via closure). "run_tests"'s callable should return
    `result.stdout + result.stderr` as a string.

    TODO: implement this.
    """
    raise NotImplementedError


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    """Same contract as prior modules' dispatch.

    TODO: implement this.
    """
    raise NotImplementedError


_SYSTEM_PROMPT = (
    "You are a coding agent. You have read_file, write_file, and run_tests tools, "
    "scoped to a single repo. Investigate the failing test, fix the bug, and "
    "verify with run_tests. When the tests pass, give a final answer with no "
    "further tool calls."
)


async def run_coding_agent(client, repo_root: Path, task: str, max_steps: int = 6) -> dict:
    """Run the ReAct-style loop (Module 04) with this capstone's three tools.

    After the loop ends (naturally or via max_steps), independently
    re-run the tests (do not trust the model's own claim of success) and
    return:
      {"status": "success", "steps": <int>, "output": <passing test output>}
      or
      {"status": "failed", "steps": <int>, "output": <failing test output>}

    TODO: implement this.
    """
    raise NotImplementedError
