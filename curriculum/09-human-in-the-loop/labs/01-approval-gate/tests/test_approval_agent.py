async def test_non_gated_tool_call_dispatches_immediately(approval_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    client.provider.add_tool_call("get_weather", {"city": "Paris"})
    client.provider.add_text("It's sunny in Paris.")

    result = await approval_agent.run_agent_with_approval(
        client, checkpoint_path, "Be concise.", "What's the weather in Paris?"
    )

    assert result.status == "done"
    assert result.text == "It's sunny in Paris."
    assert not checkpoint_path.exists()


async def test_gated_tool_call_pauses_without_dispatching(approval_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    client.provider.add_tool_call("send_email", {"to": "jane@example.com", "subject": "Hi"})

    result = await approval_agent.run_agent_with_approval(
        client, checkpoint_path, "Be concise.", "Email Jane."
    )

    assert result.status == "paused"
    assert result.pending_tool_call.name == "send_email"
    assert approval_agent._SENT_EMAILS == []  # never dispatched
    assert checkpoint_path.exists()


async def test_resume_with_approval_dispatches_and_continues(approval_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    client.provider.add_tool_call("send_email", {"to": "jane@example.com", "subject": "Hi"})
    client.provider.add_text("The email has been sent.")

    paused = await approval_agent.run_agent_with_approval(
        client, checkpoint_path, "Be concise.", "Email Jane."
    )
    assert paused.status == "paused"

    result = await approval_agent.resume_after_approval(client, checkpoint_path, approved=True)

    assert result.status == "done"
    assert result.text == "The email has been sent."
    assert approval_agent._SENT_EMAILS == [{"to": "jane@example.com", "subject": "Hi"}]
    assert not checkpoint_path.exists()


async def test_resume_with_rejection_does_not_dispatch(approval_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    client.provider.add_tool_call("send_email", {"to": "jane@example.com", "subject": "Hi"})
    client.provider.add_text("Understood, I will not send that email.")

    paused = await approval_agent.run_agent_with_approval(
        client, checkpoint_path, "Be concise.", "Email Jane."
    )
    assert paused.status == "paused"

    result = await approval_agent.resume_after_approval(client, checkpoint_path, approved=False)

    assert result.status == "done"
    assert result.text == "Understood, I will not send that email."
    assert approval_agent._SENT_EMAILS == []  # never dispatched
    assert not checkpoint_path.exists()


async def test_rejection_is_seen_by_model_as_tool_result(approval_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    client.provider.add_tool_call("send_email", {"to": "jane@example.com", "subject": "Hi"})
    client.provider.add_text("ok")

    await approval_agent.run_agent_with_approval(
        client, checkpoint_path, "Be concise.", "Email Jane."
    )
    await approval_agent.resume_after_approval(client, checkpoint_path, approved=False)

    second_call_messages = client.provider.calls[1]["messages"]
    tool_messages = [m for m in second_call_messages if m.tool_result is not None]
    assert any(m.tool_result.is_error for m in tool_messages)


async def test_run_agent_with_approval_stops_at_max_steps(approval_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    for _ in range(10):
        client.provider.add_tool_call("get_weather", {"city": "Paris"})

    result = await approval_agent.run_agent_with_approval(
        client, checkpoint_path, "Be concise.", "Keep checking weather forever.", max_steps=3
    )

    assert result.status == "stopped"
    assert checkpoint_path.exists()
