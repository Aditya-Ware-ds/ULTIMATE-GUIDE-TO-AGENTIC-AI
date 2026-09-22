"""Run: uv run python curriculum/03-tool-use/examples/dispatch_demo.py

Shows dispatching a tool call to a real function, including the unknown-tool and
exception-during-execution failure paths. See lessons/02-dispatch-and-execution.md.
"""

from __future__ import annotations

from collections.abc import Callable

from shared.llm.types import ToolCall, ToolResult


def add(a: float, b: float) -> float:
    return a + b


def divide(a: float, b: float) -> float:
    return a / b  # can raise ZeroDivisionError


REGISTRY: dict[str, Callable[..., object]] = {"add": add, "divide": divide}


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    if tool_call.name not in registry:
        return ToolResult(
            tool_call_id=tool_call.id,
            content=f"Unknown tool: {tool_call.name}",
            is_error=True,
        )
    function = registry[tool_call.name]
    try:
        result = function(**tool_call.arguments)
        return ToolResult(tool_call_id=tool_call.id, content=str(result))
    except Exception as exc:
        return ToolResult(
            tool_call_id=tool_call.id, content=f"Tool execution failed: {exc}", is_error=True
        )


def main() -> None:
    calls = [
        ToolCall(id="1", name="add", arguments={"a": 2, "b": 3}),
        ToolCall(id="2", name="divide", arguments={"a": 10, "b": 0}),
        ToolCall(id="3", name="frobnicate", arguments={}),
    ]
    for call in calls:
        result = dispatch(call, REGISTRY)
        status = "ERROR" if result.is_error else "OK"
        print(f"[{status}] {call.name}({call.arguments}) -> {result.content}")


if __name__ == "__main__":
    main()
