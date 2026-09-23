# Retries, idempotency, and rate limits

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~40 minutes

## Learning objectives

- Explain why network retries are dangerous for consequential agent actions without an idempotency key.
- Implement idempotent job handling: a repeated request with the same key never re-runs the underlying work.
- Connect rate limiting to Module 04/09's step-budget discipline as the same "bound the damage" principle applied to request volume.

## Intuition

A client that doesn't get a timely response to a request often retries it
-- reasonable behavior for a network that can drop responses in transit.
But if the *first* request actually succeeded and only the *response*
was lost, a naive retry means the underlying work happens twice. For an
agent that might call Module 18's `send_email`-style consequential tools,
"twice" can mean a real duplicate action a user never asked for.

## The concept

### Idempotent job handling

```python
_JOBS: dict[str, dict] = {}


async def create_job(idempotency_key: str, user_input: str, client) -> dict:
    if idempotency_key in _JOBS:
        return {**_JOBS[idempotency_key], "idempotent_replay": True}
    result = await run_agent_job(client, user_input)
    _JOBS[idempotency_key] = {"status": "completed", "result": result}
    return {**_JOBS[idempotency_key], "idempotent_replay": False}
```

The caller supplies a unique key per *logical* request (not per HTTP
attempt) -- a retry of the same logical request reuses the same key, so the
second attempt returns the already-computed result instead of running the
agent (and any consequential tool calls it might make) a second time. This
is the deployment-layer version of Module 18's "the tool is the trust
boundary" principle: correctness under retries shouldn't depend on the
client behaving perfectly, the same way security shouldn't depend on the
model behaving perfectly.

### Why this matters more for agents than typical CRUD APIs

A duplicate `GET` request is harmless. A duplicate agent run that includes
a consequential tool call (an email sent, a refund issued, an order placed)
is not -- and an agent's response time is often long enough (multiple model
calls, tool executions) that a client timing out and retrying is a real,
common scenario, not an edge case.

### Rate limits: bounding request volume the way step budgets bound loop length

Module 04's `max_steps` bounds how long a single agent run can go; a rate
limit bounds how many requests a client (or the service as a whole) can
make in a given window. Both exist for the identical reason: an unbounded
resource (steps in one case, requests in the other) can be consumed far
faster than intended, whether by a bug, a misbehaving client, or a
deliberate abuse attempt, and a hard limit converts "unbounded damage" into
"bounded, known damage."

## Deeper: idempotency keys need a defined lifetime

An idempotency key can't be remembered forever without unbounded storage
growth -- real systems expire keys after a defined window (commonly 24
hours) past which the same key is treated as a new request. Choosing that
window is a real design decision: too short risks a legitimate late retry
being treated as new work; too long wastes storage on keys that will never
be reused.

## When not to use this

Don't add idempotency-key handling to a purely read-only endpoint with no
side effects -- a duplicate read causes no harm, so the mechanism's
complexity isn't earning anything there.

## Common mistakes

- Using the HTTP request itself (or a timestamp) as the "idempotency key"
  instead of a value the *client* generates once per logical request and
  reuses on every retry -- a timestamp-based key changes on every attempt
  and defeats the entire mechanism.
- Rate-limiting only at the API layer while ignoring that a single request
  can still trigger an unbounded number of model/tool calls internally
  (Module 04's `max_steps` still needs to be enforced independently).
- Storing idempotency keys forever, or not defining an expiry policy at
  all, leading to unbounded storage growth in a long-running production
  service.

## Key takeaways

- An idempotency key lets a retried request reuse a prior result instead of re-running consequential work -- essential once an agent can call tools with real side effects.
- Rate limits bound request volume the same way Module 04's step budgets bound loop length -- both convert an unbounded risk into a bounded, known one.
- Idempotency keys need a defined expiry window, not indefinite storage.

## Lab

[`labs/01-streaming-idempotent-service/`](../labs/01-streaming-idempotent-service/README.md)
