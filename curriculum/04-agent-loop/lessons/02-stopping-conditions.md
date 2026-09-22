# Stopping conditions

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45 minutes

## Learning objectives

- Enumerate the ways an agent loop should be able to stop, beyond "the model produced text."
- Implement a max-steps budget that fails safely and informatively.
- Explain why an agent loop with no step budget is a production hazard, not just a theoretical concern.

## Intuition

A loop that only stops when the model "decides" to stop is trusting the model's
judgment about when it's done -- which is usually right, but not guaranteed. A
model can get stuck calling tools in an unproductive cycle, misjudge that it
needs more information when it already has enough, or (rarely) never naturally
converge on a final text response. Real agent loops need stopping conditions
that don't depend entirely on the model behaving well.

## The concept

### The stopping conditions worth having

1. **Natural completion** -- the model responds with no tool calls. This is the
   "happy path" every agent loop has (Module 03's `run_tool_loop` already has
   this one).
2. **Max steps** -- a hard ceiling on how many loop iterations are allowed,
   regardless of what the model wants. This is the safety net for every other
   failure mode: infinite tool-calling loops, models that never converge,
   runaway cost.
3. **Explicit "done" signal** -- for more complex agents, sometimes you give the
   model an explicit `finish`/`submit_answer` tool it must call to end the loop,
   rather than inferring "done" from the absence of tool calls. This makes
   "the agent is finished" an unambiguous, inspectable event rather than an
   inference.
4. **Budget-based limits** -- stopping after a token or cost budget is exhausted,
   not just a step count (Module 19 revisits this for production cost control).
5. **External interrupt** -- a human-in-the-loop approval gate or cancellation
   (Module 09) that can stop the loop regardless of the model's internal state.

### Implementing max-steps so it fails safely

```python
async def run_agent(client, system_prompt, user_input, max_steps: int = 10) -> str:
    messages = [
        Message(role=Role.SYSTEM, content=system_prompt),
        Message(role=Role.USER, content=user_input),
    ]
    for step in range(max_steps):
        response = await client.complete(messages, tools=TOOL_DEFINITIONS)
        if not response.message.tool_calls:
            return response.message.content or ""
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            result = dispatch(tool_call, TOOL_REGISTRY)
            messages.append(Message(role=Role.TOOL, tool_result=result))
    return f"Stopped after {max_steps} steps without reaching a final answer."
```

Notice this *returns* a clear message on hitting the limit rather than raising
an unhandled exception, and rather than silently returning an empty string that
looks like a (wrong) successful answer. Whoever calls this function needs to be
able to tell "the agent answered" from "the agent gave up" -- Module 03's
pitfalls.md flagged this same issue.

## Deeper: why max-steps is a safety requirement, not an optimization

Without a step limit, a single bad run can consume unbounded tokens (cost),
unbounded wall-clock time (a user waiting indefinitely), and in the worst case
(a tool that has side effects, like sending an email or writing a file) take an
unbounded number of real-world actions. A step limit turns "unbounded risk" into
"bounded, known risk" -- this is precisely why Ground Rule 8 ("never let an
agent execute code or shell commands outside a sandbox") and step limits are
both non-negotiable defaults, not tunable-later nice-to-haves.

## When not to use this

Don't set a step limit so low that legitimate multi-hop tasks can't complete --
a limit that's too aggressive just turns "runs forever" into "fails on anything
non-trivial." Size the limit to the hardest task you actually expect (with
margin), not to the easiest one.

## Common mistakes

- No step limit at all -- "it worked in my testing" is not evidence it's safe in
  production, where inputs and model behavior vary far more than a handful of
  manual test runs.
- Setting a step limit but not testing what happens *at* the limit -- does your
  code raise, return silently, or return a clear message? (This module's lab
  tests this directly, the same way Module 03's did.)
- Relying solely on "the model will call a `finish` tool" without also having a
  max-steps fallback -- an explicit done-signal is a good addition, not a
  replacement for a hard ceiling.

## Key takeaways

- Natural completion, max-steps, explicit done-signals, budgets, and external interrupts are all legitimate stopping conditions -- most real agents need more than just the first one.
- A step limit should fail with a clear, distinguishable message, not silently or with an unhandled exception.
- An unbounded loop is a real safety and cost risk, not just a theoretical edge case -- this is why Ground Rule 8 exists.

## Lab

[`labs/01-react-agent/`](../labs/01-react-agent/README.md)
