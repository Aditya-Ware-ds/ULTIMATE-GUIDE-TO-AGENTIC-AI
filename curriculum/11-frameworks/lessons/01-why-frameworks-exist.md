# Why frameworks exist

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~30-45 minutes

## Learning objectives

- Map what a framework typically abstracts back to specific pieces you built by hand in Modules 03-09.
- Know what to look for when evaluating a new framework, having built the underlying mechanics yourself.
- Recognize the recurring shape across frameworks despite different syntax.

## Intuition

Every framework in this module wraps the same handful of ideas you already
built from scratch: a tool abstraction (Module 03), an agent loop with
stopping conditions (Module 04), and increasingly, memory (Module 07),
human-in-the-loop (Module 09), and multi-agent orchestration (Module 12).
Frameworks differ in syntax, in how much control-flow they hide versus expose,
and in which patterns they make the default -- not in inventing fundamentally
new capabilities beyond what you've already implemented by hand.

## What to map, framework to framework

| What you built | What frameworks call it |
|---|---|
| `ToolDefinition` + a Python function (Module 03) | a "tool," usually via a decorator (`@tool`) inferring the schema from type hints |
| `dispatch()` (Module 03) | handled internally by the framework's executor -- you rarely write this yourself |
| the `while step < max_steps` loop (Module 04) | an "agent," "executor," or "runner" object you configure and call `.run()`/`.invoke()` on |
| `compact_messages()` (Module 05) | sometimes built in, sometimes still your job -- check each framework's docs specifically for this; it's an easy thing to assume "the framework handles it" and be wrong |
| checkpointing (Module 07) | a "memory" or "persistence" module, if the framework has one at all |
| an approval gate (Module 09) | a "human-in-the-loop" or "interrupt" feature, if present |
| multiple cooperating agents (Module 12) | "crew," "graph," "workflow," or "multi-agent" -- widely varying vocabulary for a similar idea |

## What to actually evaluate, having built this by hand

- **How much control do you give up, and where?** Some frameworks (LangGraph)
  expose the state machine explicitly; others (CrewAI) hide it behind a
  higher-level "role" abstraction. Neither is universally better -- it depends
  on whether you need Module 08-style custom control flow or a fast default.
- **How does it handle testing without a real model?** A framework with no
  clean way to inject a fake model (Module 02's `MockLLMProvider` equivalent)
  makes writing this repo's kind of offline test suite much harder -- this
  module's labs specifically evaluate each framework on this, because it
  matters for exactly the reasons Ground Rule 4 does in this repo.
- **What does it do silently that surprises you?** Automatic retries, hidden
  system prompts, automatic history truncation -- convenient until the
  behavior doesn't match what you assumed, and you don't know to look because
  you never built the equivalent yourself. Having built it yourself, you know
  exactly what to check for.

## Deeper: frameworks converge because the problem converges

Despite very different syntax, every framework in this module ends up with
some version of: a typed tool interface, an executor loop, and a way to
inspect/test the result. This isn't coincidence -- it's the same underlying
problem (Modules 03-04) being solved repeatedly. Once you see the convergence,
picking up a 10th framework later in your career is mostly learning new
vocabulary for ideas you already understand deeply.

## When not to use this

Don't assume a framework is strictly better than hand-rolled code for every
project -- Module 04, lesson 1's point about workflows-vs-agents applies at
the framework-adoption level too: a framework's abstractions cost something
(learning curve, less transparency into failures, dependency weight) that
needs to be worth it for your specific project's complexity.

## Key takeaways

- Frameworks wrap tool definition, the agent loop, and (sometimes) memory/HITL/multi-agent orchestration -- concepts you've already built by hand.
- Evaluate a framework by how much control it trades for convenience, and how well it supports offline testing.
- Convergent design across frameworks means the underlying problem is well-understood; syntax varies, the shape doesn't.

## Labs

`labs/01-langgraph/` through `labs/09-llamaindex-workflows/`
