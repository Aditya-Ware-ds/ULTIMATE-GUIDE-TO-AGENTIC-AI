import pytest


async def test_route_to_worker_returns_scripted_choice(agents, client):
    client.provider.add_text("writer")

    choice = await agents.route_to_worker(
        client, "write a tagline", ["researcher", "writer", "critic"]
    )

    assert choice == "writer"


async def test_route_to_worker_rejects_unknown_choice(agents, client):
    client.provider.add_text("editor")  # not in the allowed list

    with pytest.raises(ValueError):
        await agents.route_to_worker(client, "some task", ["researcher", "writer", "critic"])


async def test_synthesize_sends_task_and_worker_output(agents, client):
    client.provider.add_text("Here is your final answer.")

    result = await agents.synthesize(client, "some task", "raw worker output")

    assert result == "Here is your final answer."
    sent_content = client.provider.calls[0]["messages"][0].content
    assert "some task" in sent_content
    assert "raw worker output" in sent_content


async def test_supervisor_routes_and_synthesizes_on_success(agents, client):
    client.provider.add_text("researcher")
    client.provider.add_text("Jupiter has 95 known moons.")

    workers = {"researcher": agents.researcher, "writer": agents.writer, "critic": agents.critic}
    result = await agents.supervisor(client, "how many moons does Jupiter have?", workers)

    assert result == {
        "status": "success",
        "worker": "researcher",
        "output": "Jupiter has 95 known moons.",
    }
    assert client.provider.call_count == 2  # one route call, one synthesis call


async def test_supervisor_escalates_without_synthesizing_on_worker_failure(agents, client):
    client.provider.add_text("researcher")
    # No second scripted response: if supervisor wrongly calls synthesize,
    # the mock provider raises AssertionError for running out of script.

    workers = {"researcher": agents.researcher, "writer": agents.writer, "critic": agents.critic}
    result = await agents.supervisor(client, "an unanswerable claim", workers)

    assert result["status"] == "escalated"
    assert result["worker"] == "researcher"
    assert "No reliable source" in result["reason"]
    assert client.provider.call_count == 1  # routing only, no synthesis call


async def test_supervisor_dispatches_to_writer_and_critic_too(agents, client):
    client.provider.add_text("writer")
    client.provider.add_text("A tagline about fresh coffee.")

    workers = {"researcher": agents.researcher, "writer": agents.writer, "critic": agents.critic}
    result = await agents.supervisor(client, "write a tagline for a coffee shop", workers)

    assert result["worker"] == "writer"
    assert result["status"] == "success"
