"""Adapter for Anthropic's Messages API.

Verified against https://platform.claude.com/docs/en/api/messages,
https://platform.claude.com/docs/en/build-with-claude/structured-outputs, and
https://platform.claude.com/docs/en/build-with-claude/vision on 2026-09-22
(Structured Outputs is GA, no beta header required; the request parameter is
`output_config: {"format": {"type": "json_schema", "schema": ...}}`. Vision's
base64 image content block is `{"type": "image", "source": {"type": "base64",
"media_type": ..., "data": ...}}`, supporting image/jpeg, image/png,
image/gif, and image/webp).
Only exercised by `live`-marked tests -- re-check those URLs if this stops working.
"""

from __future__ import annotations

from collections.abc import AsyncIterator

from shared.llm.base import LLMProvider
from shared.llm.types import (
    CompletionResponse,
    Message,
    Role,
    StreamChunk,
    ToolCall,
    ToolDefinition,
    Usage,
)


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str | None = None) -> None:
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover - exercised only when SDK missing
            raise ImportError("Install the 'anthropic' package to use AnthropicProvider") from exc
        self._client = anthropic.AsyncAnthropic(api_key=api_key)

    @staticmethod
    def _to_wire(messages: list[Message]) -> tuple[str | None, list[dict]]:
        system: str | None = None
        wire: list[dict] = []
        for m in messages:
            if m.role == Role.SYSTEM:
                system = m.content
                continue
            if m.role == Role.TOOL and m.tool_result:
                wire.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": m.tool_result.tool_call_id,
                                "content": m.tool_result.content,
                                "is_error": m.tool_result.is_error,
                            }
                        ],
                    }
                )
                continue
            if m.tool_calls:
                content: list[dict] | str = [
                    {"type": "tool_use", "id": tc.id, "name": tc.name, "input": tc.arguments}
                    for tc in m.tool_calls
                ]
            elif m.images:
                # Images before text performs best (Module 15, verified against
                # https://platform.claude.com/docs/en/build-with-claude/vision).
                content = [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": img.media_type,
                            "data": img.data_base64,
                        },
                    }
                    for img in m.images
                ]
                if m.content:
                    content.append({"type": "text", "text": m.content})
            else:
                content = m.content or ""
            wire.append({"role": m.role.value, "content": content})
        return system, wire

    @staticmethod
    def _tool_defs(tools: list[ToolDefinition] | None) -> list[dict] | None:
        if not tools:
            return None
        return [
            {"name": t.name, "description": t.description, "input_schema": t.parameters}
            for t in tools
        ]

    async def complete(
        self,
        messages: list[Message],
        *,
        model: str,
        tools: list[ToolDefinition] | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
        response_schema: dict | None = None,
    ) -> CompletionResponse:
        system, wire_messages = self._to_wire(messages)
        kwargs: dict = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": wire_messages,
        }
        if system:
            kwargs["system"] = system
        tool_defs = self._tool_defs(tools)
        if tool_defs:
            kwargs["tools"] = tool_defs
        if response_schema:
            kwargs["output_config"] = {"format": {"type": "json_schema", "schema": response_schema}}
        response = await self._client.messages.create(**kwargs)
        text = "".join(b.text for b in response.content if b.type == "text")
        tool_calls = [
            ToolCall(id=b.id, name=b.name, arguments=b.input)
            for b in response.content
            if b.type == "tool_use"
        ]
        message = Message(role=Role.ASSISTANT, content=text or None, tool_calls=tool_calls)
        usage = Usage(
            input_tokens=response.usage.input_tokens, output_tokens=response.usage.output_tokens
        )
        return CompletionResponse(
            message=message,
            usage=usage,
            model=model,
            finish_reason=response.stop_reason or "stop",
            raw=response,
        )

    async def stream(
        self,
        messages: list[Message],
        *,
        model: str,
        tools: list[ToolDefinition] | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
    ) -> AsyncIterator[StreamChunk]:
        system, wire_messages = self._to_wire(messages)
        kwargs: dict = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": wire_messages,
        }
        if system:
            kwargs["system"] = system
        tool_defs = self._tool_defs(tools)
        if tool_defs:
            kwargs["tools"] = tool_defs
        async with self._client.messages.stream(**kwargs) as stream:
            async for text in stream.text_stream:
                yield StreamChunk(delta=text)
            final = await stream.get_final_message()
            for b in final.content:
                if b.type == "tool_use":
                    yield StreamChunk(tool_call=ToolCall(id=b.id, name=b.name, arguments=b.input))
            yield StreamChunk(done=True)
