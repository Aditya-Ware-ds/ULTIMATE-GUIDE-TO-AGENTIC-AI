import pytest

from shared.llm.types import Message, Role, ToolCall

FIXED_CONTENT = (
    "def total_price(unit_price: float, quantity: int) -> float:\n"
    "    return unit_price * quantity\n"
)


def test_resolve_within_repo_rejects_path_traversal(coding_agent, repo_copy):
    with pytest.raises(ValueError):
        coding_agent.resolve_within_repo(repo_copy, "../../etc/passwd")


def test_resolve_within_repo_allows_a_file_inside(coding_agent, repo_copy):
    resolved = coding_agent.resolve_within_repo(repo_copy, "inventory.py")

    assert resolved == (repo_copy / "inventory.py").resolve()


def test_read_file_returns_contents(coding_agent, repo_copy):
    content = coding_agent.read_file(repo_copy, "inventory.py")

    assert "total_price" in content


def test_write_file_then_read_file_round_trips(coding_agent, repo_copy):
    coding_agent.write_file(repo_copy, "inventory.py", FIXED_CONTENT)

    assert coding_agent.read_file(repo_copy, "inventory.py") == FIXED_CONTENT


def test_run_tests_fails_on_the_buggy_sample_repo(coding_agent, repo_copy):
    result = coding_agent.run_tests(repo_copy)

    assert not result.success


def test_run_tests_passes_after_a_manual_fix(coding_agent, repo_copy):
    coding_agent.write_file(repo_copy, "inventory.py", FIXED_CONTENT)

    result = coding_agent.run_tests(repo_copy)

    assert result.success


def test_dispatch_never_raises_on_unknown_tool(coding_agent, repo_copy):
    registry = coding_agent.build_tool_registry(repo_copy)
    call = ToolCall(id="1", name="not_a_tool", arguments={})

    result = coding_agent.dispatch(call, registry)

    assert result.is_error


async def test_run_coding_agent_fixes_the_bug_and_reports_success(coding_agent, client, repo_copy):
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Let me look at the failing code.",
            tool_calls=[
                ToolCall(id="1", name="read_file", arguments={"relative_path": "inventory.py"})
            ],
        )
    )
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Found it -- removing the stray -1.",
            tool_calls=[
                ToolCall(
                    id="2",
                    name="write_file",
                    arguments={"relative_path": "inventory.py", "content": FIXED_CONTENT},
                )
            ],
        )
    )
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Verifying.",
            tool_calls=[ToolCall(id="3", name="run_tests", arguments={})],
        )
    )
    client.provider.add_text("The tests pass now.")

    result = await coding_agent.run_coding_agent(client, repo_copy, "Fix the failing test.")

    assert result["status"] == "success"
    assert result["steps"] == 4
    assert coding_agent.read_file(repo_copy, "inventory.py") == FIXED_CONTENT


async def test_run_coding_agent_does_not_trust_a_false_claim_of_success(
    coding_agent, client, repo_copy
):
    # The model claims it's done without ever calling write_file -- the bug
    # is never actually fixed. run_coding_agent must not take its word for it.
    client.provider.add_text("I've fixed the bug, the tests pass now.")

    result = await coding_agent.run_coding_agent(client, repo_copy, "Fix the failing test.")

    assert result["status"] == "failed"


async def test_run_coding_agent_stops_at_max_steps_and_still_reports_failed(
    coding_agent, client, repo_copy
):
    for _ in range(10):
        client.provider.add_response(
            Message(
                role=Role.ASSISTANT,
                content="Still investigating.",
                tool_calls=[
                    ToolCall(id="x", name="read_file", arguments={"relative_path": "inventory.py"})
                ],
            )
        )

    result = await coding_agent.run_coding_agent(
        client, repo_copy, "Fix the failing test.", max_steps=3
    )

    assert result["status"] == "failed"
    assert result["steps"] == 3
    assert client.provider.call_count == 3
