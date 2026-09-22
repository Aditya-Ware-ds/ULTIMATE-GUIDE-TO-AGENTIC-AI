# Plan-and-execute

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~1 hour

## Learning objectives

- Explain how plan-and-execute differs from Module 04's step-by-step ReAct loop.
- Implement a planning call that produces a structured list of steps.
- Know when planning ahead helps versus when it just adds latency for no benefit.

## Intuition

Module 04's agent loop decides its next action one step at a time, based only
on what's happened so far -- it never commits to a multi-step plan in advance.
**Plan-and-execute** flips this: the model first produces a full plan (an
ordered list of steps) for the whole task, then a (possibly simpler, cheaper)
executor works through that plan step by step. This trades some flexibility
(the plan doesn't automatically adapt mid-execution the way step-by-step
reasoning does) for predictability and, often, cost: a smaller/cheaper model
can often execute a well-specified plan even if a stronger model was needed to
produce it.

## The concept

### The two phases

```python
async def plan(client: LLMClient, task: str) -> list[str]:
    schema = {
        "type": "object",
        "properties": {"steps": {"type": "array", "items": {"type": "string"}}},
        "required": ["steps"],
    }
    response = await client.complete(
        [Message(role=Role.USER, content=f"Break this task into steps: {task}")],
        response_schema=schema,
    )
    return json.loads(response.message.content)["steps"]


async def execute_step(client: LLMClient, step: str, tools, registry) -> str:
    # a small tool-loop for just this one step, same shape as Module 03/04
    ...
```

**Planning** uses Module 02's structured outputs (lesson 03) to get a reliably
parseable list of steps -- this is exactly the kind of extraction task
structured outputs are built for. **Execution** runs each step, often through
a small tool-calling loop (Module 03/04's machinery), then a final synthesis
call combines the step results into an answer.

### Why this can be cheaper and more predictable than pure step-by-step

Because the plan is generated once and steps are typically simpler than the
whole task, execution can often use a cheaper model (Module 02's cost lesson,
Module 19's model routing) than planning needed. It's also more
*predictable*: you can inspect and validate the plan before executing any of
it (useful for Module 09's human-in-the-loop approval), and a failure in step 3
doesn't require the model to re-derive the whole strategy from scratch --  the
remaining plan steps are already known.

### The trade-off: plans can go stale mid-execution

If executing step 2 reveals information that changes what step 3 *should* be,
a rigid plan-and-execute loop won't adapt automatically -- it'll execute the
original step 3 as planned. This is the core trade-off against Module 04's
step-by-step loop, which re-evaluates what to do next after every observation.
Some plan-and-execute systems add a re-planning step (regenerate the remaining
plan if a step's result is surprising) to mitigate this, at the cost of
looking more like the step-by-step pattern again.

## Deeper: plan-and-execute is a special case of workflow/agent hybridization

The planning phase is agentic (the model decides the plan's content), but
execution can be either a fixed workflow (run each step in the given order, no
further model judgment about control flow) or itself agentic (each step
executed via a full agent loop). Recognizing this spectrum -- purely fixed
workflow at one end, purely step-by-step agent at the other, with
plan-and-execute occupying a middle position -- is more useful than treating
"workflow" and "agent" as a strict binary (lesson 05 returns to this).

## When not to use this

Don't use plan-and-execute for tasks where later steps are genuinely
contingent on earlier results in ways you can't predict ahead of time -- Module
04's step-by-step loop (or a plan-and-execute variant with re-planning) fits
better. Also skip it for simple, single-step tasks where a plan of one step is
pure overhead.

## Common mistakes

- Never validating the plan before executing it -- a malformed or nonsensical
  plan (e.g. an empty steps list, or a step that doesn't map to any available
  tool) should be caught before spending execution-phase calls on it.
- Assuming the plan is correct just because it's well-formed JSON -- structured
  outputs (Module 02) guarantee *shape*, not correctness of *content*.
- Using an unnecessarily expensive model for straightforward execution steps
  when a cheaper model could execute the same well-specified step just as well
  (Module 19's model routing).

## Key takeaways

- Plan-and-execute generates a full plan up front (via structured outputs), then executes steps, versus Module 04's one-step-at-a-time decisions.
- This trades adaptability for predictability, inspectability, and often lower execution cost.
- It sits on a spectrum between a fixed workflow and a fully step-by-step agent, not as a wholly separate category.

## Lab

[`labs/01-plan-vs-evaluate/`](../labs/01-plan-vs-evaluate/README.md)
