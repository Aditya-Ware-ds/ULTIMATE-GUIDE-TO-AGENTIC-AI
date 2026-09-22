from shared.tracing import get_exported_spans


async def test_run_traced_agent_natural_completion_produces_invoke_agent_and_chat_spans(
    traced_agent, client
):
    client.provider.add_text("I already know the answer: 4.")

    result = await traced_agent.run_traced_agent(client, "What is 2+2 without using a tool?")

    assert result == "I already know the answer: 4."
    spans = get_exported_spans()
    names = [s.name for s in spans]
    assert "invoke_agent react-agent" in names
    assert any(name.startswith("chat ") for name in names)


async def test_run_traced_agent_records_token_usage_on_chat_span(traced_agent, client):
    client.provider.add_text("42")

    await traced_agent.run_traced_agent(client, "What is 6*7?")

    chat = next(s for s in get_exported_spans() if s.name.startswith("chat "))
    assert chat.attributes["gen_ai.usage.input_tokens"] >= 0
    assert "gen_ai.usage.output_tokens" in chat.attributes


async def test_run_traced_agent_tool_call_produces_nested_execute_tool_span(traced_agent, client):
    client.provider.add_tool_call("calculate", {"expression": "6 * 7"})
    client.provider.add_text("The answer is 42.")

    result = await traced_agent.run_traced_agent(client, "What is 6*7?")

    assert result == "The answer is 42."
    spans = get_exported_spans()
    tool_span = next(s for s in spans if s.name == "execute_tool calculate")
    agent_span = next(s for s in spans if s.name == "invoke_agent react-agent")

    # The tool span's ancestor chain reaches the invoke_agent span (nested
    # under a chat span in between, matching the loop's structure).
    spans_by_id = {s.context.span_id: s for s in spans}
    ancestor = tool_span
    found_agent_ancestor = False
    while ancestor.parent is not None:
        ancestor = spans_by_id[ancestor.parent.span_id]
        if ancestor.context.span_id == agent_span.context.span_id:
            found_agent_ancestor = True
            break
    assert found_agent_ancestor


def test_replay_trace_orders_spans_and_indents_children(traced_agent):
    from shared.tracing import chat_span, invoke_agent_span

    with invoke_agent_span("demo"), chat_span(model="mock-model", provider="mock"):
        pass

    output = traced_agent.replay_trace(get_exported_spans())
    lines = output.splitlines()

    assert lines[0].startswith("invoke_agent demo")
    assert lines[1].startswith("  chat mock-model")


def test_summarize_usage_sums_token_counts_across_chat_spans(traced_agent):
    from shared.tracing import chat_span

    with chat_span(model="m", provider="mock") as span:
        span.set_attribute("gen_ai.usage.input_tokens", 10)
        span.set_attribute("gen_ai.usage.output_tokens", 5)
    with chat_span(model="m", provider="mock") as span:
        span.set_attribute("gen_ai.usage.input_tokens", 20)
        span.set_attribute("gen_ai.usage.output_tokens", 8)

    summary = traced_agent.summarize_usage(get_exported_spans())

    assert summary == {"chat_calls": 2, "input_tokens": 30, "output_tokens": 13}
