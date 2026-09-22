from shared.llm.types import Message, Role, ToolCall, ToolDefinition, ToolResult

NOOP_TOOL = ToolDefinition(
    name="noop",
    description="Does nothing, used for testing.",
    parameters={"type": "object", "properties": {}},
)


def noop() -> str:
    return "ok"


TOOLS = [NOOP_TOOL]
REGISTRY = {"noop": noop}


def test_message_round_trip_plain_text(resumable_agent):
    message = Message(role=Role.USER, content="hello")

    restored = resumable_agent.message_from_dict(resumable_agent.message_to_dict(message))

    assert restored == message


def test_message_round_trip_with_tool_call(resumable_agent):
    message = Message(
        role=Role.ASSISTANT,
        tool_calls=[ToolCall(id="1", name="noop", arguments={"x": 1})],
    )

    restored = resumable_agent.message_from_dict(resumable_agent.message_to_dict(message))

    assert restored == message


def test_message_round_trip_with_tool_result(resumable_agent):
    message = Message(role=Role.TOOL, tool_result=ToolResult(tool_call_id="1", content="ok"))

    restored = resumable_agent.message_from_dict(resumable_agent.message_to_dict(message))

    assert restored == message


def test_save_and_load_checkpoint(resumable_agent, tmp_path):
    path = tmp_path / "checkpoint.json"
    messages = resumable_agent.build_initial_messages("Be concise.", "hi")

    resumable_agent.save_checkpoint(path, messages, step=2)
    loaded_messages, loaded_step = resumable_agent.load_checkpoint(path)

    assert loaded_messages == messages
    assert loaded_step == 2


def test_load_checkpoint_missing_file_returns_none(resumable_agent, tmp_path):
    assert resumable_agent.load_checkpoint(tmp_path / "does_not_exist.json") is None


def test_dispatch_never_raises_on_unknown_tool(resumable_agent):
    call = ToolCall(id="1", name="not_a_tool", arguments={})

    result = resumable_agent.dispatch(call, REGISTRY)

    assert result.is_error


async def test_run_one_step_tool_call_returns_none_answer(resumable_agent, client):
    client.provider.add_tool_call("noop", {})
    messages = resumable_agent.build_initial_messages("Be concise.", "go")

    updated_messages, answer = await resumable_agent.run_one_step(client, messages, TOOLS, REGISTRY)

    assert answer is None
    assert len(updated_messages) > len(messages)


async def test_run_one_step_final_text_returns_answer(resumable_agent, client):
    client.provider.add_text("done")
    messages = resumable_agent.build_initial_messages("Be concise.", "go")

    _, answer = await resumable_agent.run_one_step(client, messages, TOOLS, REGISTRY)

    assert answer == "done"


async def test_run_resumable_agent_fresh_start_completes(resumable_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    client.provider.add_tool_call("noop", {})
    client.provider.add_text("done")

    result = await resumable_agent.run_resumable_agent(
        client, TOOLS, REGISTRY, checkpoint_path, "Be concise.", "go"
    )

    assert result == "done"
    assert not checkpoint_path.exists()


async def test_run_resumable_agent_leaves_checkpoint_at_max_steps(
    resumable_agent, client, tmp_path
):
    checkpoint_path = tmp_path / "checkpoint.json"
    for _ in range(10):
        client.provider.add_tool_call("noop", {})

    result = await resumable_agent.run_resumable_agent(
        client, TOOLS, REGISTRY, checkpoint_path, "Be concise.", "go", max_steps=3
    )

    assert "3" in result or "stopped" in result.lower()
    assert checkpoint_path.exists()


async def test_kill_and_resume_does_not_repeat_completed_steps(resumable_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    client.provider.add_tool_call("noop", {})  # step 1 (before "crash")
    client.provider.add_tool_call("noop", {})  # step 2 (after resume)
    client.provider.add_text("done")  # step 3 (after resume)

    # Simulate a crash after the first step: run one step manually and
    # checkpoint that partial state, rather than calling run_resumable_agent
    # (which would run to completion in one go).
    initial_messages = resumable_agent.build_initial_messages("Be concise.", "go")
    messages_after_step_1, answer = await resumable_agent.run_one_step(
        client, initial_messages, TOOLS, REGISTRY
    )
    assert answer is None
    resumable_agent.save_checkpoint(checkpoint_path, messages_after_step_1, step=1)
    assert client.provider.call_count == 1

    # "Restart": a fresh call to run_resumable_agent should resume from the
    # checkpoint and only need 2 more model calls, not repeat step 1's call.
    result = await resumable_agent.run_resumable_agent(
        client, TOOLS, REGISTRY, checkpoint_path, "Be concise.", "go", max_steps=10
    )

    assert result == "done"
    assert client.provider.call_count == 3
    assert not checkpoint_path.exists()
