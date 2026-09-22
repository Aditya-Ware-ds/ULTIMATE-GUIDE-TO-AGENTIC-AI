import json

import pytest


async def test_plan_returns_steps(patterns, client):
    client.provider.add_text(json.dumps({"steps": ["step one", "step two"]}))

    steps = await patterns.plan(client, "some task")

    assert steps == ["step one", "step two"]


async def test_plan_raises_on_empty_steps(patterns, client):
    client.provider.add_text(json.dumps({"steps": []}))

    with pytest.raises(ValueError):
        await patterns.plan(client, "some task")


async def test_execute_step_returns_text(patterns, client):
    client.provider.add_text("4")

    result = await patterns.execute_step(client, "Calculate 2 + 2")

    assert result == "4"


async def test_plan_and_execute_calls_model_once_per_step_plus_plan(patterns, client):
    client.provider.add_text(json.dumps({"steps": ["a", "b", "c"]}))
    client.provider.add_text("result a")
    client.provider.add_text("result b")
    client.provider.add_text("result c")

    result = await patterns.plan_and_execute(client, "some task")

    assert result == "result c"
    assert client.provider.call_count == 4  # 1 plan + 3 steps


async def test_generate_draft_includes_feedback_when_given(patterns, client):
    client.provider.add_text("revised draft")

    await patterns.generate_draft(client, "task", feedback="be more specific")

    sent_content = client.provider.calls[0]["messages"][0].content
    assert "be more specific" in sent_content


async def test_evaluate_draft_parses_structured_response(patterns, client):
    client.provider.add_text(json.dumps({"approved": True, "feedback": "looks good"}))

    approved, feedback = await patterns.evaluate_draft(client, "task", "some draft")

    assert approved is True
    assert feedback == "looks good"


async def test_evaluator_optimizer_stops_as_soon_as_approved(patterns, client):
    client.provider.add_text("draft 1")
    client.provider.add_text(json.dumps({"approved": True, "feedback": "great"}))

    result = await patterns.evaluator_optimizer(client, "task", max_iterations=5)

    assert result == "draft 1"
    assert client.provider.call_count == 2  # did not use all 5 iterations


async def test_evaluator_optimizer_revises_until_approved(patterns, client):
    client.provider.add_text("draft 1")
    client.provider.add_text(json.dumps({"approved": False, "feedback": "too vague"}))
    client.provider.add_text("draft 2")
    client.provider.add_text(json.dumps({"approved": True, "feedback": "good"}))

    result = await patterns.evaluator_optimizer(client, "task", max_iterations=5)

    assert result == "draft 2"
    assert client.provider.call_count == 4


async def test_evaluator_optimizer_returns_last_draft_if_never_approved(patterns, client):
    for i in range(3):
        client.provider.add_text(f"draft {i}")
        client.provider.add_text(json.dumps({"approved": False, "feedback": "still not right"}))

    result = await patterns.evaluator_optimizer(client, "task", max_iterations=3)

    assert result == "draft 2"  # the last attempt, not an exception
    assert client.provider.call_count == 6
