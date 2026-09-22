from shared.llm.types import Message, Role, ToolDefinition


def make_messages(n_user_messages: int, filler: str = "word " * 20) -> list[Message]:
    messages = [Message(role=Role.SYSTEM, content="Be concise.")]
    for i in range(n_user_messages):
        messages.append(Message(role=Role.USER, content=f"turn {i}: {filler}"))
    return messages


def test_compact_messages_noop_when_under_budget(compacting_agent):
    messages = make_messages(3)

    result = compacting_agent.compact_messages(messages, max_tokens=10_000)

    assert result == messages


def test_compact_messages_keeps_system_message(compacting_agent):
    messages = make_messages(20)

    result = compacting_agent.compact_messages(messages, max_tokens=50, keep_recent=4)

    assert result[0].role == Role.SYSTEM


def test_compact_messages_keeps_recent_messages(compacting_agent):
    messages = make_messages(20)

    result = compacting_agent.compact_messages(messages, max_tokens=50, keep_recent=4)

    non_system = [m for m in result if m.role != Role.SYSTEM]
    assert non_system[-1].content == messages[-1].content
    assert non_system[-2].content == messages[-2].content


def test_compact_messages_reduces_token_count(compacting_agent):
    messages = make_messages(20)
    before = compacting_agent.count_tokens(messages)

    result = compacting_agent.compact_messages(messages, max_tokens=50, keep_recent=4)
    after = compacting_agent.count_tokens(result)

    assert after < before


def test_compact_messages_noop_when_nothing_old_enough(compacting_agent):
    messages = make_messages(2)

    result = compacting_agent.compact_messages(messages, max_tokens=1, keep_recent=4)

    assert result == messages


NOOP_TOOL = ToolDefinition(
    name="noop",
    description="Does nothing, used to simulate a long-running agent for testing.",
    parameters={"type": "object", "properties": {}},
)


def noop() -> str:
    return "ok " * 15


TOOLS = [NOOP_TOOL]
REGISTRY = {"noop": noop}


async def test_run_agent_with_compaction_completes_long_run(compacting_agent, client):
    for _ in range(18):
        client.provider.add_tool_call("noop", {})
    client.provider.add_text("Done after a long run.")

    result = await compacting_agent.run_agent_with_compaction(
        client,
        system_prompt="Be concise.",
        user_input="Run the noop tool many times.",
        tools=TOOLS,
        registry=REGISTRY,
        max_context_tokens=150,
        max_steps=25,
    )

    assert result == "Done after a long run."


async def test_run_agent_with_compaction_keeps_final_call_within_budget(compacting_agent, client):
    for _ in range(18):
        client.provider.add_tool_call("noop", {})
    client.provider.add_text("Done after a long run.")
    max_context_tokens = 150

    await compacting_agent.run_agent_with_compaction(
        client,
        system_prompt="Be concise.",
        user_input="Run the noop tool many times.",
        tools=TOOLS,
        registry=REGISTRY,
        max_context_tokens=max_context_tokens,
        max_steps=25,
    )

    final_call_messages = client.provider.calls[-1]["messages"]
    assert compacting_agent.count_tokens(final_call_messages) <= max_context_tokens


async def test_run_agent_with_compaction_stops_at_max_steps(compacting_agent, client):
    for _ in range(30):
        client.provider.add_tool_call("noop", {})

    result = await compacting_agent.run_agent_with_compaction(
        client,
        system_prompt="Be concise.",
        user_input="Never stop.",
        tools=TOOLS,
        registry=REGISTRY,
        max_context_tokens=150,
        max_steps=5,
    )

    assert client.provider.call_count == 5
    assert "5" in result or "stopped" in result.lower()
