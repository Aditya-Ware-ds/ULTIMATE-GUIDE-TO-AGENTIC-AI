# How terminal coding agents work

**Last verified:** 2026-09-22 (against [Claude Code's best-practices docs](https://code.claude.com/docs/en/best-practices))
**Difficulty:** ★★★☆☆ · **Time:** ~30 minutes

## Learning objectives

- Describe the "explore, plan, code, commit" pattern real terminal coding agents encourage, and why each phase exists.
- Explain why context-window management is treated as the primary constraint on a coding agent's effectiveness.
- Connect this module's hand-rolled sandboxed loop to what a full terminal coding agent adds on top of it.

## Intuition

This module's lab builds one narrow slice of what a real terminal coding
agent (Claude Code, and comparable current tools) does: given a task, edit
files and run a check until it passes. Real terminal coding agents wrap that
same core loop with more structure around *when* to explore vs. act, and
active management of the one resource that degrades their performance the
fastest: the context window.

## The concept

### Explore, plan, code, commit

Claude Code's own current best-practices guidance recommends a four-phase
workflow for any non-trivial task: **explore** the relevant code read-only
first, **plan** an approach (and let a human review or edit that plan)
before any file changes happen, **implement** the plan while continuously
verifying against it, then **commit** with a clear message. The explicit
reasoning given for separating exploration from implementation: "letting
[the agent] jump straight to coding can produce code that solves the wrong
problem" -- the same problem Module 08's plan-and-execute lesson names for
agents generally, now specific to code.

This maps directly onto tools you've already built: "explore" is Module 13's
`read_file` (lesson 02, read-only); "code" is `write_file` plus `run_tests`
(lessons 02-03); "plan" is closer to Module 08's plan-and-execute output (a
list of steps) than anything hand-rolled in this module's lab, which
deliberately skips explicit planning for its narrow, single-bug task.

### Give it a way to verify its work

The same guidance states the core justification for lesson 03's test-driven
loop directly: "Claude stops when the work looks done. Without a check it
can run, 'looks done' is the only signal available... Give Claude something
that produces a pass or fail, and the loop closes on its own." This is
exactly why this module's lab uses a real, running test suite as its stop
condition rather than the model's own judgment -- it's not a curriculum
simplification, it's the documented reason real coding agents work the way
they do.

### Context management is the primary constraint

Current Claude Code guidance is explicit that "Claude's context window fills
up fast, and performance degrades as it fills" -- every file read and every
command's output consumes it, and a single debugging session can burn tens
of thousands of tokens. This is Module 05's context-engineering material
(compaction, budgeting, avoiding irrelevant accumulation), now identified as
the *primary* lever real coding-agent tooling gives users to manage (clearing
context between unrelated tasks, scoping investigations, using subagents for
research so exploration doesn't pollute the main task's context -- Module 12's
supervisor-worker pattern, applied to keep a coding agent's main loop
focused).

### What this module's lab deliberately leaves out

A production terminal coding agent adds, beyond this module's scope:
permission modes and sandboxing configurable per-command (lesson 01's
allowlist, made adjustable rather than fixed), checkpointing and rewind
(closer to Module 07's checkpoint/resume, applied to file edits specifically),
and multi-file/multi-step planning for larger tasks (Module 08). This
module's lab is deliberately the smallest complete version of the core loop,
not a full terminal coding agent.

## Deeper: verification changes what you can trust unattended

The practical consequence of "give it a check it can run" is trust: a task
with a reliable mechanical check can be run unattended and its result
believed; a task without one requires a human to eyeball the result every
time. This is why Module 16 (Evaluation) revisits "how do you know an agent
actually succeeded" as a whole module -- coding agents are the clearest
possible case of that question, because the answer can be a simple exit
code instead of an open-ended judgment.

## When not to use this

The explore-plan-code-commit structure is overhead for a one-line, obviously
scoped change (the same current guidance says exactly this: "if you could
describe the diff in one sentence, skip the plan") -- match the process
weight to the task's actual uncertainty, the same principle Module 08
lesson 05 applied to workflow-vs-agent generally.

## Common mistakes

- Skipping the "explore" phase for a task that turns out to touch code you
  don't actually understand yet, producing a plausible-looking fix that
  solves the wrong problem.
- Letting context accumulate indefinitely across unrelated tasks in one
  session instead of resetting between them, degrading later steps'
  performance for no benefit to the current task.
- Assuming a terminal coding agent's polish (checkpointing, permission
  modes, planning UI) is separate magic, rather than recognizing it as the
  same loop, sandbox, and verification-check ideas this module built,
  extended and made configurable.

## Key takeaways

- Real terminal coding agents structure work as explore -> plan -> code -> commit specifically to avoid solving the wrong problem.
- A runnable check (tests, build, lint) is what lets an agent's loop close on itself instead of requiring a human to judge "looks done."
- Context-window management is treated as the primary lever for coding-agent effectiveness, not an afterthought -- Module 05's material, now load-bearing.

## Lab

[`labs/01-fix-the-failing-test/`](../labs/01-fix-the-failing-test/README.md)
