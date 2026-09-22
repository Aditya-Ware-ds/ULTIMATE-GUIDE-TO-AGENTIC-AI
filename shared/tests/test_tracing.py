from shared.tracing import (
    chat_span,
    clear_exported_spans,
    execute_tool_span,
    get_exported_spans,
    invoke_agent_span,
)


def setup_function() -> None:
    clear_exported_spans()


def test_invoke_agent_span_records_expected_attributes():
    with invoke_agent_span("research-agent"):
        pass

    spans = get_exported_spans()
    assert len(spans) == 1
    assert spans[0].name == "invoke_agent research-agent"
    assert spans[0].attributes["gen_ai.operation.name"] == "invoke_agent"
    assert spans[0].attributes["gen_ai.agent.name"] == "research-agent"


def test_chat_span_nested_inside_invoke_agent_span():
    with (
        invoke_agent_span("research-agent"),
        chat_span(model="claude-haiku-4-5", provider="anthropic"),
    ):
        pass

    spans = get_exported_spans()
    names = {s.name for s in spans}
    assert "invoke_agent research-agent" in names
    assert "chat claude-haiku-4-5" in names

    chat = next(s for s in spans if s.name == "chat claude-haiku-4-5")
    agent = next(s for s in spans if s.name == "invoke_agent research-agent")
    assert chat.parent.span_id == agent.context.span_id


def test_execute_tool_span_records_tool_name():
    with execute_tool_span("get_weather"):
        pass

    spans = get_exported_spans()
    assert spans[0].attributes["gen_ai.tool.name"] == "get_weather"


def test_extra_attributes_are_recorded():
    with invoke_agent_span("agent", **{"gen_ai.request.max_tokens": 512}):
        pass

    spans = get_exported_spans()
    assert spans[0].attributes["gen_ai.request.max_tokens"] == 512
