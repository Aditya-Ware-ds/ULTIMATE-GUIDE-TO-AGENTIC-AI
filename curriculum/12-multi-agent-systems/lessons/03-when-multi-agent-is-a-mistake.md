# When multi-agent is a mistake

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~30 minutes

## Learning objectives

- Recognize the symptoms of reaching for multi-agent when a single agent (or no agent) would do.
- Apply a concrete decision process before adding a second agent to a system.
- Explain why multi-agent's costs (latency, cost, debuggability) are not optional extras.

## Intuition

Modules 08 and 12 gave you real tools for building multi-agent systems. Having
the tools creates its own risk: once you know how to build a supervisor and
three workers, it's tempting to reach for that shape even when a single agent
with a good prompt and a few tools (Modules 03-04) would solve the same
problem with a fraction of the latency, cost, and failure surface.

## The concept

### The symptoms of over-reaching for multi-agent

- **The "sub-tasks" aren't actually distinct skills.** If every worker would
  use the same tools and the same underlying model, splitting them into
  separate agents adds coordination overhead without adding capability --
  it's one agent's job, just described three times.
- **The task is a single, sequential chain of steps.** Module 04's ReAct
  loop or Module 08's plan-and-execute already handle sequential multi-step
  tasks well; multi-agent's value is *specialization* and *parallelism*, not
  "more than one step."
- **You can't articulate what each agent knows that the others don't.** A
  real multi-agent boundary usually maps to a real difference in context,
  tools, or system prompt. If a supervisor and its worker would receive
  identical instructions and tools, they're the same agent.
- **The problem doesn't actually need an LLM at all.** Module 03's tool-use
  lesson already flagged this: if the "reasoning" is really just a fixed
  sequence of deterministic steps, plain code outperforms even a single
  agent, let alone a multi-agent system, on cost, latency, and reliability.

### The decision process

Before adding a second agent, answer, in order:

1. **Does this need an agent at all**, or is it deterministic enough for
   plain code (Module 04's "when not to use this")? If plain code works,
   stop here.
2. **Does a single agent with more/better tools solve it** (Module 03)? Most
   tasks that feel like they need "coordination" actually just need one
   agent with a clearer prompt and the right tool set.
3. **Does the task have genuinely distinct sub-skills, or a genuine need for
   parallel independent work**, such that a single agent's context would get
   overloaded or its behavior would need to switch personas mid-task? Only
   here does Module 12's supervisor-worker (or another topology from lesson
   01) earn its cost.

```python
def should_use_multi_agent(task_description: str, distinct_skills: list[str]) -> bool:
    if len(distinct_skills) <= 1:
        return False  # one skill: one agent (or no agent) is enough
    if _fits_in_single_context(task_description):
        return False  # a single agent with more tools would do
    return True  # genuinely distinct skills, worth the coordination cost
```

(`_fits_in_single_context` is illustrative -- in practice this is a judgment
call about whether one system prompt and one tool set can competently cover
every sub-skill the task needs.)

### The real costs, restated plainly

- **Latency**: every hop (supervisor → worker → supervisor) is at least one
  extra full model round-trip, compounding with topology depth.
- **Cost**: Module 08's parallelization lesson already covered this --
  multi-agent multiplies token spend across every agent involved, not just
  the "main" one.
- **Debuggability**: lesson 02 of this module showed failures that only
  emerge from inter-agent interaction -- a real cost paid on every incident,
  not just at build time.

## Deeper: this mirrors the workflow-vs-agent decision from Module 08

Module 08 asked "should this be a fixed workflow or an autonomous agent?"
before reaching for autonomy. This lesson asks the same style of question one
level up: "should this be one agent or several?" In both cases the answer is
governed by the same principle -- add flexibility/complexity only where the
problem's actual variability demands it, not by default.

## When not to use this

This lesson is itself a caution against overuse -- it isn't an argument
against multi-agent systems in general. Genuinely distinct specialists
working on genuinely parallel or divergent sub-problems (Module 12's own
lab, or a real research-plus-fact-check pipeline) are exactly where the
supervisor-worker pattern pays for itself.

## Common mistakes

- Reaching for multi-agent because a tutorial or framework made it easy, not
  because the problem's structure calls for it (lesson 01's "Deeper"
  section made the same point about topology choice).
- Splitting a single coherent task into "agents" that all share the same
  prompt and tools, gaining coordination overhead with no real specialization.
- Never revisiting the decision -- a system that started as genuinely
  multi-agent can be simplified back to one agent as the task's actual
  shape becomes clearer during development.

## Key takeaways

- Multi-agent earns its cost only when sub-tasks need genuinely distinct skills/context or genuine parallelism -- not merely because a task has multiple steps.
- Always check, in order: does this need an agent at all → does a single agent with better tools suffice → only then reach for multi-agent.
- Multi-agent's costs (latency, token spend, debuggability) are real and compounding, not optional extras to worry about later.

## Lab

[`labs/01-supervisor-worker/`](../labs/01-supervisor-worker/README.md)
