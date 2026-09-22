"""Run: uv run python curriculum/17-observability-and-debugging/examples/trace_replay_demo.py

Creates a small nested trace (an invoke_agent span containing two chat spans
and one execute_tool span) and replays it as a readable timeline. No API key
needed. See lessons/01-tracing-agent-loops.md and
lessons/02-replaying-failed-runs.md.
"""

from __future__ import annotations

import time

from shared.tracing import (
    chat_span,
    clear_exported_spans,
    execute_tool_span,
    get_exported_spans,
    invoke_agent_span,
)


def replay_trace(spans) -> str:
    spans_by_id = {s.context.span_id: s for s in spans}
    lines = []
    for span in sorted(spans, key=lambda s: s.start_time):
        depth = 0
        parent = span.parent
        while parent is not None:
            depth += 1
            parent_span = spans_by_id.get(parent.span_id)
            parent = parent_span.parent if parent_span else None
        duration_ms = (span.end_time - span.start_time) / 1_000_000
        attrs = ", ".join(f"{k}={v}" for k, v in span.attributes.items())
        lines.append(f"{'  ' * depth}{span.name} ({duration_ms:.1f}ms) [{attrs}]")
    return "\n".join(lines)


def main() -> None:
    clear_exported_spans()

    with invoke_agent_span("demo-agent", **{"gen_ai.request.max_steps": 6}):
        with chat_span(model="mock-model", provider="mock") as span:
            time.sleep(0.01)
            span.set_attribute("gen_ai.usage.input_tokens", 42)
            span.set_attribute("gen_ai.usage.output_tokens", 8)
        with execute_tool_span("search"):
            time.sleep(0.005)
        with chat_span(model="mock-model", provider="mock") as span:
            time.sleep(0.01)
            span.set_attribute("gen_ai.usage.input_tokens", 55)
            span.set_attribute("gen_ai.usage.output_tokens", 20)

    print(replay_trace(get_exported_spans()))


if __name__ == "__main__":
    main()
