# Cheatsheet: agent design patterns

From Module 08 (Planning & reasoning) and Module 12 (Multi-agent systems).
One line each: what it is, and when to reach for it.

| Pattern | What it is | Reach for it when |
|---|---|---|
| **Plan-and-execute** | Generate a full plan up front, then execute each step in order. | The task decomposes cleanly into steps you can commit to before starting. |
| **Reflection / evaluator-optimizer** | One call drafts, a separate call critiques, loop until approved or budget exhausted. | Quality matters more than speed and there's no mechanical correctness check. |
| **Routing** | A cheap classification step sends a request to the right specialized handler. | Inputs fall into a few distinct categories that need different handling. |
| **Parallelization** | Run independent, predetermined sub-tasks concurrently with `asyncio.gather`. | Sub-tasks are genuinely independent -- neither depends on another's output. |
| **Orchestrator-workers** | A coordinator decides how to split work at runtime, dispatches, then synthesizes. | Sub-tasks aren't knowable in advance; workers may need their own tools/specialization. |
| **Supervisor-worker (multi-agent)** | Orchestrator-workers with workers framed as real specialists (researcher, writer, critic). | Sub-tasks need genuinely distinct skills, context, or tools -- not just parallel copies of the same job. |
| **Handoff** | Agents transfer full control (and context) to each other as needed, no central coordinator. | Which agent is "right" changes as the conversation develops. |
| **Debate** | Independent attempts (possibly different models), judged by a separate arbiter. | Independent, unbiased attempts are worth more than one attempt iteratively revised. |
| **Workflow (no agent)** | Fixed, code-controlled sequence of steps, no model deciding what happens next. | You can enumerate every instance's steps in advance -- almost always cheaper and more reliable than an agent. |

## The one question to ask before reaching for any of these

**Does this need an agent (or multiple agents) at all, or is it deterministic
enough for plain code / a single well-tooled agent?** (Module 08 lesson 05,
Module 12 lesson 03.) Multi-agent and reflection both add real latency and
cost -- earn the complexity with the problem's actual structure, don't
default to it.

See: `curriculum/08-planning-and-reasoning/`, `curriculum/12-multi-agent-systems/`.
