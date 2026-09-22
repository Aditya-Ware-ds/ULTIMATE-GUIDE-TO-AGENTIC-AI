import json


async def test_simple_agent_returns_model_text(eval_harness, client):
    client.provider.add_text("Paris")

    result = await eval_harness.simple_agent(client, "What is the capital of France?")

    assert result == "Paris"


async def test_judge_returns_structured_verdict(eval_harness, client):
    client.provider.add_text(json.dumps({"correct": True, "reasoning": "Matches the reference."}))

    verdict = await eval_harness.judge(client, "What is 2+2?", "4", "Four")

    assert verdict == {"correct": True, "reasoning": "Matches the reference."}


async def test_evaluate_dataset_computes_accuracy_and_keeps_per_item_results(eval_harness, client):
    dataset = [
        {"question": "Q1", "reference_answer": "A1"},
        {"question": "Q2", "reference_answer": "A2"},
    ]
    client.provider.add_text("A1")  # agent answer for Q1
    client.provider.add_text(json.dumps({"correct": True, "reasoning": "Correct."}))  # judge Q1
    client.provider.add_text("wrong answer")  # agent answer for Q2
    client.provider.add_text(json.dumps({"correct": False, "reasoning": "Doesn't match."}))

    async def scripted_agent(client, question):
        response = await client.complete([])
        return response.message.content

    result = await eval_harness.evaluate_dataset(client, scripted_agent, dataset)

    assert result["total"] == 2
    assert result["correct"] == 1
    assert result["accuracy"] == 0.5
    assert len(result["results"]) == 2
    assert result["results"][0]["correct"] is True
    assert result["results"][1]["correct"] is False
    assert result["results"][1]["answer"] == "wrong answer"


async def test_evaluate_dataset_perfect_score(eval_harness, client):
    dataset = [{"question": "Q1", "reference_answer": "A1"}]
    client.provider.add_text("A1")
    client.provider.add_text(json.dumps({"correct": True, "reasoning": "Correct."}))

    async def scripted_agent(client, question):
        response = await client.complete([])
        return response.message.content

    result = await eval_harness.evaluate_dataset(client, scripted_agent, dataset)

    assert result["accuracy"] == 1.0
