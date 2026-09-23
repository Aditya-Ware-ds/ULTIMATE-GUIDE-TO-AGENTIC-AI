async def test_evaluate_citation_accuracy_averages_over_succeeded_topics(eval_suite):
    async def fake_pipeline(client, topic):
        return {"status": "success", "citation_accuracy": client}  # client stands in for a score

    scores = iter([1.0, 0.5])

    def client_factory():
        return next(scores)

    result = await eval_suite.evaluate_citation_accuracy(
        fake_pipeline, client_factory, topics=["topic a", "topic b"]
    )

    assert result["total"] == 2
    assert result["succeeded"] == 2
    assert result["mean_citation_accuracy"] == 0.75
    assert [r["topic"] for r in result["results"]] == ["topic a", "topic b"]


async def test_evaluate_citation_accuracy_excludes_escalated_topics_from_the_mean(eval_suite):
    async def fake_pipeline(client, topic):
        if topic == "bad topic":
            return {"status": "escalated", "reason": "no sources"}
        return {"status": "success", "citation_accuracy": 1.0}

    def client_factory():
        return object()

    result = await eval_suite.evaluate_citation_accuracy(
        fake_pipeline, client_factory, topics=["good topic", "bad topic"]
    )

    assert result["total"] == 2
    assert result["succeeded"] == 1
    assert result["mean_citation_accuracy"] == 1.0


async def test_evaluate_citation_accuracy_handles_all_escalated(eval_suite):
    async def fake_pipeline(client, topic):
        return {"status": "escalated", "reason": "no sources"}

    result = await eval_suite.evaluate_citation_accuracy(
        fake_pipeline, lambda: object(), topics=["a"]
    )

    assert result["succeeded"] == 0
    assert result["mean_citation_accuracy"] == 0.0


async def test_evaluate_citation_accuracy_uses_default_topics_when_none_given(
    eval_suite, research_pipeline, client
):
    import json

    for _ in eval_suite.DEFAULT_TOPICS:
        client.provider.add_text(json.dumps({"status": "success", "facts": ["Fact A"]}))
        client.provider.add_text("Fact A matters [1].")
        client.provider.add_text(json.dumps({"approved": True, "feedback": "Good."}))

    result = await eval_suite.evaluate_citation_accuracy(
        research_pipeline.run_traced_pipeline, lambda: client
    )

    assert result["total"] == len(eval_suite.DEFAULT_TOPICS)
    assert result["succeeded"] == len(eval_suite.DEFAULT_TOPICS)
    assert result["mean_citation_accuracy"] == 1.0
