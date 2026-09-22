"""Adapter for OpenAI's Responses API (the current standard for tool calling, having
superseded Chat Completions for new integrations).

Verified against https://developers.openai.com/api/docs/guides/function-calling on
2026-09-22. Only exercised by `live`-marked tests -- re-check that URL if this stops
working, and re-check before pinning a specific model id.
"""

from __future__ import annotations

import json
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


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str | None = None) -> None:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:  # pragma: no cover
            raise ImportError("Install the 'openai' package to use OpenAIProvider") from exc
        self._client = AsyncOpenAI(api_key=api_key)

    @staticmethod
    def _to_wire(messages: list[Message]) -> list[dict]:
        wire: list[dict] = []
        for m in messages:
            if m.role == Role.TOOL and m.tool_result:
                wire.append(
                    {
                        "type": "function_call_output",
                        "call_id": m.tool_result.tool_call_id,
                        "output": m.tool_result.content,
                    }
                )
                continue
            if m.tool_calls:
                for tc in m.tool_calls:
                    wire.append(
                        {
                            "type": "function_call",
                            "call_id": tc.id,
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments),
                        }
                    )
                continue
            wire.append({"role": m.role.value, "content": m.content or ""})
        return wire

    @staticmethod
    def _tool_defs(tools: list[ToolDefinition] | None) -> list[dict] | None:
        if not tools:
            return None
        return [
            {
                "type": "function",
                "name": t.name,
                "description": t.description,
                "parameters": t.parameters,
            }
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
        kwargs: dict = {
            "model": model,
            "input": self._to_wire(messages),
            "max_output_tokens": max_tokens,
            "temperature": temperature,
        }
        tool_defs = self._tool_defs(tools)
        if tool_defs:
            kwargs["tools"] = tool_defs
        if response_schema:
            kwargs["text"] = {
                "format": {"type": "json_schema", "name": "response", "schema": response_schema}
            }
        response = await self._client.responses.create(**kwargs)
        tool_calls = [
            ToolCall(id=item.call_id, name=item.name, arguments=json.loads(item.arguments))
            for item in response.output
            if item.type == "function_call"
        ]
        text = getattr(response, "output_text", None)
        message = Message(role=Role.ASSISTANT, content=text or None, tool_calls=tool_calls)
        usage = Usage(
            input_tokens=response.usage.input_tokens if response.usage else 0,
            output_tokens=response.usage.output_tokens if response.usage else 0,
        )
        finish_reason = "tool_calls" if tool_calls else "stop"
        return CompletionResponse(
            message=message, usage=usage, model=model, finish_reason=finish_reason, raw=response
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
        kwargs: dict = {
            "model": model,
            "input": self._to_wire(messages),
            "max_output_tokens": max_tokens,
            "temperature": temperature,
        }
        tool_defs = self._tool_defs(tools)
        if tool_defs:
            kwargs["tools"] = tool_defs
        async with self._client.responses.stream(**kwargs) as stream:
            async for event in stream:
                if event.type == "response.output_text.delta":
                    yield StreamChunk(delta=event.delta)
            final = await stream.get_final_response()
            for item in final.output:
                if item.type == "function_call":
                    yield StreamChunk(
                        tool_call=ToolCall(
                            id=item.call_id, name=item.name, arguments=json.loads(item.arguments)
                        )
                    )
            yield StreamChunk(done=True)
