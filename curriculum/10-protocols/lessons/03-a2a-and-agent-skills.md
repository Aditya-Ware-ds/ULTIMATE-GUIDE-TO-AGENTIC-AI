# A2A and Agent Skills

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~1 hour

## Learning objectives

- Explain what A2A standardizes and implement a minimal version of its task lifecycle.
- Explain what Agent Skills standardizes and package a tool as a valid `SKILL.md`.
- Distinguish all three of this module's protocols by the specific problem each solves.

## Intuition

MCP (lessons 01-02) standardizes an agent *calling a tool*. **A2A**
standardizes something different: one *agent* handing work to *another
agent* -- not a stateless function call, but a task that might take time,
need clarification, or produce a rich result. **Agent Skills** standardizes a
third, different thing: packaging domain knowledge and workflows into a
portable folder any compliant agent can load on demand, without a live
connection to anything -- more like a library than a service call.

## The concept

### A2A: agents delegating tasks to other agents

An A2A **AgentCard** is metadata one agent publishes describing what it can
do -- name, description, declared skills, capabilities (e.g. does it support
streaming updates), and how to reach it. A **task** moves through a defined
lifecycle as the receiving agent works on it:

```
submitted -> working -> [input-required | auth-required] -> completed
                                                           -> failed
                                                           -> canceled
                                                           -> rejected
```

`input-required` and `auth-required` are *interrupted* states -- the task
pauses, waiting on the client, similar in spirit to Module 09's approval
gates, but here the "pause" is a formal part of an inter-agent task's state
machine, not an ad hoc mechanism you built yourself.

A minimal, illustrative version of this lifecycle (simplified -- not the full
A2A wire protocol/SDK, which also covers Parts, Artifacts, streaming, and
authentication):

```python
from dataclasses import dataclass, field
from enum import StrEnum


class TaskState(StrEnum):
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input-required"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    state: TaskState = TaskState.SUBMITTED
    result: str | None = None


def advance(task: Task, requesting_agent_input: bool = False) -> Task:
    if task.state == TaskState.SUBMITTED:
        task.state = TaskState.INPUT_REQUIRED if requesting_agent_input else TaskState.WORKING
    return task
```

### Agent Skills: portable, on-demand capabilities

A **skill** is a folder with a `SKILL.md` file (YAML frontmatter with, at
minimum, `name` and `description`) plus any bundled scripts/references/assets
it needs. Agents load skills via **progressive disclosure**:

1. **Discovery** -- at startup, the agent sees only every skill's `name` and
   `description` (small, cheap, always in context).
2. **Activation** -- when a task matches a skill's description, the agent
   loads that skill's full `SKILL.md` instructions into context.
3. **Execution** -- the agent follows those instructions, optionally running
   bundled scripts or reading bundled reference files.

```markdown
---
name: invoice-calculator
description: Calculates invoice totals including tax and discounts. Use when the user asks about invoice amounts, totals, or tax calculations.
---

# Invoice calculator

To calculate an invoice total: sum the line items, apply any discount
percentage, then apply the tax rate to the discounted subtotal.
```

This is exactly the same format used to package the instructions loaded
throughout this Claude Code session you're using right now -- Agent Skills
isn't a hypothetical example; it's a currently-operating standard.

### Choosing between the three

| Need | Protocol |
|---|---|
| An agent calls a specific tool/reads specific data from a service | MCP |
| One agent delegates a task to another (possibly long-running, autonomous) agent | A2A |
| Package reusable domain knowledge/workflow instructions for any compliant agent to load on demand | Agent Skills |

## Deeper: these three are complementary, not competing

A real system plausibly uses all three at once: an orchestrating agent (Module
08) delegates a sub-task to a specialist agent via A2A; that specialist agent
calls tools via MCP; both agents load relevant Agent Skills for
domain-specific instructions neither would otherwise have. They standardize
different *relationships* (client-to-tool, agent-to-agent, agent-to-
knowledge), not different implementations of the same relationship.

## When not to use this

Don't reach for A2A's full task-lifecycle machinery for a same-process
function call -- that's just a function call (or an MCP tool if it needs to
cross a process boundary to a non-agent service). Don't package a skill for
one-off, single-use instructions that fit fine directly in a system prompt --
Agent Skills earns its complexity when instructions are substantial and
reused across many tasks or products.

## Common mistakes

- Building a custom, ad hoc "agent talks to agent" protocol when A2A already
  standardizes this -- reinventing task-lifecycle semantics (interrupted vs.
  terminal states, in particular) is easy to get subtly wrong.
- Writing a `SKILL.md` with a vague `description` -- discovery (stage 1 above)
  depends entirely on the description alone; if it doesn't clearly say when
  the skill applies, the agent won't activate it when it should (the same
  point Module 03's tool-description lesson made, applied to skills).
- Confusing "my agent has an AgentCard" with "my agent is now interoperable" --
  publishing a card is necessary but not sufficient; the receiving agent also
  needs a compliant client implementation.

## Key takeaways

- A2A standardizes agent-to-agent task delegation with a formal lifecycle (submitted/working/interrupted states/terminal states).
- Agent Skills standardizes portable, on-demand capability packages loaded via progressive disclosure (discovery -> activation -> execution).
- MCP, A2A, and Agent Skills solve different relationships and are commonly used together, not as alternatives to each other.

## Lab

[`labs/02-a2a-task-handoff/`](../labs/02-a2a-task-handoff/README.md) and
[`labs/03-agent-skill-package/`](../labs/03-agent-skill-package/README.md)
