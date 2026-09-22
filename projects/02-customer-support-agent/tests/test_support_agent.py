import pytest


def test_search_faq_finds_relevant_entry(support_agent):
    result = support_agent.search_faq("How long does shipping take?")

    assert "shipping" in result.lower() or "business days" in result.lower()


def test_search_faq_raises_on_unrelated_query(support_agent):
    with pytest.raises(ValueError):
        support_agent.search_faq("xyzzy plugh completely unrelated nonsense")


def test_issue_refund_appends_to_tracking_list(support_agent):
    support_agent._ISSUED_REFUNDS.clear()

    support_agent.issue_refund("ORDER123", 49.99)

    assert support_agent._ISSUED_REFUNDS == [{"order_id": "ORDER123", "amount": 49.99}]


async def test_gated_refund_pauses_without_issuing(support_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    client.provider.add_tool_call("issue_refund", {"order_id": "ORDER123", "amount": 49.99})

    result = await support_agent.run_support_agent(
        client, checkpoint_path, "Please refund order ORDER123."
    )

    assert result.status == "paused"
    assert support_agent._ISSUED_REFUNDS == []
    assert checkpoint_path.exists()


async def test_resume_approved_issues_refund(support_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    client.provider.add_tool_call("issue_refund", {"order_id": "ORDER123", "amount": 49.99})
    client.provider.add_text("Your refund has been processed.")

    await support_agent.run_support_agent(client, checkpoint_path, "Please refund order ORDER123.")
    result = await support_agent.resume_after_approval(client, checkpoint_path, approved=True)

    assert result.status == "done"
    assert support_agent._ISSUED_REFUNDS == [{"order_id": "ORDER123", "amount": 49.99}]
    assert not checkpoint_path.exists()


async def test_resume_rejected_does_not_issue_refund(support_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    client.provider.add_tool_call("issue_refund", {"order_id": "ORDER123", "amount": 49.99})
    client.provider.add_text("I will not process that refund.")

    await support_agent.run_support_agent(client, checkpoint_path, "Please refund order ORDER123.")
    result = await support_agent.resume_after_approval(client, checkpoint_path, approved=False)

    assert result.status == "done"
    assert support_agent._ISSUED_REFUNDS == []


async def test_faq_lookup_does_not_pause(support_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    client.provider.add_tool_call("search_faq", {"query": "shipping time"})
    client.provider.add_text("Shipping takes 3-5 business days.")

    result = await support_agent.run_support_agent(
        client, checkpoint_path, "How long does shipping take?"
    )

    assert result.status == "done"
    assert result.text == "Shipping takes 3-5 business days."


async def test_escalates_with_summary_at_max_steps(support_agent, client, tmp_path):
    checkpoint_path = tmp_path / "checkpoint.json"
    for _ in range(10):
        client.provider.add_tool_call("search_faq", {"query": "an unresolvable question"})

    result = await support_agent.run_support_agent(
        client, checkpoint_path, "A very confusing request.", max_steps=3
    )

    assert result.status == "escalated"
    assert "search_faq" in result.text
    assert "step limit" in result.text.lower()
