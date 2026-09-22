"""Provider-agnostic message and response types shared by every LLM adapter.

Every provider adapter (Anthropic, OpenAI, Gemini, Ollama, and the mock) translates
to and from these types, so lab code is written once against this shape and never
against a vendor SDK's own types.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Role(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class ToolDefinition:
    """A tool the model may call, described as JSON Schema (the shape every current
    provider converges on, even though each wraps it slightly differently on the wire).
    """

    name: str
    description: str
    parameters: dict[str, Any]


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class ToolResult:
    tool_call_id: str
    content: str
    is_error: bool = False


@dataclass
class Message:
    role: Role
    content: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_result: ToolResult | None = None


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class CompletionResponse:
    message: Message
    usage: Usage
    model: str
    finish_reason: str
    raw: Any = None


@dataclass
class StreamChunk:
    delta: str = ""
    tool_call: ToolCall | None = None
    done: bool = False
