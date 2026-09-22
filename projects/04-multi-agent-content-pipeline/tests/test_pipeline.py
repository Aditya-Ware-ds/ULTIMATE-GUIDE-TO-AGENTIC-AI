import json


async def test_research_returns_facts_on_success(pipeline, client):
    client.provider.add_text(json.dumps({"status": "success", "facts": ["fact one", "fact two"]}))

    result = await pipeline.research(client, "the history of tea")

    assert result["status"] == "success"
    assert result["facts"] == ["fact one", "fact two"]


async def test_draft_includes_facts_and_feedback(pipeline, client):
    client.provider.add_text("A short article.")

    await pipeline.draft(client, "tea", ["fact one"], "make it shorter")

    sent = client.provider.calls[0]["messages"][0].content
    assert "fact one" in sent
    assert "make it shorter" in sent


async def test_critique_returns_approval_and_feedback(pipeline, client):
    client.provider.add_text(json.dumps({"approved": True, "feedback": "looks good"}))

    approved, feedback = await pipeline.critique(client, "tea", "draft text")

    assert approved is True
    assert feedback == "looks good"


async def test_pipeline_succeeds_on_first_draft(pipeline, client):
    client.provider.add_text(json.dumps({"status": "success", "facts": ["fact one"]}))
    client.provider.add_text("Article v1.")
    client.provider.add_text(json.dumps({"approved": True, "feedback": "great"}))

    result = await pipeline.run_pipeline(client, "tea", max_revisions=2)

    assert result == {"status": "success", "article": "Article v1.", "revisions": 0}
    assert client.provider.call_count == 3


async def test_pipeline_escalates_immediately_on_research_failure(pipeline, client):
    client.provider.add_text(json.dumps({"status": "error", "reason": "no reliable sources"}))

    result = await pipeline.run_pipeline(client, "an unresearchable topic", max_revisions=2)

    assert result == {"status": "escalated", "reason": "no reliable sources"}
    assert client.provider.call_count == 1  # research only -- no draft or critique calls


async def test_pipeline_revises_once_then_succeeds(pipeline, client):
    client.provider.add_text(json.dumps({"status": "success", "facts": ["fact one"]}))
    client.provider.add_text("Article v1.")
    client.provider.add_text(json.dumps({"approved": False, "feedback": "too short"}))
    client.provider.add_text("Article v2.")
    client.provider.add_text(json.dumps({"approved": True, "feedback": "much better"}))

    result = await pipeline.run_pipeline(client, "tea", max_revisions=2)

    assert result == {"status": "success", "article": "Article v2.", "revisions": 1}
    assert client.provider.call_count == 5


async def test_pipeline_escalates_with_last_draft_after_exhausting_revisions(pipeline, client):
    client.provider.add_text(json.dumps({"status": "success", "facts": ["fact one"]}))
    client.provider.add_text("Article v1.")
    client.provider.add_text(json.dumps({"approved": False, "feedback": "still wrong"}))
    client.provider.add_text("Article v2.")
    client.provider.add_text(json.dumps({"approved": False, "feedback": "still wrong"}))

    result = await pipeline.run_pipeline(client, "tea", max_revisions=1)

    assert result["status"] == "escalated"
    assert result["article"] == "Article v2."
    assert "still wrong" in result["reason"]
    assert client.provider.call_count == 5  # research + 2 drafts + 2 critiques
