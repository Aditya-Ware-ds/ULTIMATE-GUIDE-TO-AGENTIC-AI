# Multi-agent failure modes

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Name concrete multi-agent failure modes beyond single-agent stopping conditions.
- Design a supervisor loop that detects and recovers from a stuck or looping worker.
- Explain why multi-agent systems need more monitoring, not less, than single agents.

## Intuition

Module 04's stopping-condition discipline (max-steps, explicit done-signals)
solves single-agent runaway loops. Multi-agent systems have all of those
same risks, plus new ones that only emerge from agents interacting with each
other -- a supervisor and worker can each be individually well-behaved and
still produce a system that never terminates, wastes work, or silently fails.

## The concept

### Infinite handoff loops

Agent A hands off to agent B, who decides the task actually needs agent A,
who hands back to B... Each individual handoff decision can look reasonable
in isolation while the system as a whole never converges. **Mitigation**: a
global step/handoff budget across the *entire* multi-agent run (not just
per-agent), the same max-steps discipline from Module 04 applied at the
system level, not the individual-agent level.

```python
async def run_with_handoff_budget(initial_agent, task: str, max_handoffs: int = 5) -> str:
    current_agent = initial_agent
    for _ in range(max_handoffs):
        result, next_agent = await current_agent.run(task)
        if next_agent is None:
            return result
        current_agent = next_agent
    return "Stopped: exceeded maximum handoffs without resolution."
```

### Duplicated or contradictory work

Two workers, given overlapping sub-tasks, can both complete real work that
overlaps or contradicts -- a research agent and a fact-checking agent that
both search the same source, or two workers writing conflicting sections of
a report. **Mitigation**: shared, visible state (which sub-tasks are
claimed/in-progress/done) rather than assuming implicit non-overlap, and a
synthesis step that explicitly reconciles rather than concatenates.

### A supervisor that can't tell a worker actually finished

If a worker's "done" signal is just "I stopped producing tool calls" (Module
04's natural-completion signal), a worker that got confused and gave up
looks identical, from the supervisor's perspective, to one that succeeded.
**Mitigation**: workers should report an explicit status (succeeded / failed
/ needs clarification) rather than the supervisor inferring success from the
mere presence of a response, the same "explicit done-signal" discipline from
Module 04 lesson 2, applied to inter-agent communication.

### Cascading cost

Every agent-to-agent handoff or worker dispatch is itself a set of model
calls (Module 02's cost lesson) -- a multi-agent system with a hierarchy 3
levels deep multiplies cost at every level, and a bug causing one extra
unnecessary round of delegation multiplies across everything below it in the
hierarchy. **Mitigation**: a cost budget tracked across the whole run, not
just a step count, aborting (with a clear message, not a silent partial
result) if exceeded.

## Deeper: multi-agent systems need more observability, not less

Because failures can emerge from *interaction* between agents rather than
any single agent's individual behavior, debugging a multi-agent failure
means being able to see the whole conversation/handoff graph, not just one
agent's trace. This is a direct preview of Module 17 (observability) --
multi-agent systems are exactly where tracing (which agent said what, in what
order, with what token/cost accounting) stops being a nice-to-have and
becomes necessary for debugging at all.

## When not to use this

This lesson's mitigations add real overhead (budgets to track, explicit
status reporting, shared state to maintain) -- appropriate for genuinely
multi-agent systems, not something to bolt onto a single agent that doesn't
need it.

## Common mistakes

- Setting a per-agent step budget but no *system-wide* budget, missing
  exactly the infinite-handoff-loop failure mode this lesson opens with.
- Trusting a worker's plain-text summary as proof of success instead of
  requiring an explicit, structured status the supervisor can check
  mechanically (Module 02's structured outputs, applied here).
- Debugging a multi-agent failure by staring at one agent's log in isolation,
  missing that the actual bug is in how two agents' outputs interact.

## Key takeaways

- Multi-agent systems have failure modes beyond single-agent stopping conditions: infinite handoffs, duplicated work, ambiguous success signals, and cascading cost.
- Mitigate with system-wide budgets (not just per-agent), explicit structured status reporting, and shared visible state.
- Multi-agent debugging needs full-system observability (a preview of Module 17), since failures can emerge from interaction, not any single agent's behavior.

## Lab

[`labs/01-supervisor-worker/`](../labs/01-supervisor-worker/README.md)
