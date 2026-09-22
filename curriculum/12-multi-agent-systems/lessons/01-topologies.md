# Multi-agent topologies

**Last verified:** 2026-09-22
**Difficulty:** ★★★★★ · **Time:** ~1 hour

## Learning objectives

- Implement supervisor-worker, this module's primary hands-on pattern.
- Explain hierarchical, handoff, swarm, and debate topologies at a level sufficient to recognize and choose between them.
- Map each topology to what you already saw in Module 11's 9 frameworks.

## Intuition

A "topology" is just the shape of who talks to whom. Module 08's
orchestrator-workers pattern already showed you one: a coordinator that
decides sub-tasks and dispatches to workers. This lesson names the rest of
the common shapes, because recognizing the topology a problem needs is most
of the design work in a multi-agent system.

## The concept

### Supervisor-worker (this module's lab)

A supervisor agent receives a task, decides which of several specialized
workers should handle it (or breaks it into pieces across workers), and
synthesizes their results -- structurally identical to Module 08's
orchestrator-workers, with workers now framed as distinct *specialists*
(a researcher, a writer, a critic) rather than generic parallel sub-tasks.

```python
async def supervisor(client, task: str, workers: dict[str, Callable]) -> str:
    worker_name = await route_to_worker(client, task, list(workers.keys()))  # Module 08's routing
    worker_result = await workers[worker_name](task)
    return await synthesize(client, task, worker_result)
```

### Hierarchical

Supervisors of supervisors -- a top-level coordinator delegates to
mid-level supervisors, each managing their own workers. This is
supervisor-worker recursively applied, useful when the problem itself
naturally decomposes into layers (a company org chart, not a flat team).

### Handoff

Instead of one supervisor retaining control, agents hand off the *entire*
conversation to each other based on what's needed next -- agent A decides
"this needs agent B" and transfers control (and context) directly, rather
than reporting back to a coordinator. OpenAI's Agents SDK has explicit
`handoffs` support (Module 11); this is the topology it's built around.

### Swarm

Multiple agents work on the same problem concurrently with lighter,
more decentralized coordination than a strict supervisor -- closer to
Module 08's plain parallelization, but with agents that can also
communicate with each other mid-task, not just report back independently.

### Debate

Two or more agents argue different positions or independently attempt the
same task, then a judge (another agent, or a person) compares results --
a structural cousin of Module 08's evaluator-optimizer, but with multiple
independent attempts compared against each other instead of one attempt
revised iteratively.

## Deeper: topology choice should follow the problem's actual structure

A flat team of specialists (supervisor-worker) fits a problem with several
genuinely distinct sub-skills needed once each. A hierarchy fits a problem
that's naturally layered. A handoff fits a problem where "who's the right
agent" changes as the conversation develops rather than being decided once
up front. Debate fits problems where independent, unbiased attempts are more
valuable than one attempt refined with feedback (Module 08's
evaluator-optimizer can share the same bias across iterations if the same
model both drafts and revises; independent debate participants don't have
that shared-bias risk). Picking the topology that matches your problem's
actual shape, rather than defaulting to whichever one you read about most
recently, is the real skill here.

## When not to use this

Don't build a hierarchy for a problem with only two or three specialists and
no natural layering -- flat supervisor-worker is simpler and sufficient.
Don't reach for debate's doubled-or-tripled cost unless independent
verification is genuinely valuable for your task's stakes (Module 16 revisits
this trade-off for evaluation specifically).

## Common mistakes

- Choosing a topology because a specific framework makes it the path of
  least resistance, rather than because it matches the problem.
- Building a handoff system where every agent could plausibly handle every
  request, making the handoff decision itself unreliable and a new source of
  errors.
- Assuming more agents/more topology sophistication always improves results
  -- lesson 03 covers when a single agent (or no agent at all) is the right
  call.

## Key takeaways

- Supervisor-worker (Module 08's orchestrator-workers, specialized) is the primary pattern this module builds by hand.
- Hierarchical, handoff, swarm, and debate are named variations solving different structural problems -- match the topology to the problem's actual shape.
- Every framework in Module 11 has some version of these topologies as a feature; you're building the pattern they automate.

## Lab

[`labs/01-supervisor-worker/`](../labs/01-supervisor-worker/README.md)
