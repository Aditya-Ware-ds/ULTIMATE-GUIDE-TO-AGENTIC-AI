# The ReAct pattern

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~1 hour

## Learning objectives

- Explain what ReAct adds on top of a plain tool-calling loop.
- Implement a ReAct-style agent that interleaves explicit reasoning with tool calls.
- Explain why making reasoning explicit tends to improve multi-hop task performance and debuggability.

## Intuition

ReAct ("**Rea**soning and **Act**ing," Yao et al., 2022) is a prompting pattern
where the model is asked to explicitly narrate its reasoning *before* each
action, rather than jumping straight to a tool call. Instead of just calling
`search("capital of France")`, a ReAct-style step looks like: "I need to find
the capital of France first, then find its population. Let me search for the
capital." -- then the tool call. This extra narration isn't decoration: writing
out the reasoning step by step measurably helps the model actually follow a
more careful multi-hop plan, and it gives *you* a debuggable trace of why the
agent did what it did.

## The concept

### The ReAct loop shape

```
Thought: I need to find the capital of France, then its population.
Action: search("capital of France")
Observation: Paris is the capital of France.
Thought: Now I need the population of Paris.
Action: search("population of Paris")
Observation: Paris has a population of about 2.1 million.
Thought: I have both pieces of information now.
Final Answer: The capital of France, Paris, has a population of about 2.1 million.
```

Each `Thought` is reasoning text, each `Action` is a tool call, each
`Observation` is that tool's result fed back in. The loop is structurally
identical to Module 04 lesson 01's observe-think-act cycle -- ReAct just makes
the "think" step *explicit and visible* as reasoning text, instead of an
opaque decision the model makes silently before emitting a tool call.

### Implementing it with this repo's client

With current tool-calling APIs, you don't need a special parser for
`Thought:`/`Action:` text -- the model can produce reasoning as regular text
content *alongside* a tool call in the same response (most providers support
both `content` text and `tool_calls` in one message), or you can prompt it to
put reasoning first, then call a tool in the same turn:

```python
system_prompt = """You solve multi-hop questions using the search tool.
Before each tool call, briefly explain your reasoning in one sentence.
When you have enough information, give a final answer with no further tool calls."""
```

The agent loop itself doesn't change from Module 04 lesson 01/02 -- what
changes is the system prompt asking for visible reasoning, and (for your own
debugging) logging `response.message.content` even on steps that also contain
tool calls, so you can see the reasoning trace, not just the actions.

## Deeper: why explicit reasoning helps, and where it stops helping

Making reasoning explicit tends to help most on genuinely multi-step problems
where the *plan* itself is non-obvious (which of several search results
actually answers the question; what order sub-questions need to be resolved
in). It helps least on simple single-step lookups, where the "reasoning" is
trivial and just adds tokens (cost, latency) with no accuracy benefit -- the
same trade-off Module 01 lesson 05 covered for reasoning models generally.
ReAct is a lightweight, prompt-level version of that same idea, usable with any
model, not just ones with a dedicated reasoning mode.

## When not to use this

Don't force a ReAct-style "always narrate reasoning" pattern onto single-step,
obvious tool calls -- it adds cost and latency for no benefit. Use it where the
task genuinely benefits from an explicit multi-step plan, which this module's
"multi-hop question" framing is specifically chosen to demonstrate.

## Common mistakes

- Treating ReAct's visible reasoning as *proof* the model's final answer is
  correct -- fluent, plausible-looking reasoning and a correct answer are not
  the same thing (Module 01 lesson 05 makes this point about reasoning models
  generally; it applies here too).
- Forgetting to actually use the reasoning trace for anything (debugging,
  logging) -- if you're not going to look at it, you're paying its token cost
  for nothing.
- Confusing the ReAct *pattern* (a prompting/loop-structuring technique) with a
  specific framework's implementation of it -- Module 11 will show you several
  frameworks that have built-in ReAct-style agent constructors; this lesson is
  about understanding what they're doing underneath.

## Key takeaways

- ReAct interleaves explicit reasoning ("Thought") with tool calls ("Action") and their results ("Observation"), inside the same observe-think-act loop from lesson 01.
- Explicit reasoning tends to help most on genuinely multi-step, non-obvious tasks, and least on simple single-step lookups.
- The technique is prompt-level and framework-agnostic -- Module 11's frameworks build convenience around it, not a fundamentally different mechanism.

## Lab

[`labs/01-react-agent/`](../labs/01-react-agent/README.md)
