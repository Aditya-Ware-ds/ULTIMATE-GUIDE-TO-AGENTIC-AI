"""GenAI-semantic-convention-shaped tracing, usable offline via an in-memory exporter.

from shared.tracing import invoke_agent_span, chat_span, execute_tool_span, get_exported_spans

with invoke_agent_span("research-agent"):
    with chat_span(model="claude-haiku-4-5", provider="anthropic"):
        ...
"""

from shared.tracing.tracer import (
    chat_span,
    clear_exported_spans,
    execute_tool_span,
    get_exported_spans,
    invoke_agent_span,
)

__all__ = [
    "invoke_agent_span",
    "chat_span",
    "execute_tool_span",
    "get_exported_spans",
    "clear_exported_spans",
]
