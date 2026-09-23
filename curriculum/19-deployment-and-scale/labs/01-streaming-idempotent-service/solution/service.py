"""Lab 19.01: a FastAPI service wrapping an agent, with idempotent job
handling and a streaming endpoint. Reference solution. See ../README.md.
"""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from shared.llm import LLMClient, Message, Role, get_client

_JOBS: dict[str, dict] = {}


def get_llm_client() -> LLMClient:
    return get_client()


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


@app.get("/jobs/{idempotency_key}")
async def get_job(idempotency_key: str) -> dict:
    if idempotency_key not in _JOBS:
        raise HTTPException(status_code=404, detail="Job not found")
    return _JOBS[idempotency_key]


@app.post("/jobs/stream")
async def stream_job(
    payload: dict, client: LLMClient = Depends(get_llm_client)
) -> StreamingResponse:
    idempotency_key = payload["idempotency_key"]
    if idempotency_key not in _JOBS:
        result = await run_agent_job(client, payload["input"])
        _JOBS[idempotency_key] = {"status": "completed", "result": result}
    result = _JOBS[idempotency_key]["result"]

    async def generate():
        for word in result.split(" "):
            yield word + " "

    return StreamingResponse(generate(), media_type="text/plain")
