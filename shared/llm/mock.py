"""A scriptable fake LLM provider so every test in this repo runs offline, with no
API keys and no network calls (Ground Rule: 'tests run without API keys').

Usage:
    provider = MockLLMProvider()
    provider.add_text("hello")
    provider.add_tool_call("get_weather", {"city": "Paris"})
    response = await provider.complete(messages, model="mock-model")
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


class MockLLMProvider(LLMProvider):
    def __init__(self, script: list[Message] | None = None) -> None:
        self._script: list[Message] = list(script) if script else []
        self.calls: list[dict] = []

    def add_response(self, message: Message) -> MockLLMProvider:
        self._script.append(message)
        return self

    def add_text(self, text: str) -> MockLLMProvider:
        return self.add_response(Message(role=Role.ASSISTANT, content=text))

    def add_tool_call(
        self, name: str, arguments: dict, call_id: str | None = None
    ) -> MockLLMProvider:
        call_id = call_id or f"call_{len(self._script)}"
        return self.add_response(
            Message(
                role=Role.ASSISTANT,
                tool_calls=[ToolCall(id=call_id, name=name, arguments=arguments)],
            )
        )

    @property
    def call_count(self) -> int:
        return len(self.calls)

    @property
    def exhausted(self) -> bool:
        return not self._script

    async def complete(
        self,
        messages: list[Message],
        *,
        model: str = "mock-model",
        tools: list[ToolDefinition] | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
        response_schema: dict | None = None,
    ) -> CompletionResponse:
        self.calls.append({"messages": messages, "model": model, "tools": tools})
        if not self._script:
            raise AssertionError(
                "MockLLMProvider ran out of scripted responses. "
                "Call .add_text()/.add_tool_call() once per expected model turn."
            )
        message = self._script.pop(0)
        input_tokens = sum(len(m.content or "") for m in messages) // 4
        output_tokens = len(message.content or "") // 4
        finish_reason = "tool_calls" if message.tool_calls else "stop"
        return CompletionResponse(
            message=message,
            usage=Usage(input_tokens=input_tokens, output_tokens=output_tokens),
            model=model,
            finish_reason=finish_reason,
        )

    async def stream(
        self,
        messages: list[Message],
        *,
        model: str = "mock-model",
        tools: list[ToolDefinition] | None = None,
        max_tokens: int = 1024,
        temperature: float = 1.0,
    ) -> AsyncIterator[StreamChunk]:
        response = await self.complete(
            messages, model=model, tools=tools, max_tokens=max_tokens, temperature=temperature
        )
        text = response.message.content or ""
        for i, word in enumerate(text.split(" ")):
            yield StreamChunk(delta=word if i == 0 else f" {word}")
        for tool_call in response.message.tool_calls:
            yield StreamChunk(tool_call=tool_call)
        yield StreamChunk(done=True)
