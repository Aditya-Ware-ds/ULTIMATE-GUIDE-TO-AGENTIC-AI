# Orchestrator-workers

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Explain the orchestrator-workers pattern and how it differs from plain parallelization.
- Give each worker a narrow, focused context rather than the whole task's history.
- Know why this pattern is the direct precursor to Module 12's multi-agent systems.

## Intuition

Parallelization (lesson 03) runs independent, *predetermined* sub-tasks
concurrently. **Orchestrator-workers** goes further: a central orchestrator
*decides* (at runtime, based on the task) how to break work into sub-tasks and
what each worker should focus on, dispatches those sub-tasks to worker calls
(possibly concurrently), then synthesizes their results. The orchestrator's
decisions aren't fixed in advance the way plain parallelization's task list
usually is.

## The concept

### The shape

```python
async def orchestrate(client: LLMClient, task: str) -> str:
    schema = {
        "type": "object",
        "properties": {"subtasks": {"type": "array", "items": {"type": "string"}}},
        "required": ["subtasks"],
    }
    response = await client.complete(
        [Message(role=Role.USER, content=f"Break this into independent worker sub-tasks: {task}")],
        response_schema=schema,
    )
    subtasks = json.loads(response.message.content)["subtasks"]

    worker_results = await asyncio.gather(*[run_worker(client, s) for s in subtasks])

    synthesis_prompt = "Combine these results into a final answer:\n" + "\n".join(worker_results)
    final = await client.complete([Message(role=Role.USER, content=synthesis_prompt)])
    return final.message.content or ""


async def run_worker(client: LLMClient, subtask: str) -> str:
    response = await client.complete([Message(role=Role.USER, content=subtask)])
    return response.message.content or ""
```

Notice `run_worker` receives *only* its own sub-task, not the orchestrator's
full context -- this is deliberate (Module 05's context-budget lesson): each
worker gets a narrow, focused window relevant to its piece of the problem,
rather than inheriting everything the orchestrator has seen. This keeps each
worker's context clean and, per Module 05 lesson 03, less exposed to context
rot from irrelevant accumulated history.

### Why this is plan-and-execute's sibling, not a duplicate

Orchestrator-workers looks similar to lesson 01's plan-and-execute (both
generate a breakdown, then act on it), but the emphasis differs: plan-and-execute
is usually about *sequential* steps toward one goal; orchestrator-workers is
usually about *parallel*, more loosely related sub-tasks whose results get
combined, each ideally handled by a worker specialized (via prompt, tools, or
even model choice) for its specific sub-task.

## Deeper: this is a multi-agent system, just not named that yet

Once workers are complex enough to have their own tools, their own multi-step
reasoning, or their own distinct "role" (a researcher worker, a writer worker,
a fact-checker worker), orchestrator-workers *is* a multi-agent system --
Module 12 formalizes this with more structure (agent-to-agent communication
protocols, more complex topologies) but the core idea -- one coordinator,
several specialized executors, synthesis at the end -- is exactly what you're
already building here.

## When not to use this

Don't split a task into workers when the sub-tasks aren't actually independent
enough to benefit from separation (per lesson 03's independence check), or
when the task is simple enough that one direct call handles it fine --
orchestration adds real complexity (an extra planning call, a synthesis call,
more moving pieces to debug) that needs to be earned by genuine task
complexity.

## Common mistakes

- Giving every worker the orchestrator's full context "just in case," instead
  of scoping each worker to only what it needs -- this defeats the context-
  budget benefit that's much of the point of splitting work up in the first
  place.
- No synthesis step, or a weak one -- combining worker outputs well is its own
  non-trivial task, not an afterthought; a bad synthesis pass can waste good
  worker results.
- Treating orchestrator-workers as fundamentally different from multi-agent
  systems -- recognizing they're the same idea at different scales of
  complexity will make Module 12 feel like a continuation, not a new topic.

## Key takeaways

- Orchestrator-workers dynamically decides how to split work and dispatches to workers, then synthesizes -- more flexible than plain parallelization's fixed task list.
- Each worker should get a narrow, focused context scoped to its sub-task, not the orchestrator's entire history.
- This pattern is the direct precursor to Module 12's multi-agent systems -- the difference is mostly one of degree, not kind.

## Lab

[`labs/01-plan-vs-evaluate/`](../labs/01-plan-vs-evaluate/README.md)
