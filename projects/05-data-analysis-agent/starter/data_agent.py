"""Project 05: a data-analysis agent that writes and runs Python inside
shared/sandbox/ to answer questions about a bundled CSV. See ../README.md
for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest projects/05-data-analysis-agent/tests
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from shared.llm import (  # noqa: F401 -- used once you implement run_data_analysis_agent below
    Message,
    Role,
)
from shared.llm.types import ToolCall, ToolDefinition, ToolResult
from shared.sandbox.code_sandbox import (
    run_python,  # noqa: F401 -- used once you implement run_analysis below
)


def run_analysis(code: str, dataset_dir: Path) -> str:
    """Run `code` via shared.sandbox.code_sandbox.run_python with
    cwd=dataset_dir. Return result.stdout on success, or
    f"Error running code:\\n{result.stderr}" if it failed.

    TODO: implement this.
    """
    raise NotImplementedError


RUN_ANALYSIS_TOOL = ToolDefinition(
    name="run_analysis",
    description=(
        "Run a Python script (using only the standard library) in a sandboxed "
        "subprocess whose working directory contains sales.csv. Print any "
        "results you need with print()."
    ),
    parameters={
        "type": "object",
        "properties": {"code": {"type": "string"}},
        "required": ["code"],
    },
)

TOOLS = [RUN_ANALYSIS_TOOL]


def build_tool_registry(dataset_dir: Path) -> dict[str, Callable]:
    """Return {"run_analysis": ...}, a callable taking only the
    model-supplied `code` argument (bind `dataset_dir` via closure).

    TODO: implement this.
    """
    raise NotImplementedError


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    """Same contract as prior modules' dispatch.

    TODO: implement this.
    """
    raise NotImplementedError


_SYSTEM_PROMPT = (
    "You are a data-analysis agent. You have a run_analysis tool that runs a "
    "Python script (standard library only) against sales.csv in its working "
    "directory. Write and run code to answer the question, then give a final "
    "answer with no further tool calls."
)


async def run_data_analysis_agent(client, dataset_dir: Path, task: str, max_steps: int = 6) -> str:
    """Run the ReAct-style loop (Module 04) with this project's one tool.
    Return the model's final text answer, or a "Stopped after N steps..."
    message if max_steps is exhausted without one.

    TODO: implement this.
    """
    raise NotImplementedError
