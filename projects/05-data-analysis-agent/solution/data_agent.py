"""Project 05: a data-analysis agent that writes and runs Python inside
shared/sandbox/ to answer questions about a bundled CSV. Reference solution.
See ../README.md.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from shared.llm import Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult
from shared.sandbox.code_sandbox import run_python


def run_analysis(code: str, dataset_dir: Path) -> str:
    result = run_python(code, cwd=dataset_dir)
    if not result.success:
        return f"Error running code:\n{result.stderr}"
    return result.stdout


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
    return {"run_analysis": lambda code: run_analysis(code, dataset_dir)}


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    if tool_call.name not in registry:
        return ToolResult(
            tool_call_id=tool_call.id, content=f"Unknown tool: {tool_call.name}", is_error=True
        )
    function = registry[tool_call.name]
    try:
        result = function(**tool_call.arguments)
        return ToolResult(tool_call_id=tool_call.id, content=str(result))
    except Exception as exc:
        return ToolResult(
            tool_call_id=tool_call.id, content=f"Tool execution failed: {exc}", is_error=True
        )


_SYSTEM_PROMPT = (
    "You are a data-analysis agent. You have a run_analysis tool that runs a "
    "Python script (standard library only) against sales.csv in its working "
    "directory. Write and run code to answer the question, then give a final "
    "answer with no further tool calls."
)


async def run_data_analysis_agent(client, dataset_dir: Path, task: str, max_steps: int = 6) -> str:
    messages: list[Message] = [
        Message(role=Role.SYSTEM, content=_SYSTEM_PROMPT),
        Message(role=Role.USER, content=task),
    ]
    registry = build_tool_registry(dataset_dir)
    for _ in range(max_steps):
        response = await client.complete(messages, tools=TOOLS)
        if not response.message.tool_calls:
            return response.message.content or ""
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            result = dispatch(tool_call, registry)
            messages.append(Message(role=Role.TOOL, tool_result=result))
    return f"Stopped after {max_steps} steps without a final answer."
