# Workflow vs. agent

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45 minutes

## Learning objectives

- Define the distinction precisely: who controls the control flow, the model or your code.
- Apply a concrete decision test to a real task.
- Explain why defaulting to "agent" for everything is a common, costly mistake.

## Intuition

This distinction has been foreshadowed since Module 04, lesson 01 -- now it's
explicit. A **workflow** is a fixed sequence of steps your code controls; the
model (if involved at all) is called for specific sub-tasks (classification,
generation, extraction) but never decides *what happens next* or *in what
order*. An **agent** is a loop where the model itself decides which action to
take at each step, including whether to stop. Every pattern in this module
sits somewhere on that spectrum: a plain sequential pipeline is a pure
workflow; Module 04's ReAct loop is a pure agent; plan-and-execute and
orchestrator-workers are hybrids (the model decides *what* the steps/sub-tasks
are, but execution can be either fixed or itself agentic).

## The concept

### The decision test

Ask: **do you know, in advance, the fixed sequence of operations needed to
solve every instance of this task?**

- **Yes -> workflow.** Write the sequence directly in code. Call the model only
  for sub-tasks (e.g. "extract this field," "classify this request") where a
  fixed function can't do the job, but don't let the model decide *which*
  sub-tasks run or in what order.
- **No, it genuinely varies by input in ways you can't enumerate ahead of
  time -> agent.** Let the model decide the next action based on what it
  observes, within the stopping-condition discipline from Module 04.

### A worked example

*"Summarize this document, extract its key entities, and email the summary to
the document's owner."* -- if this is always exactly these three steps in this
order for every document, it's a **workflow**: summarize (one call) -> extract
entities (one call) -> send email (one function call, no model decision
involved in *whether* to send it). Wrapping this in an agent loop that
"decides" to do these three things, every time, in the same order, adds
latency, cost, and unpredictability for zero benefit -- the sequence was never
actually in question.

*"Investigate why this deployment failed and either fix it or escalate to a
human"* -- this is an **agent**: the right sequence of diagnostic steps
genuinely depends on what's actually wrong, which you can't enumerate for
every possible failure ahead of time.

### Hybrids are normal, not a cop-out

Most real production systems are neither purely one nor the other: a workflow
that calls an agent for one genuinely-variable sub-step, or an agent whose
individual steps are internally fixed workflows (e.g. Module 06's `dispatch`
function is a tiny fixed workflow -- check the tool name, call the function,
format the result -- living inside an otherwise agentic loop). The decision
test applies *per decision point*, not to an entire system as one monolithic
choice.

## Deeper: agents cost more and are less predictable, by design

An agent's entire value proposition is adapting to cases you didn't
anticipate -- which is exactly why it's harder to test exhaustively (Module 16),
more expensive (more model calls, less predictable how many), and less
debuggable (the sequence of actions isn't fixed, so "what will it do" isn't
always answerable in advance) than a workflow covering the same ground. This
isn't a flaw to fix; it's the trade-off you're accepting by choosing "agent."
Choosing it for a task a workflow would handle just as well means paying that
cost for nothing.

## When not to use this

This lesson's decision test is a starting heuristic, not an absolute rule --
some tasks are workflow-shaped 90% of the time with rare edge cases that need
agentic handling. In that situation, a workflow with an explicit "escalate to
an agent" branch for the rare case is often better than making the whole
system agentic just to cover a minority of instances.

## Common mistakes

- Defaulting to building an agent because it feels more sophisticated or
  future-proof, for a task whose steps are actually fixed and well-understood.
- Building a rigid workflow for a task whose steps genuinely vary by input,
  then bolting on special cases in code for every new variation instead of
  admitting the task needs agentic handling.
- Treating "workflow vs. agent" as a property of an entire system rather than
  a decision made at each individual decision point within it.

## Key takeaways

- The test: if you can enumerate the fixed sequence of steps for every instance of the task in advance, use a workflow; if it genuinely varies in ways you can't enumerate, use an agent.
- Most real systems are hybrids -- apply the test per decision point, not to a whole system at once.
- Agents trade predictability and cost for adaptability -- that trade-off should be a deliberate choice, not a default.

## Lab

[`labs/01-plan-vs-evaluate/`](../labs/01-plan-vs-evaluate/README.md)
