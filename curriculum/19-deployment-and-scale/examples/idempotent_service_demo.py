"""Run: uv run python curriculum/19-deployment-and-scale/examples/idempotent_service_demo.py

A minimal FastAPI service wrapping a one-call agent, tested in-process with
TestClient -- no real server, no API key. Shows a repeated request with the
same idempotency key returning the cached result instead of re-running the
agent. See lessons/01-streaming-services-and-durable-jobs.md and
lessons/02-retries-idempotency-and-rate-limits.md.
"""

from __future__ import annotations

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from shared.llm import LLMClient, Message, Role, get_client

_JOBS: dict[str, dict] = {}


def get_llm_client() -> LLMClient:
    return get_client("mock")


app = FastAPI()


async def run_agent_job(client: LLMClient, user_input: str) -> str:
    response = await client.complete([Message(role=Role.USER, content=user_input)])
    return response.message.content or ""


@app.post("/jobs")
async def create_job(payload: dict, client: LLMClient = Depends(get_llm_client)) -> dict:
    idempotency_key = payload["idempotency_key"]
    if idempotency_key in _JOBS:
        return {**_JOBS[idempotency_key], "idempotent_replay": True}
    result = await run_agent_job(client, payload["input"])
    _JOBS[idempotency_key] = {"status": "completed", "result": result}
    return {**_JOBS[idempotency_key], "idempotent_replay": False}


def main() -> None:
    mock_client = get_client("mock")
    mock_client.provider.add_text("The capital of France is Paris.")
    app.dependency_overrides[get_llm_client] = lambda: mock_client

    with TestClient(app) as test_client:
        first = test_client.post(
            "/jobs", json={"idempotency_key": "req-1", "input": "What is the capital of France?"}
        )
        print("First request:", first.json())

        # A client retry, reusing the same idempotency key -- must NOT call
        # the agent again (the mock provider has no more scripted responses
        # left, so a second real call would raise).
        second = test_client.post(
            "/jobs", json={"idempotency_key": "req-1", "input": "What is the capital of France?"}
        )
        print("Retried request (same key):", second.json())

        print(f"Agent was actually called {mock_client.provider.call_count} time(s).")


if __name__ == "__main__":
    main()
