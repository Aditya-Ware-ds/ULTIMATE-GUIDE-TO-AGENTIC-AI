# The agent loop

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~1 hour

## Learning objectives

- Define an "agent" precisely: a loop, not a single call.
- Trace the observe -> think -> act cycle through a concrete multi-step example.
- Explain how Module 03's `run_tool_loop` already was a (simplified) agent loop.

## Intuition

A single tool-calling exchange (Module 03) answers one question with at most a
handful of tool calls before the model settles on a final answer. An **agent**
is what you get when you let that process repeat: at each step, the model
observes the current state of the world (the conversation so far, including any
tool results), thinks about what to do next, and acts (calls a tool, or decides
it's done and produces a final answer). The loop keeps going until some stopping
condition is met (lesson 02). This is the same shape whether the task takes one
step or fifty.

## The concept

### Observe -> think -> act, made explicit

```
1. OBSERVE: what's in the conversation so far? (system prompt, history, last tool result)
2. THINK:   call the model with the current messages
3. ACT:     if the model's response has tool calls, dispatch them (observe their results next loop)
            if the model's response is plain text, that's the final answer -- stop
```

Compare this to Module 03's `run_tool_loop`:

```python
for _ in range(max_steps):
    response = await client.complete(messages, tools=TOOL_DEFINITIONS)  # THINK
    if not response.message.tool_calls:
        return response.message.content or ""  # ACT: done
    messages.append(response.message)
    for tool_call in response.message.tool_calls:
        result = dispatch(tool_call, TOOL_REGISTRY)  # ACT: tool call
        messages.append(Message(role=Role.TOOL, tool_result=result))  # OBSERVE (next loop)
```

You already built this. This module's job is to make you see it as the general
pattern it is, and extend it with more deliberate stopping logic (lesson 02) and
explicit reasoning (lesson 03, ReAct).

### Why this generalizes beyond tool calling

The exact same loop shape underlies far more complex agents later in this
curriculum: a coding agent (Module 13) observes a failing test, thinks about
what code change might fix it, acts by editing a file and re-running the test --
same three steps, just with richer "observe" (file contents, test output) and
"act" (file edits, shell commands via `shared/sandbox/`) than a
calculator/weather tool.

## Deeper: an agent loop is a state machine with exactly one interesting state transition

At its core, the loop has one meaningful branch: "does the model want to act
again, or is it done?" Everything else (memory, planning, multi-agent handoffs
in later modules) is elaboration on top of this one branch -- richer ways to
decide what "observe" includes, richer ways to decide what "act" can do, and
richer ways to decide when to stop. Understanding this keeps later, more
complex patterns from feeling like unrelated new ideas -- they're this same loop
with more sophisticated pieces plugged in.

## When not to use this

Don't build an agent loop for a task that's really a fixed, known sequence of
steps -- Module 08 covers exactly this distinction ("workflow vs. agent"). If you
always know in advance which 3 API calls need to happen in which order, a plain
function calling them in sequence is simpler, cheaper, and more predictable than
looping a model through deciding that same fixed sequence for itself.

## Common mistakes

- Treating "wrote a while loop calling the model" as automatically "built an
  agent" without a real stopping condition -- lesson 02 exists because this is
  exactly where things go wrong.
- Forgetting that "observe" includes *everything* in the conversation so far,
  not just the most recent tool result -- Module 05 (context engineering) covers
  what happens when that "everything" grows unmanageably large.
- Conflating the agent loop itself with the ReAct *prompting pattern* (lesson
  03) -- ReAct is one way to structure what happens inside "think"; the loop
  itself is more general than any one prompting strategy.

## Key takeaways

- An agent is a loop: observe (conversation state) -> think (call the model) -> act (tool call, or stop with a final answer).
- Module 03's tool-calling loop already had this shape -- this module makes it explicit and extends it.
- The same loop underlies simple tool-use agents and far more complex agents later in this curriculum; complexity comes from richer observe/act, not a different core loop.

## Lab

[`labs/01-react-agent/`](../labs/01-react-agent/README.md)
