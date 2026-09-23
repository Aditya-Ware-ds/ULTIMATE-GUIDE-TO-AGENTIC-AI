# Lab 19.01 -- Streaming, idempotent agent service

**Difficulty:** ★★★★☆ · **Time:** ~2-3 hours

## Task

Wrap a one-call agent in a small FastAPI service with idempotent job
handling and a streaming endpoint. No API key or real running server
needed -- tested in-process against `fastapi.testclient.TestClient` and
`shared.llm.get_client("mock")`, using FastAPI's dependency-injection
override to swap in the mock client.

## Files

- `starter/service.py` -- skeleton with the pieces to implement
- `solution/service.py` -- complete reference implementation
- `tests/` -- tests that exercise idempotency, retrieval, and streaming

## Requirements

Implement these in `starter/service.py` (`run_agent_job`, `get_llm_client`,
and the FastAPI app instance are already given):

- `@app.post("/jobs") async def create_job(payload, client=Depends(get_llm_client)) -> dict`
  -- if `payload["idempotency_key"]` is already in `_JOBS`, return
  `{**_JOBS[key], "idempotent_replay": True}` **without** calling
  `run_agent_job` again. Otherwise run the agent on `payload["input"]`,
  store `{"status": "completed", "result": result}` under that key, and
  return it with `"idempotent_replay": False`.
- `@app.get("/jobs/{idempotency_key}") async def get_job(idempotency_key) -> dict`
  -- return the stored job, or raise
  `HTTPException(status_code=404, detail="Job not found")`.
- `@app.post("/jobs/stream") async def stream_job(payload, client=Depends(get_llm_client)) -> StreamingResponse`
  -- same idempotency behavior as `create_job`, then return a
  `StreamingResponse` (`media_type="text/plain"`) yielding the result one
  word at a time (each word followed by a space).

## Acceptance criteria

- All tests in `tests/` pass against your `starter/service.py`.
- A repeated `POST /jobs` with the same `idempotency_key` returns the exact
  same result **without** calling the agent again (verified via
  `mock_client.provider.call_count`).
- Different `idempotency_key`s each run the agent independently.
- `GET /jobs/{key}` returns the stored result for a known key, and `404`
  for an unknown one.
- `POST /jobs/stream` returns a response whose reassembled body text
  matches what a direct (non-streamed) call would have returned, and reuses
  an existing idempotent result rather than re-running the agent.

## Running the tests

```bash
uv run pytest curriculum/19-deployment-and-scale/labs/01-streaming-idempotent-service/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/19-deployment-and-scale/labs/01-streaming-idempotent-service/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Level 6, Module 20 -- Optimizing agents](../../../20-optimizing-agents/README.md)
