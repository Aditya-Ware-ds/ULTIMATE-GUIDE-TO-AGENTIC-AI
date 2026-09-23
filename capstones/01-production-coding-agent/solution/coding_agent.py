"""Capstone 1: production coding agent. Reference solution. See ../README.md
and ../ARCHITECTURE.md.

This is Module 13's sandboxed coding-agent pattern, generalized to run
against any repo_root -- the same read_file/write_file/run_tests tools,
the same independent post-loop test re-run (never trust the model's own
claim of success).
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from shared.llm import Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult
from shared.sandbox.shell_sandbox import ShellResult, run_shell


def resolve_within_repo(repo_root: Path, relative_path: str) -> Path:
    candidate = (repo_root / relative_path).resolve()
    if not candidate.is_relative_to(repo_root.resolve()):
        raise ValueError(f"Path {relative_path!r} escapes the repo root")
    return candidate


def read_file(repo_root: Path, relative_path: str) -> str:
    return resolve_within_repo(repo_root, relative_path).read_text()


def write_file(repo_root: Path, relative_path: str, content: str) -> str:
    path = resolve_within_repo(repo_root, relative_path)
    path.write_text(content)
    return f"Wrote {len(content)} characters to {relative_path}"


def run_tests(repo_root: Path) -> ShellResult:
    return run_shell("pytest -q", cwd=repo_root)


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
    def _run_tests() -> str:
        result = run_tests(repo_root)
        return result.stdout + result.stderr

    return {
        "read_file": lambda relative_path: read_file(repo_root, relative_path),
        "write_file": lambda relative_path, content: write_file(repo_root, relative_path, content),
        "run_tests": _run_tests,
    }


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
    "You are a coding agent. You have read_file, write_file, and run_tests tools, "
    "scoped to a single repo. Investigate the failing test, fix the bug, and "
    "verify with run_tests. When the tests pass, give a final answer with no "
    "further tool calls."
)


async def run_coding_agent(client, repo_root: Path, task: str, max_steps: int = 6) -> dict:
    messages: list[Message] = [
        Message(role=Role.SYSTEM, content=_SYSTEM_PROMPT),
        Message(role=Role.USER, content=task),
    ]
    registry = build_tool_registry(repo_root)
    steps_used = 0
    for step in range(max_steps):
        steps_used = step + 1
        response = await client.complete(messages, tools=TOOLS)
        if not response.message.tool_calls:
            break
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            result = dispatch(tool_call, registry)
            messages.append(Message(role=Role.TOOL, tool_result=result))

    # Never trust the model's own claim that it's done (Module 12 lesson 02):
    # independently re-run the tests as the actual, mechanical status check.
    final_check = run_tests(repo_root)
    if final_check.success:
        return {"status": "success", "steps": steps_used, "output": final_check.stdout}
    return {
        "status": "failed",
        "steps": steps_used,
        "output": final_check.stdout + final_check.stderr,
    }
