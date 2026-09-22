# Trajectory evals and current benchmarks

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~40 minutes

## Learning objectives

- Distinguish outcome evals (lesson 01) from trajectory evals (how an agent got there).
- Explain what SWE-bench, GAIA, tau-bench, and other current public agent benchmarks each actually measure.
- Choose an appropriate benchmark, or build a custom eval, for a given agent's actual task.

## Intuition

Lesson 01's golden-dataset eval checks the *final answer*. Two agents can
reach the same correct final answer through very different paths -- one
that called exactly the tools it needed, and one that flailed through
several wrong tool calls before stumbling onto the right one. Both score
identically on an outcome eval. A **trajectory eval** looks at the sequence
of steps itself, not just where it ended up.

## The concept

### What a trajectory eval checks

Given a full agent run (the message history Module 04's loop accumulates,
or Module 07's checkpoint state), a trajectory eval can check things an
outcome eval can't see at all:

- Did it call the *right* tools, in a *reasonable* order, without
  redundant or contradictory calls (Module 12 lesson 02's "duplicated
  work" failure mode is exactly what a trajectory eval catches)?
- Did it stay within an expected step budget, or barely scrape by right at
  the limit (a signal the task is harder than the budget assumes, even
  though it technically succeeded)?
- Did it recover cleanly from a tool error (Module 03's error-handling
  discipline), or get stuck repeating the same failing call?

```python
def check_trajectory(messages: list[Message], expected_tools: set[str]) -> dict:
    called_tools = {tc.name for m in messages for tc in m.tool_calls}
    return {
        "used_expected_tools": expected_tools.issubset(called_tools),
        "unexpected_tools": called_tools - expected_tools,
        "tool_call_count": sum(len(m.tool_calls) for m in messages),
    }
```

### Why trajectory evals matter even when the outcome eval passes

An agent that reaches the right answer by luck, or by an inefficient path
that happens to work this time, is a bigger production risk than one whose
trajectory shows disciplined, minimal, correct tool use -- the lucky path
is far more likely to fail on a slightly different input. Trajectory evals
catch this risk before it shows up as a production outage.

### Regression suites

A regression suite combines lesson 01's golden dataset with trajectory
checks and runs both automatically (e.g. in CI) on every change -- the same
idea as this repo's own `make test`, applied to agent *behavior* quality,
not just code correctness. A regression suite's real value is catching a
silent quality drop from a seemingly unrelated change (a tool description
edit, a system prompt tweak, a model upgrade) before it reaches production.

### Current public agent benchmarks (verified 2026-09-22)

- **SWE-bench** (and its **Verified** subset): given a real GitHub issue and
  its repository, produce a patch that makes the repository's hidden test
  suite pass -- a large-scale, realistic coding-agent benchmark, actively
  maintained with current leaderboards.
- **GAIA**: over 450 real-world questions across three difficulty levels,
  requiring tool use, web search, and multi-step reasoning to reach an
  unambiguous answer -- explicitly designed so level-1 questions are
  "breakable by very good LLMs" while level-3 requires a real capability
  jump.
- **tau-bench**: evaluates an agent's ability to follow domain-specific
  policies while interacting with simulated users and tools in realistic
  business scenarios (e.g. airline or retail customer service) -- a
  benchmark for policy-following and multi-turn tool use, not just raw
  task completion.
- **BrowseComp, WebArena**: benchmarks for web-browsing and browser-task
  agents (Module 14) -- multi-step information-seeking and realistic
  website-interaction tasks, respectively.
- **OSWorld**: a benchmark for general computer-use agents (Module 14
  lesson 02) operating a real desktop OS environment across varied
  applications, not just a browser.
- **Terminal-Bench**: evaluates agents operating in a terminal environment
  on realistic command-line tasks -- closer to Module 13's coding-agent
  material than SWE-bench's patch-focused format.

Verify current leaderboard standings and exact task counts before quoting
specific numbers in your own work -- this field's benchmarks are actively
maintained and their leaderboards change; what's stable is *what each one
measures*, which is what's summarized above.

## Deeper: choosing a benchmark vs. building a custom eval

Public benchmarks are valuable for comparing against the broader field, but
they rarely match your actual task's specifics. The realistic path for most
production agents is: use a public benchmark (if one fits your domain) for
external comparison, and build a custom golden-dataset + trajectory eval
(lessons 01-03) for your actual task -- the two serve different purposes and
aren't a substitute for each other.

## When not to use this

Don't build full trajectory-eval infrastructure for a simple, single-tool-call
agent where the outcome eval already captures everything that could go
wrong -- trajectory analysis earns its complexity for multi-step, multi-tool
agents where the path genuinely matters.

## Common mistakes

- Reporting only an outcome-eval accuracy number and missing that the
  agent's trajectories are quietly getting less efficient (more retries,
  more redundant calls) even while accuracy holds steady.
- Choosing a public benchmark that doesn't match your actual task's
  domain, then treating a good score on it as evidence your specific agent
  is production-ready.
- Quoting a specific benchmark leaderboard number without a fresh
  verification date -- these boards move, and a memorized number from
  training data can already be stale.

## Key takeaways

- Trajectory evals check *how* an agent reached an answer (tool choice, ordering, efficiency, error recovery), not just whether the final answer was correct.
- A regression suite combines outcome and trajectory evals and runs automatically on every change, the same discipline as this repo's own test suite applied to agent behavior.
- Public benchmarks (SWE-bench, GAIA, tau-bench, BrowseComp, WebArena, OSWorld, Terminal-Bench) each measure a different, specific capability -- match the benchmark to the task, and re-verify current standings before quoting numbers.

## Lab

[`labs/01-eval-harness-and-judge/`](../labs/01-eval-harness-and-judge/README.md)
