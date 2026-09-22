import pytest

from shared.llm.types import Message, Role, ToolCall


def test_goto_allows_an_allowlisted_url(browser_agent, session, sample_site_index, allowed):
    result = browser_agent.goto(session, sample_site_index, allowed)

    assert session.current_url == sample_site_index
    assert "Navigated" in result


def test_goto_rejects_a_url_not_on_the_allowlist(browser_agent, session, allowed):
    with pytest.raises(ValueError):
        browser_agent.goto(session, "https://not-allowed.example.com", allowed)


def test_get_text_before_click_raises(browser_agent, session):
    with pytest.raises(ValueError):
        browser_agent.get_text(session, "#details")


def test_click_then_get_text_reveals_details(browser_agent, session):
    browser_agent.click(session, "#details-btn")

    assert "Battery life" in browser_agent.get_text(session, "#details")


def test_dispatch_never_raises_on_unknown_tool(browser_agent, session, allowed):
    registry = browser_agent.build_tool_registry(session, allowed)
    call = ToolCall(id="1", name="not_a_tool", arguments={})

    result = browser_agent.dispatch(call, registry)

    assert result.is_error


def test_dispatch_wraps_disallowed_url_as_error_result(browser_agent, session, allowed):
    registry = browser_agent.build_tool_registry(session, allowed)
    call = ToolCall(id="1", name="goto", arguments={"url": "https://not-allowed.example.com"})

    result = browser_agent.dispatch(call, registry)

    assert result.is_error


async def test_run_browser_agent_two_step_task(
    browser_agent, client, session, sample_site_index, allowed
):
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Navigating to the page.",
            tool_calls=[ToolCall(id="1", name="goto", arguments={"url": sample_site_index})],
        )
    )
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Clicking to reveal details.",
            tool_calls=[ToolCall(id="2", name="click", arguments={"selector": "#details-btn"})],
        )
    )
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Reading the details.",
            tool_calls=[ToolCall(id="3", name="get_text", arguments={"selector": "#details"})],
        )
    )
    client.provider.add_text("The battery life is 6 months.")

    result = await browser_agent.run_browser_agent(
        client, session, "What is the battery life?", allowed
    )

    assert result == "The battery life is 6 months."
    assert client.provider.call_count == 4


async def test_run_browser_agent_stops_at_max_steps(browser_agent, client, session, allowed):
    for _ in range(10):
        client.provider.add_response(
            Message(
                role=Role.ASSISTANT,
                content="Still looking.",
                tool_calls=[ToolCall(id="x", name="get_text", arguments={"selector": "#title"})],
            )
        )

    result = await browser_agent.run_browser_agent(
        client, session, "Keep looking forever.", allowed, max_steps=3
    )

    assert client.provider.call_count == 3
    assert "3" in result or "stopped" in result.lower()


@pytest.mark.live
async def test_run_browser_agent_against_a_real_playwright_browser(
    browser_agent, client, sample_site_index, allowed
):
    """Requires the `playwright` package and its browser binaries. Run with:
    uv run --with "playwright>=1.47" pytest -m live \
        curriculum/14-browser-and-computer-use-agents/labs/01-browser-task-agent/tests
    (after a one-time `uv run --with playwright playwright install chromium`)
    """
    playwright_module = pytest.importorskip("playwright.sync_api")

    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Navigating.",
            tool_calls=[ToolCall(id="1", name="goto", arguments={"url": sample_site_index})],
        )
    )
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Clicking.",
            tool_calls=[ToolCall(id="2", name="click", arguments={"selector": "#details-btn"})],
        )
    )
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Reading.",
            tool_calls=[ToolCall(id="3", name="get_text", arguments={"selector": "#details"})],
        )
    )
    client.provider.add_text("Battery life: 6 months.")

    with playwright_module.sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        real_session = browser_agent.PlaywrightBrowserSession(page)

        result = await browser_agent.run_browser_agent(
            client, real_session, "What is the battery life?", allowed
        )

        browser.close()

    assert "6 months" in result
