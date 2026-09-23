def test_create_job_runs_the_agent_and_returns_result(test_client, mock_client):
    mock_client.provider.add_text("Paris")

    response = test_client.post(
        "/jobs", json={"idempotency_key": "req-1", "input": "capital of France?"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["result"] == "Paris"
    assert body["idempotent_replay"] is False


def test_repeated_request_with_same_key_does_not_rerun_the_agent(test_client, mock_client):
    mock_client.provider.add_text("Paris")
    # No second scripted response: if create_job wrongly calls the agent
    # again, the mock provider raises AssertionError for running out of script.

    first = test_client.post(
        "/jobs", json={"idempotency_key": "req-1", "input": "capital of France?"}
    )
    second = test_client.post(
        "/jobs", json={"idempotency_key": "req-1", "input": "capital of France?"}
    )

    assert first.json()["result"] == second.json()["result"] == "Paris"
    assert first.json()["idempotent_replay"] is False
    assert second.json()["idempotent_replay"] is True
    assert mock_client.provider.call_count == 1


def test_different_keys_each_run_the_agent(test_client, mock_client):
    mock_client.provider.add_text("Paris")
    mock_client.provider.add_text("Tokyo")

    first = test_client.post("/jobs", json={"idempotency_key": "a", "input": "capital of France?"})
    second = test_client.post("/jobs", json={"idempotency_key": "b", "input": "capital of Japan?"})

    assert first.json()["result"] == "Paris"
    assert second.json()["result"] == "Tokyo"
    assert mock_client.provider.call_count == 2


def test_get_job_returns_the_stored_result(test_client, mock_client):
    mock_client.provider.add_text("Paris")
    test_client.post("/jobs", json={"idempotency_key": "req-1", "input": "capital of France?"})

    response = test_client.get("/jobs/req-1")

    assert response.status_code == 200
    assert response.json()["result"] == "Paris"


def test_get_job_unknown_key_returns_404(test_client):
    response = test_client.get("/jobs/does-not-exist")

    assert response.status_code == 404


def test_stream_job_streams_the_result_and_reassembles_correctly(test_client, mock_client):
    mock_client.provider.add_text("The capital of France is Paris.")

    response = test_client.post(
        "/jobs/stream", json={"idempotency_key": "req-1", "input": "capital of France?"}
    )

    assert response.status_code == 200
    assert response.text.strip() == "The capital of France is Paris."


def test_stream_job_reuses_idempotent_result_without_rerunning_the_agent(test_client, mock_client):
    mock_client.provider.add_text("Paris")

    test_client.post("/jobs", json={"idempotency_key": "req-1", "input": "capital of France?"})
    stream_response = test_client.post(
        "/jobs/stream", json={"idempotency_key": "req-1", "input": "capital of France?"}
    )

    assert stream_response.text.strip() == "Paris"
    assert mock_client.provider.call_count == 1
