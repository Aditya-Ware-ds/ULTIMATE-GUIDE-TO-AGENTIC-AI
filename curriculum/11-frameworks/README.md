# Module 11 -- Frameworks

**Difficulty:** ★★★★★ · **Time estimate:** 12-16 hours (this is the largest module in the curriculum)

## Objectives

By the end of this module you can:

- Build the same reference agent in each of the 9 current major agent frameworks.
- Read any of these frameworks' docs and map their abstractions back to the from-scratch concepts in Modules 03-09.
- Choose a framework for a real project using the verified comparison matrix, not vibes or hype.

## Prerequisites

Level 3, Module 10 (Protocols).

## The reference task (built 9 times)

Every framework lab in this module implements the **same** small agent: given
a math question like `"What is 15 times 7, plus 3?"`, the agent calls a
`calculate(expression: str) -> float` tool and returns the numeric answer.
This task is deliberately trivial -- the point of this module is comparing
each framework's *syntax and abstractions* for tool definition, the agent
loop, and testing, not building something impressive. You already know how
to build a much more capable agent by hand (Modules 03-09); now you're
learning 9 different sets of training wheels for it.

## Why this module exists

Frameworks exist to save you from re-writing Modules 03-09's plumbing (tool
dispatch, the agent loop, message formatting) for every new project. Having
built that plumbing by hand, you're in a position most framework users never
reach: you can tell exactly what each framework is doing for you, and exactly
what it's hiding. That's the difference between using a framework and being
used by one.

## A note on scope and dependencies

Each framework lives in its own `uv` dependency group (see `pyproject.toml`)
rather than the default install -- 9 fast-moving frameworks in one
`dependencies` list would create real version-conflict risk and bloat
`make setup` for everyone, even learners only interested in a couple of
frameworks. Each lab's tests use `pytest.importorskip(...)` so `make test`
stays green by default; to actually run and verify a given framework's tests,
install its group first: `uv sync --group <framework-name>` (each lab's
README says exactly which one). Every lab in this module was built and its
tests verified passing with the relevant group installed before being
committed -- see `PROGRESS.md` for exact verification notes per framework,
including the one framework (Claude Agent SDK) that cannot be tested fully
offline for a structural reason explained in its own lab README.

## Contents

- [`lessons/01-why-frameworks-exist.md`](lessons/01-why-frameworks-exist.md)
- `labs/01-langgraph/` through `labs/09-llamaindex-workflows/` -- the reference agent, once per framework
- [`lessons/02-comparison-matrix-and-how-to-choose.md`](lessons/02-comparison-matrix-and-how-to-choose.md) -- written last, after all 9 are built
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 12 -- Multi-agent systems](../12-multi-agent-systems/README.md)
