"""A real OpenTelemetry tracer pre-wired for GenAI semantic conventions, with an
in-memory exporter so labs and tests can inspect spans without a collector.

Span/attribute names follow the OTel GenAI semantic conventions (`gen_ai.*`) as
verified against https://opentelemetry.io/blog/2026/genai-observability/ on
2026-09-22: an `invoke_agent` span wraps the whole agent run, with nested `chat`
spans per model call and `execute_tool` spans per tool call. This is the schema
Module 17 (Observability & debugging) builds on.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

_exporter = InMemorySpanExporter()
_provider = TracerProvider(resource=Resource.create({"service.name": "agentic-ai-mastery"}))
_provider.add_span_processor(SimpleSpanProcessor(_exporter))
trace.set_tracer_provider(_provider)
_tracer = trace.get_tracer("agentic-ai-mastery")


def get_exported_spans() -> tuple[ReadableSpan, ...]:
    """All finished spans recorded so far -- used by tests and by Module 17's replay lab."""
    return _exporter.get_finished_spans()


def clear_exported_spans() -> None:
    _exporter.clear()


@contextmanager
def invoke_agent_span(agent_name: str, **attrs: Any) -> Iterator[trace.Span]:
    with _tracer.start_as_current_span(f"invoke_agent {agent_name}") as span:
        span.set_attribute("gen_ai.operation.name", "invoke_agent")
        span.set_attribute("gen_ai.agent.name", agent_name)
        for key, value in attrs.items():
            span.set_attribute(key, value)
        yield span


@contextmanager
def chat_span(model: str, provider: str, **attrs: Any) -> Iterator[trace.Span]:
    with _tracer.start_as_current_span(f"chat {model}") as span:
        span.set_attribute("gen_ai.operation.name", "chat")
        span.set_attribute("gen_ai.request.model", model)
        span.set_attribute("gen_ai.provider.name", provider)
        for key, value in attrs.items():
            span.set_attribute(key, value)
        yield span


@contextmanager
def execute_tool_span(tool_name: str, **attrs: Any) -> Iterator[trace.Span]:
    with _tracer.start_as_current_span(f"execute_tool {tool_name}") as span:
        span.set_attribute("gen_ai.operation.name", "execute_tool")
        span.set_attribute("gen_ai.tool.name", tool_name)
        for key, value in attrs.items():
            span.set_attribute(key, value)
        yield span
