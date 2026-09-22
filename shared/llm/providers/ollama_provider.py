"""Adapter for local models served by Ollama.

Verified against https://ollama.com/blog/tool-support and the ollama-python README
on 2026-09-22. Requires a local Ollama server (`ollama serve`) and a tool-calling
model pulled locally (default: qwen3:8b -- see shared/llm/pricing.py). Only
exercised by `live`-marked tests, since it needs a running local server rather than
a cloud API key.
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


class OllamaProvider(LLMProvider):
    def __init__(self, host: str | None = None) -> None:
        try:
            from ollama import AsyncClient
        except ImportError as exc:  # pragma: no cover
            raise ImportError("Install the 'ollama' package to use OllamaProvider") from exc
        self._client = AsyncClient(host=host) if host else AsyncClient()

    @staticmethod
    def _to_wire(messages: list[Message]) -> list[dict]:
        wire: list[dict] = []
        for m in messages:
            if m.role == Role.TOOL and m.tool_result:
                wire.append({"role": "tool", "content": m.tool_result.content})
                continue
            entry: dict = {"role": m.role.value, "content": m.content or ""}
            if m.tool_calls:
                entry["tool_calls"] = [
                    {"function": {"name": tc.name, "arguments": tc.arguments}}
                    for tc in m.tool_calls
                ]
            wire.append(entry)
        return wire

    @staticmethod
    def _tool_defs(tools: list[ToolDefinition] | None) -> list[dict] | None:
        if not tools:
            return None
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                },
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
            "messages": self._to_wire(messages),
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        tool_defs = self._tool_defs(tools)
        if tool_defs:
            kwargs["tools"] = tool_defs
        if response_schema:
            kwargs["format"] = response_schema
        response = await self._client.chat(**kwargs)
        wire_message = response["message"]
        raw_tool_calls = wire_message.get("tool_calls") or []
        tool_calls = [
            ToolCall(
                id=f"call_{i}",
                name=tc["function"]["name"],
                arguments=tc["function"]["arguments"],
            )
            for i, tc in enumerate(raw_tool_calls)
        ]
        message = Message(
            role=Role.ASSISTANT, content=wire_message.get("content") or None, tool_calls=tool_calls
        )
        usage = Usage(
            input_tokens=response.get("prompt_eval_count", 0) or 0,
            output_tokens=response.get("eval_count", 0) or 0,
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
            "messages": self._to_wire(messages),
            "stream": True,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        tool_defs = self._tool_defs(tools)
        if tool_defs:
            kwargs["tools"] = tool_defs
        async for part in await self._client.chat(**kwargs):
            content = part["message"].get("content") or ""
            if content:
                yield StreamChunk(delta=content)
            for tc in part["message"].get("tool_calls") or []:
                yield StreamChunk(
                    tool_call=ToolCall(
                        id="call_0",
                        name=tc["function"]["name"],
                        arguments=tc["function"]["arguments"],
                    )
                )
            if part.get("done"):
                yield StreamChunk(done=True)
