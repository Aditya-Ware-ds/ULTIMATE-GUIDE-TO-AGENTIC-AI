"""Provider-agnostic LLM client used by every lab in this curriculum.

from shared.llm import get_client, Message, Role

client = get_client()  # LLM_PROVIDER env var, default "mock"
response = await client.complete([Message(role=Role.USER, content="hi")])
"""

from shared.llm.client import LLMClient, get_client
from shared.llm.mock import MockLLMProvider
from shared.llm.types import (
    CompletionResponse,
    Message,
    Role,
    StreamChunk,
    ToolCall,
    ToolDefinition,
    ToolResult,
    Usage,
)

__all__ = [
    "LLMClient",
    "get_client",
    "MockLLMProvider",
    "CompletionResponse",
    "Message",
    "Role",
    "StreamChunk",
    "ToolCall",
    "ToolDefinition",
    "ToolResult",
    "Usage",
]
