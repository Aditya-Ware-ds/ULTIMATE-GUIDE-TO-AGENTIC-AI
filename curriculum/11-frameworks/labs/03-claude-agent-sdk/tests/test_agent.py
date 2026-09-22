import pytest

pytest.importorskip("claude_agent_sdk")


def test_evaluate_basic_arithmetic(agent_module):
    assert agent_module._evaluate("2 + 2") == 4
    assert agent_module._evaluate("15 * 7 + 3") == 108


def test_evaluate_rejects_non_arithmetic(agent_module):
    with pytest.raises(ValueError):
        agent_module._evaluate("__import__('os')")


def test_build_options_constructs_without_error(agent_module):
    options = agent_module.build_options()

    assert options.model == "claude-haiku-4-5"
    assert "calculator" in options.mcp_servers
    assert "mcp__calculator__calculate" in options.allowed_tools


@pytest.mark.live
async def test_run_agent_end_to_end_with_real_model(agent_module):
    """Requires a real ANTHROPIC_API_KEY or Claude Code CLI auth. Run explicitly with:
    uv run --with "claude-agent-sdk>=0.2.0" pytest -m live \
        curriculum/11-frameworks/labs/03-claude-agent-sdk/tests
    """
    result = await agent_module.run_agent("What is 15 times 7, plus 3?")

    assert "108" in result
