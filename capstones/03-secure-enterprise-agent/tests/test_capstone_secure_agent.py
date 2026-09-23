from mcp import Client

from shared.llm.types import Message, Role, ToolCall


async def test_dispatch_returns_the_looked_up_record(secure_agent, mcp_server_module):
    async with Client(mcp_server_module.mcp) as mcp_client:
        result = await secure_agent.dispatch(
            mcp_client, ToolCall(id="1", name="lookup_record", arguments={"record_id": "emp-001"})
        )

    assert not result.is_error
    assert "Alice Smith" in result.content


async def test_dispatch_surfaces_the_real_error_message_for_an_unknown_record(
    secure_agent, mcp_server_module
):
    async with Client(mcp_server_module.mcp) as mcp_client:
        result = await secure_agent.dispatch(
            mcp_client, ToolCall(id="1", name="lookup_record", arguments={"record_id": "nope"})
        )

    assert result.is_error
    assert "No record found for id" in result.content


async def test_run_agent_with_approval_pauses_before_sending_an_announcement(
    secure_agent, mcp_server_module, client, checkpoint_path
):
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Sending.",
            tool_calls=[
                ToolCall(
                    id="1",
                    name="send_announcement",
                    arguments={"channel": "general", "message": "Hello team"},
                )
            ],
        )
    )

    async with Client(mcp_server_module.mcp) as mcp_client:
        result = await secure_agent.run_agent_with_approval(
            client, mcp_client, checkpoint_path, "Announce hello to general."
        )

    assert result.status == "paused"
    assert result.pending_tool_call.name == "send_announcement"
    assert checkpoint_path.exists()
    assert mcp_server_module._SENT_ANNOUNCEMENTS == []  # never dispatched before approval


async def test_resume_after_approval_true_actually_sends_the_announcement(
    secure_agent, mcp_server_module, client, checkpoint_path
):
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Sending.",
            tool_calls=[
                ToolCall(
                    id="1",
                    name="send_announcement",
                    arguments={"channel": "general", "message": "Hello team"},
                )
            ],
        )
    )
    client.provider.add_text("Sent.")

    async with Client(mcp_server_module.mcp) as mcp_client:
        await secure_agent.run_agent_with_approval(
            client, mcp_client, checkpoint_path, "Announce hello to general."
        )
        result = await secure_agent.resume_after_approval(
            client, mcp_client, checkpoint_path, approved=True
        )

    assert result.status == "done"
    assert mcp_server_module._SENT_ANNOUNCEMENTS == [
        {"channel": "general", "message": "Hello team"}
    ]
    assert not checkpoint_path.exists()


async def test_resume_after_approval_false_never_sends_the_announcement(
    secure_agent, mcp_server_module, client, checkpoint_path
):
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Sending.",
            tool_calls=[
                ToolCall(
                    id="1",
                    name="send_announcement",
                    arguments={"channel": "general", "message": "Hello team"},
                )
            ],
        )
    )
    client.provider.add_text("Understood, not sending.")

    async with Client(mcp_server_module.mcp) as mcp_client:
        await secure_agent.run_agent_with_approval(
            client, mcp_client, checkpoint_path, "Announce hello to general."
        )
        result = await secure_agent.resume_after_approval(
            client, mcp_client, checkpoint_path, approved=False
        )

    assert result.status == "done"
    assert mcp_server_module._SENT_ANNOUNCEMENTS == []


async def test_redteam_approved_but_non_allowlisted_channel_is_still_blocked(
    secure_agent, mcp_server_module, client, checkpoint_path
):
    """Core red-team scenario: even if a human approves the request (maybe
    without noticing the suspicious channel), the tool's own allowlist
    must still block it -- defense in depth, not reliant on human review
    alone (Module 18 lesson 02).
    """
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Sending.",
            tool_calls=[
                ToolCall(
                    id="1",
                    name="send_announcement",
                    arguments={"channel": "external-leak-channel", "message": "confidential data"},
                )
            ],
        )
    )
    client.provider.add_text("That could not be sent.")

    async with Client(mcp_server_module.mcp) as mcp_client:
        await secure_agent.run_agent_with_approval(
            client, mcp_client, checkpoint_path, "Announce to external-leak-channel."
        )
        result = await secure_agent.resume_after_approval(
            client, mcp_client, checkpoint_path, approved=True
        )

    assert result.status == "done"
    assert mcp_server_module._SENT_ANNOUNCEMENTS == []


async def test_kill_and_resume_reloads_the_checkpoint_from_a_fresh_process(
    secure_agent, mcp_server_module, client, checkpoint_path, capstone_dir
):
    """Simulates a real process restart: the pause happens in one process
    (this test's first `async with` block), and resume happens against a
    freshly loaded agent module and a freshly started MCP server/client --
    proving the checkpoint file on disk, not in-memory state, is what
    carries everything needed to resume (Module 07's discipline, applied
    here at the approval-gate boundary).
    """
    from shared.testing import load_lab_module

    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Sending.",
            tool_calls=[
                ToolCall(
                    id="1",
                    name="send_announcement",
                    arguments={"channel": "engineering", "message": "Deploy complete"},
                )
            ],
        )
    )

    async with Client(mcp_server_module.mcp) as mcp_client:
        paused = await secure_agent.run_agent_with_approval(
            client, mcp_client, checkpoint_path, "Announce the deploy to engineering."
        )
    assert paused.status == "paused"
    assert checkpoint_path.exists()

    # "Restart": fresh module instances, fresh MCP server, fresh client --
    # only the checkpoint file on disk is shared with the paused run above.
    fresh_agent = load_lab_module(capstone_dir, "secure_agent")
    fresh_mcp_module = load_lab_module(capstone_dir, "mcp_server")
    client.provider.add_text("Done.")

    async with Client(fresh_mcp_module.mcp) as fresh_mcp_client:
        resumed = await fresh_agent.resume_after_approval(
            client, fresh_mcp_client, checkpoint_path, approved=True
        )

    assert resumed.status == "done"
    assert fresh_mcp_module._SENT_ANNOUNCEMENTS == [
        {"channel": "engineering", "message": "Deploy complete"}
    ]
    assert not checkpoint_path.exists()
