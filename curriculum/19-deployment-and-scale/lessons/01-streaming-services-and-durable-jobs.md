# Streaming services and durable jobs

**Last verified:** 2026-09-22 (against [FastAPI's current docs](https://fastapi.tiangolo.com/))
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Wrap an agent's response in a FastAPI streaming endpoint.
- Explain why a deployed agent needs to survive a process restart mid-run, and how Module 07's checkpointing is the foundation for that.
- Test an HTTP service without a real running server, using FastAPI's `TestClient`.

## Intuition

Module 02 introduced streaming as an API shape (partial output arriving
incrementally instead of all at once); this lesson deploys that shape
behind a real HTTP endpoint, so a client consuming your agent gets the same
incremental experience over the network that Module 02's `stream_and_collect`
demonstrated in-process.

## The concept

### A minimal streaming endpoint

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


@app.post("/jobs/stream")
async def stream_job(payload: dict) -> StreamingResponse:
    result = await run_agent_job(payload["input"])

    async def generate():
        for word in result.split(" "):
            yield word + " "

    return StreamingResponse(generate(), media_type="text/plain")
```

This lab's version streams a completed result word-by-word for simplicity;
a production service would more naturally stream `client.stream()`'s chunks
(Module 02) directly to the client as they arrive from the provider,
reducing time-to-first-byte instead of waiting for the full response first.

### Testing without a real server

```python
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.post("/jobs/stream", json={"input": "hello"})
assert response.status_code == 200
```

`TestClient` (verified against FastAPI's current docs, imported from
`fastapi.testclient`) runs requests against the app in-process, with no real
socket, port, or network involved -- the same "test the real thing without
the real infrastructure" principle as Module 10's in-process MCP
`Client(mcp_server_instance)` connection, or Module 00's local HTTP server
fixture, applied to a full HTTP service this time.

### Durable jobs: checkpointing triggered by infrastructure, not just a crash

Module 07 built checkpoint/resume for an agent that gets killed mid-run;
a **durable job** is the production version of exactly that idea, triggered
by infrastructure events (a worker process restarting, a deploy rolling
out, a request timing out) rather than a simulated crash in a test. The
checkpoint format doesn't need to change -- what changes is *who* decides to
resume (a job queue or orchestrator, not a human re-running a script) and
*when* (automatically, on worker restart, not only when explicitly asked).

## Deeper: dependency injection makes a real service testable against the mock provider

```python
from fastapi import Depends
from shared.llm import get_client, LLMClient


def get_llm_client() -> LLMClient:
    return get_client()


@app.post("/jobs")
async def create_job(payload: dict, client: LLMClient = Depends(get_llm_client)): ...
```

FastAPI's dependency-injection system lets tests swap `get_llm_client` for a
function returning a scripted mock client (`app.dependency_overrides[get_llm_client] = lambda: mock_client`)
-- the exact same "swap the real provider for a scriptable fake" principle
`shared/llm/mock.py` already provides for plain function tests, now applied
at the service layer so the whole HTTP API is testable with zero API keys.

## When not to use this

Don't add streaming to an endpoint whose response is always short and
arrives quickly regardless -- streaming adds real complexity (chunked
responses, client-side incremental parsing) that only pays off when
time-to-first-byte meaningfully matters to the caller.

## Common mistakes

- Testing a FastAPI service by actually starting `uvicorn` and making real
  HTTP requests in a test suite -- slow, flaky, and unnecessary when
  `TestClient` tests the same routing/handler logic in-process.
- Building "durable jobs" as a new concept from scratch instead of
  recognizing it as Module 07's checkpoint/resume pattern, triggered by
  different (infrastructure) events.
- Streaming a result that was already fully computed before streaming
  begins (as this lab's simplified version does) and mistaking that for
  genuine latency improvement -- real benefit requires streaming from the
  provider as tokens actually arrive, not chunking a finished string.

## Key takeaways

- FastAPI's `StreamingResponse` deploys Module 02's streaming concept behind a real HTTP endpoint.
- `TestClient` tests a real service in-process, with no real server or network -- the same principle as Module 00/10's fixtures, applied to a full HTTP API.
- A durable job is Module 07's checkpoint/resume pattern, triggered by infrastructure events instead of a simulated crash.

## Lab

[`labs/01-streaming-idempotent-service/`](../labs/01-streaming-idempotent-service/README.md)
