# Module 08 -- Planning & reasoning patterns

**Difficulty:** ★★★★☆ · **Time estimate:** 7-9 hours

## Objectives

By the end of this module you can:

- Implement plan-and-execute: generate a plan up front, then execute each step.
- Implement reflection / evaluator-optimizer: generate, critique, and revise.
- Explain routing, parallelization, and orchestrator-workers, and when each earns its complexity.
- Decide, for a given task, whether a workflow (fixed steps) or an agent (model decides) is the right shape -- and defend that decision.

## Prerequisites

[Module 07 -- Memory & state](../07-memory-and-state/README.md)

## Why this module exists

Modules 03-07 built one shape of agent: a loop that decides its next single
step, one step at a time. That's not the only way to structure agentic work.
This module is a catalog of the other well-established shapes -- planning
ahead instead of deciding one step at a time, critiquing your own output
before returning it, splitting a task across specialized workers, running
independent steps concurrently -- and, just as importantly, when a fixed
*workflow* (no model deciding anything about control flow) beats an agent
entirely.

## Contents

- [`lessons/01-plan-and-execute.md`](lessons/01-plan-and-execute.md)
- [`lessons/02-reflection-and-evaluator-optimizer.md`](lessons/02-reflection-and-evaluator-optimizer.md)
- [`lessons/03-routing-and-parallelization.md`](lessons/03-routing-and-parallelization.md)
- [`lessons/04-orchestrator-workers.md`](lessons/04-orchestrator-workers.md)
- [`lessons/05-workflow-vs-agent.md`](lessons/05-workflow-vs-agent.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-plan-vs-evaluate/`](labs/01-plan-vs-evaluate/) -- implement plan-and-execute AND evaluator-optimizer for the same task and compare
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 09 -- Human-in-the-loop](../09-human-in-the-loop/README.md)
