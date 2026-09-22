# Routing and parallelization

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45 minutes

## Learning objectives

- Implement routing: classify a request, then dispatch to a specialized handler.
- Implement parallelization: run independent sub-tasks concurrently and combine results.
- Know how to tell whether sub-tasks are actually independent enough to parallelize safely.

## Intuition

**Routing** and **parallelization** are both about not treating every request
identically. Routing picks *which* specialized path handles a request;
parallelization runs *multiple* independent paths at once instead of one after
another. Both are ways of matching the system's structure to the actual shape
of the work, rather than funneling everything through one generic path.

## The concept

### Routing: classify, then dispatch

```python
async def route(client: LLMClient, request: str) -> str:
    schema = {
        "type": "object",
        "properties": {"category": {"type": "string", "enum": ["billing", "technical", "general"]}},
        "required": ["category"],
    }
    response = await client.complete(
        [Message(role=Role.USER, content=f"Classify this request: {request}")],
        response_schema=schema,
    )
    return json.loads(response.message.content)["category"]


async def handle_request(client: LLMClient, request: str) -> str:
    category = await route(client, request)
    handler = {"billing": handle_billing, "technical": handle_technical, "general": handle_general}[
        category
    ]
    return await handler(client, request)
```

Routing lets each specialized handler have a narrower, more focused system
prompt and tool set (Module 05's context-budget point: a billing handler
doesn't need technical-support tools cluttering its context), and lets you use
different models per category (a cheap model for simple general questions, a
more capable one for technical issues) -- Module 19's model routing is this
same idea applied at the infrastructure level.

### Parallelization: fan out independent work

```python
async def parallel_research(client: LLMClient, questions: list[str]) -> list[str]:
    tasks = [answer_question(client, q) for q in questions]
    return await asyncio.gather(*tasks)
```

This is Module 00, lesson 04's `asyncio.gather` applied directly: if
sub-questions are genuinely independent (answering one doesn't need another's
result), running them concurrently reduces total wall-clock time to roughly
the slowest single sub-task, not the sum of all of them.

## Deeper: the independence check is the whole safety condition

Parallelization is only correct when sub-tasks are truly independent -- no
sub-task's input depends on another's output. A multi-hop question (Module
04's ReAct example, where the second search depends on the first search's
result) is *not* safely parallelizable; forcing it into `asyncio.gather` would
run the second lookup before the first one's answer is known, producing
nonsense. Before parallelizing, explicitly check: does step B need anything
step A produces? If yes, they're sequential, not parallel, regardless of how
tempting the latency win looks.

## When not to use this

Don't add routing for a system with only one real category of request -- the
classification step itself costs a call and adds a failure mode (misrouting)
for no benefit if there's nothing to route between. Don't parallelize
dependent steps just because concurrency is available -- correctness first,
latency second.

## Common mistakes

- Routing to a category that doesn't have a real, meaningfully different
  handler -- if every category ends up doing basically the same thing, the
  routing step is pure overhead.
- Parallelizing steps that look independent but secretly share mutable state
  (e.g. two "independent" tasks both appending to the same list without
  synchronization) -- Python's `asyncio` is single-threaded, so this is more
  about logical independence (do results depend on each other) than classic
  thread-safety, but shared mutable state across concurrent tasks is still a
  real source of bugs.
- Not handling one sub-task's failure in a parallel batch -- `asyncio.gather`
  by default propagates the first exception and cancels remaining tasks; decide
  deliberately whether that's the behavior you want, or whether partial results
  (via `return_exceptions=True`) are more appropriate for your use case.

## Key takeaways

- Routing classifies a request and dispatches to a specialized handler with its own focused prompt/tools/model.
- Parallelization runs genuinely independent sub-tasks concurrently via `asyncio.gather`, cutting wall-clock time to roughly the slowest single task.
- Parallelizing dependent steps produces wrong results, not just wasted effort -- always check independence first.

## Lab

[`labs/01-plan-vs-evaluate/`](../labs/01-plan-vs-evaluate/README.md)
