# Module 04 quiz

**1. What makes a loop of model calls "an agent" rather than just "a loop"?**

<details><summary>Answer</summary>

The loop implements observe -> think -> act, repeating until a stopping
condition is met, where the model itself decides what action to take at each
step based on the current state -- as opposed to a fixed, predetermined
sequence of calls.

</details>

**2. How does Module 03's `run_tool_loop` relate to this module's general agent loop?**

<details><summary>Answer</summary>

It already had the same structure (observe-think-act, repeating on tool calls,
stopping on plain text) -- it was a simplified special case. This module makes
the pattern explicit and adds more deliberate stopping conditions and reasoning.

</details>

**3. Name three stopping conditions an agent loop might use besides "the model stopped calling tools."**

<details><summary>Answer</summary>

Any three of: a max-steps ceiling, an explicit "finish"/"submit_answer" tool
the model must call, a token/cost budget, or an external interrupt (human
approval gate, cancellation).

</details>

**4. Why is a max-steps limit described as a safety requirement rather than an optimization?**

<details><summary>Answer</summary>

Without it, a single bad run has unbounded cost, unbounded wall-clock time, and
(if tools have real side effects) unbounded real-world actions. A step limit
converts unbounded risk into bounded, known risk -- this connects directly to
Ground Rule 8's sandboxing requirement.

</details>

**5. What should a well-designed agent loop return when it hits `max_steps`, and what shouldn't it do?**

<details><summary>Answer</summary>

It should return a clear, distinguishable message (or otherwise signal
explicitly) that it stopped without a final answer. It should not raise an
unhandled exception, and it should not silently return an empty or
ambiguous-looking result that could be mistaken for a successful answer.

</details>

**6. What does ReAct add on top of the plain agent loop from lesson 01?**

<details><summary>Answer</summary>

It makes the "think" step's reasoning explicit and visible as narrated text
("Thought: ...") before each action, instead of an opaque decision baked
silently into the model's choice of tool call.

</details>

**7. Why does explicit reasoning tend to help most on multi-hop tasks and least on simple single-step lookups?**

<details><summary>Answer</summary>

Multi-hop tasks require a non-obvious plan (which order to resolve
sub-questions, which result to use next) that benefits from being worked out
explicitly. A single-step lookup has no real planning to do, so narrating
"reasoning" just adds tokens and latency with no accuracy benefit.

</details>

**8. Does a fluent, well-structured ReAct reasoning trace guarantee the final answer is correct?**

<details><summary>Answer</summary>

No. This is the same point made about reasoning models generally (Module 01,
lesson 05): plausible-looking reasoning and correct reasoning aren't the same
thing. A ReAct trace is useful for debugging and can improve accuracy, but it
isn't proof of correctness.

</details>

**9. In this module's lab, why does `search()` raise `ValueError` for an unknown query instead of returning an empty string?**

<details><summary>Answer</summary>

A raised, specific error becomes a recoverable `is_error=True` `ToolResult` via
`dispatch()` (Module 03's pattern) that the model can see and react to. A
silent empty string looks like a (wrong) successful lookup, giving the model no
signal that anything went wrong.

</details>

**10. When would a fixed, hand-written sequence of function calls be a better design than an agent loop deciding each step?**

<details><summary>Answer</summary>

When you always know in advance exactly which steps need to happen and in what
order -- a workflow, not a genuinely adaptive task. Module 08 covers this
"workflow vs. agent" distinction directly; an agent loop adds cost, latency,
and unpredictability that isn't worth paying for a fixed sequence.

</details>
