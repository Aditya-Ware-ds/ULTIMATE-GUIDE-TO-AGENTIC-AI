"""Lab 14.01: a browser-automation agent with a small, allowlisted action
vocabulary. Reference solution. See ../README.md.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from shared.llm import Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult


class BrowserSession(Protocol):
    def goto(self, url: str) -> None: ...
    def click(self, selector: str) -> None: ...
    def get_text(self, selector: str) -> str: ...


class PlaywrightBrowserSession:
    """Wraps a real Playwright sync `Page`. Requires the `playwright` package
    and its browser binaries (not part of this repo's default dependencies --
    see ../README.md's live-test instructions). Playwright itself is never
    imported here, so this class is safe to define even when it isn't
    installed.
    """

    def __init__(self, page) -> None:
        self._page = page

    def goto(self, url: str) -> None:
        self._page.goto(url)

    def click(self, selector: str) -> None:
        self._page.click(selector)

    def get_text(self, selector: str) -> str:
        return self._page.text_content(selector) or ""


def goto(session: BrowserSession, url: str, allowed_prefixes: tuple[str, ...]) -> str:
    if not any(url.startswith(prefix) for prefix in allowed_prefixes):
        raise ValueError(f"URL not allowed: {url!r}")
    session.goto(url)
    return f"Navigated to {url}"


def click(session: BrowserSession, selector: str) -> str:
    session.click(selector)
    return f"Clicked {selector}"


def get_text(session: BrowserSession, selector: str) -> str:
    return session.get_text(selector)


GOTO_TOOL = ToolDefinition(
    name="goto",
    description="Navigate the browser to a URL.",
    parameters={
        "type": "object",
        "properties": {"url": {"type": "string"}},
        "required": ["url"],
    },
)

CLICK_TOOL = ToolDefinition(
    name="click",
    description="Click the element matching a CSS selector.",
    parameters={
        "type": "object",
        "properties": {"selector": {"type": "string"}},
        "required": ["selector"],
    },
)

GET_TEXT_TOOL = ToolDefinition(
    name="get_text",
    description="Get the text content of the element matching a CSS selector.",
    parameters={
        "type": "object",
        "properties": {"selector": {"type": "string"}},
        "required": ["selector"],
    },
)

TOOLS = [GOTO_TOOL, CLICK_TOOL, GET_TEXT_TOOL]


def build_tool_registry(
    session: BrowserSession, allowed_prefixes: tuple[str, ...]
) -> dict[str, Callable]:
    return {
        "goto": lambda url: goto(session, url, allowed_prefixes),
        "click": lambda selector: click(session, selector),
        "get_text": lambda selector: get_text(session, selector),
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
    "You are a browser agent. You have goto, click, and get_text tools. "
    "Navigate to the given page and use them to answer the question. "
    "When you have the answer, give a final response with no further tool calls."
)


async def run_browser_agent(
    client,
    session: BrowserSession,
    task: str,
    allowed_prefixes: tuple[str, ...],
    max_steps: int = 6,
) -> str:
    messages: list[Message] = [
        Message(role=Role.SYSTEM, content=_SYSTEM_PROMPT),
        Message(role=Role.USER, content=task),
    ]
    registry = build_tool_registry(session, allowed_prefixes)
    for _ in range(max_steps):
        response = await client.complete(messages, tools=TOOLS)
        if not response.message.tool_calls:
            return response.message.content or ""
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            result = dispatch(tool_call, registry)
            messages.append(Message(role=Role.TOOL, tool_result=result))
    return f"Stopped after {max_steps} steps without a final answer."
