"""Lab 14.01: a browser-automation agent with a small, allowlisted action
vocabulary. See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/14-browser-and-computer-use-agents/labs/01-browser-task-agent/tests
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from shared.llm import (  # noqa: F401 -- used once you implement run_browser_agent below
    Message,
    Role,
)
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
    """Raise ValueError if `url` doesn't start with any of `allowed_prefixes`
    (see lessons/01-browser-automation.md); otherwise navigate and return a
    confirmation string.

    TODO: implement this.
    """
    raise NotImplementedError


def click(session: BrowserSession, selector: str) -> str:
    """TODO: implement this. Return a confirmation string."""
    raise NotImplementedError


def get_text(session: BrowserSession, selector: str) -> str:
    """TODO: implement this."""
    raise NotImplementedError


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
    """Return {"goto": ..., "click": ..., "get_text": ...}, each a callable
    taking only the model-supplied arguments (bind `session` and
    `allowed_prefixes` via closure).

    TODO: implement this.
    """
    raise NotImplementedError


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    """Same contract as prior modules' dispatch.

    TODO: implement this.
    """
    raise NotImplementedError


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
    """Run the ReAct-style loop (Module 04) with this lab's three tools.
    Return the model's final text answer, or a "Stopped after N steps..."
    message if max_steps is exhausted without one.

    TODO: implement this.
    """
    raise NotImplementedError
