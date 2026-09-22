from shared.llm.types import Message, Role, ToolCall


def test_search_known_query(agent):
    assert agent.search("capital of France") == "Paris"
    assert agent.search("CAPITAL OF FRANCE") == "Paris"  # case-insensitive


def test_search_unknown_query_raises(agent):
    import pytest

    with pytest.raises(ValueError):
        agent.search("capital of Atlantis")


def test_calculate_basic(agent):
    assert agent.calculate("2 + 2") == 4
    assert agent.calculate("10 / 4") == 2.5


def test_dispatch_never_raises_on_unknown_tool(agent):
    call = ToolCall(id="1", name="not_a_tool", arguments={})

    result = agent.dispatch(call, agent.TOOL_REGISTRY)

    assert result.is_error


def test_dispatch_never_raises_on_bad_search(agent):
    call = ToolCall(id="2", name="search", arguments={"query": "nonexistent"})

    result = agent.dispatch(call, agent.TOOL_REGISTRY)

    assert result.is_error


async def test_run_react_agent_two_hop_search(agent, client):
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="First I'll find the capital of France.",
            tool_calls=[ToolCall(id="1", name="search", arguments={"query": "capital of France"})],
        )
    )
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Now I'll find its population.",
            tool_calls=[
                ToolCall(id="2", name="search", arguments={"query": "population of Paris"})
            ],
        )
    )
    client.provider.add_text("Paris has a population of 2.1 million.")

    result = await agent.run_react_agent(client, "What's the population of France's capital?")

    assert result == "Paris has a population of 2.1 million."
    assert client.provider.call_count == 3


async def test_run_react_agent_mixed_tools(agent, client):
    client.provider.add_tool_call("search", {"query": "population of Tokyo"})
    client.provider.add_tool_call("calculate", {"expression": "14 * 2"})
    client.provider.add_text("Double Tokyo's population is 28 million.")

    result = await agent.run_react_agent(client, "Double the population of Tokyo.")

    assert result == "Double Tokyo's population is 28 million."


async def test_run_react_agent_stops_at_max_steps(agent, client):
    for _ in range(10):
        client.provider.add_tool_call("search", {"query": "capital of France"})

    result = await agent.run_react_agent(client, "Keep searching forever.", max_steps=3)

    assert client.provider.call_count == 3
    assert "3" in result or "stopped" in result.lower()


async def test_run_react_agent_natural_completion_needs_no_tools(agent, client):
    client.provider.add_text("I already know the answer: 42.")

    result = await agent.run_react_agent(client, "What is the answer?")

    assert result == "I already know the answer: 42."
    assert client.provider.call_count == 1
