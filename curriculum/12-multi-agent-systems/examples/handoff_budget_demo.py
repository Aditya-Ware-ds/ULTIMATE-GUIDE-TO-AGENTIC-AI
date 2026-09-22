"""Run: uv run python curriculum/12-multi-agent-systems/examples/handoff_budget_demo.py

Shows why a per-agent step budget isn't enough for handoff systems: two
agents that keep handing off to each other, each individually "reasonable,"
still need a system-wide handoff budget to guarantee termination. See
lessons/02-failure-modes.md. No API key needed.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass


@dataclass
class HandoffAgent:
    name: str
    next_agent_name: str | None  # who this agent hands off to, if anyone

    async def run(
        self, task: str, agents: dict[str, HandoffAgent]
    ) -> tuple[str, HandoffAgent | None]:
        if self.next_agent_name is None:
            return f"[{self.name}] resolved: {task}", None
        return f"[{self.name}] needs help from {self.next_agent_name}", agents[self.next_agent_name]


async def run_with_handoff_budget(
    initial_agent: HandoffAgent,
    task: str,
    agents: dict[str, HandoffAgent],
    max_handoffs: int = 5,
) -> str:
    current_agent = initial_agent
    trace = []
    for _ in range(max_handoffs):
        result, next_agent = await current_agent.run(task, agents)
        trace.append(result)
        if next_agent is None:
            return "\n".join(trace) + f"\nDone after {len(trace)} hop(s)."
        current_agent = next_agent
    trace.append(f"Stopped: exceeded max_handoffs={max_handoffs} without resolution.")
    return "\n".join(trace)


async def main() -> None:
    # Well-behaved: agent_a resolves the task itself.
    agents_ok = {"agent_a": HandoffAgent("agent_a", None)}
    print(await run_with_handoff_budget(agents_ok["agent_a"], "simple task", agents_ok))
    print()

    # Pathological: agent_a and agent_b hand off to each other forever.
    agents_loop = {
        "agent_a": HandoffAgent("agent_a", "agent_b"),
        "agent_b": HandoffAgent("agent_b", "agent_a"),
    }
    print(await run_with_handoff_budget(agents_loop["agent_a"], "ambiguous task", agents_loop))


if __name__ == "__main__":
    asyncio.run(main())
