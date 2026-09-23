"""Lab 19.01: a FastAPI service wrapping an agent, with idempotent job
handling and a streaming endpoint. See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/19-deployment-and-scale/labs/01-streaming-idempotent-service/tests
"""

from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException  # noqa: F401 -- used below
from fastapi.responses import (
    StreamingResponse,  # noqa: F401 -- used once you implement stream_job below
)

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
    """If payload["idempotency_key"] is already in _JOBS, return
    {**_JOBS[key], "idempotent_replay": True} WITHOUT calling run_agent_job
    again. Otherwise, run the agent on payload["input"], store
    {"status": "completed", "result": result} under that key in _JOBS, and
    return it with "idempotent_replay": False.

    TODO: implement this.
    """
    raise NotImplementedError


@app.get("/jobs/{idempotency_key}")
async def get_job(idempotency_key: str) -> dict:
    """Return _JOBS[idempotency_key], or raise
    HTTPException(status_code=404, detail="Job not found") if it doesn't exist.

    TODO: implement this.
    """
    raise NotImplementedError


@app.post("/jobs/stream")
async def stream_job(
    payload: dict, client: LLMClient = Depends(get_llm_client)
) -> StreamingResponse:
    """Same idempotency behavior as create_job (reuse an existing result
    under payload["idempotency_key"] if present, otherwise compute and
    store one), then return a StreamingResponse that yields the result one
    word at a time (each word followed by a space), media_type="text/plain".

    TODO: implement this.
    """
    raise NotImplementedError
