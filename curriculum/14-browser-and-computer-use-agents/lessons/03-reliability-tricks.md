# Reliability tricks for browser and computer-use agents

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~30 minutes

## Learning objectives

- Explain why fixed `sleep()` calls are an unreliable way to wait for page state to change.
- Apply explicit wait conditions and retry-on-ambiguous-element as concrete reliability techniques.
- Recognize that this module's step budget and error-surfacing patterns are Module 04's stopping-condition discipline, applied to a flakier environment.

## Intuition

Browser and computer-use agents fail more often than the tool-calling agents
built earlier in this curriculum, for a structural reason: the environment
they act on can change out from under them for reasons that have nothing to
do with whether the agent's *reasoning* was correct -- a page that's still
loading, an animation mid-transition, or an element that only exists after
an asynchronous request resolves. Reliability techniques here are mostly
about not mistaking "the environment wasn't ready yet" for "the task
failed."

## The concept

### Fixed sleeps are a guess, not a condition

```python
# Fragile: guesses how long loading takes
session.click("#load-more")
time.sleep(2)
results = session.get_text("#results")
```

A fixed sleep is either too short (the page genuinely needed 3 seconds,
this run) or wastes time (it needed 200ms, every single run). The reliable
version waits for an actual, checkable condition:

```python
# Reliable: waits for the specific condition that matters
session.click("#load-more")
session.wait_for_selector("#results", state="visible")
results = session.get_text("#results")
```

Playwright's own APIs (`wait_for_selector`, auto-waiting built into
`click`/`fill`) are built around this same idea by default -- most of
Playwright's actions already wait for their target element to be
actionable before proceeding, which is a large part of why DOM-based
automation (lesson 01) is more reliable than naive pixel-coordinate
scripting to begin with.

### Retry on ambiguous or transient failures, not on every failure

If a selector matches zero elements because the page hasn't finished
loading yet, a short bounded retry can recover cleanly. If a selector
matches zero elements because the task's premise was wrong (the button was
renamed, or never existed), retrying does nothing but waste steps. The
distinction matters: retry a fixed, small number of times for *transient*
failures (an explicit wait timeout), and surface everything else as a real
tool error immediately -- exactly like Module 03's tool-error-handling
lesson: not every failure deserves a retry, and retrying a permanent failure
just delays returning useful information.

### A narrow action vocabulary is itself a reliability technique

Lesson 01's small, fixed set of actions (`goto`/`click`/`get_text`) isn't
just a security boundary -- it's also a reliability one. A generic
"execute this Playwright code" tool gives the model far more ways to
construct a subtly broken interaction (a bad selector, a race condition
in hand-written async code) than three narrow, well-tested primitives can.

### Step budgets still apply, and so does explicit failure

Nothing about a flakier environment changes Module 04's stopping-condition
discipline: `max_steps` still bounds the loop, and exhausting it should say
so plainly rather than returning whatever partial state the last action
left behind as if it were a complete answer.

## Deeper: browser/computer-use agents make Module 16's evaluation harder, not easier

A flaky environment means the same agent, given the same task, can succeed
on one run and fail on another for reasons unrelated to its reasoning
quality -- which is exactly why Module 16 (Evaluation) treats environment
flakiness as a real confound to control for, not just agent quality. A
result you can't reproduce isn't evidence of anything yet.

## When not to use this

Don't add retry logic to a tool call whose failure is deterministic and
task-relevant (e.g. `goto` rejecting a URL that's genuinely not on the
allowlist, lesson 01) -- retrying that just delays surfacing a real,
non-transient problem.

## Common mistakes

- Sprinkling `time.sleep()` calls tuned to "whatever worked once locally,"
  which becomes flaky again the moment the page's actual timing shifts.
- Retrying indefinitely on any failure, turning a fast, clear error into a
  slow, unclear timeout.
- Widening the action vocabulary "to be safe" (adding a general
  code-execution escape hatch) instead of adding the one or two specific
  actions a task actually needs.

## Key takeaways

- Wait for explicit, checkable conditions, never a fixed sleep duration -- Playwright's own APIs default to this.
- Retry only transient, ambiguous failures a small bounded number of times; surface everything else as a real error immediately.
- A narrow action vocabulary reduces both security exposure (lesson 01) and the surface area for reliability bugs.

## Lab

[`labs/01-browser-task-agent/`](../labs/01-browser-task-agent/README.md)
