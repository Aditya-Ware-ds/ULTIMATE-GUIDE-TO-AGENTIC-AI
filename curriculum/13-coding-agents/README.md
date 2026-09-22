# Module 13 -- Coding agents

**Difficulty:** ★★★★☆ · **Time estimate:** 6-8 hours

## Objectives

By the end of this module you can:

- Explain why an agent that writes or runs code must always do so inside a sandbox, and use `shared/sandbox/` to enforce that.
- Build tools that let an agent navigate and edit a real, multi-file repository, scoped so it can never touch anything outside it.
- Implement a test-driven agent loop: edit, run the tests, read the result, iterate.
- Explain the "explore, plan, code" pattern current terminal coding agents use and why giving an agent a verifiable check changes what it can be trusted to do unattended.

## Prerequisites

[Module 12 -- Multi-agent systems](../12-multi-agent-systems/README.md)

## Why this module exists

Every agent loop this curriculum has built so far (Module 04's ReAct loop,
Module 08's planning patterns, Module 12's multi-agent systems) has called
tools that were either pure functions or read-only lookups. A coding agent
is the first place the tools themselves are dangerous by default -- reading
and writing real files, and running real processes -- which is exactly why
`shared/sandbox/` (built in Phase 0, unused until now) exists: this module is
where "never let an agent execute code outside a sandbox" (a ground rule
since day one) stops being a slogan and becomes the thing standing between
an agent's mistake and your actual filesystem.

## Contents

- [`lessons/01-sandboxed-code-execution.md`](lessons/01-sandboxed-code-execution.md)
- [`lessons/02-repo-navigation-and-editing.md`](lessons/02-repo-navigation-and-editing.md)
- [`lessons/03-test-driven-agent-loop.md`](lessons/03-test-driven-agent-loop.md)
- [`lessons/04-how-terminal-coding-agents-work.md`](lessons/04-how-terminal-coding-agents-work.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-fix-the-failing-test/`](labs/01-fix-the-failing-test/) -- an agent that fixes a failing test in a small sample repo, entirely inside `shared/sandbox/`
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 14 -- Browser & computer-use agents](../14-browser-and-computer-use-agents/README.md)
