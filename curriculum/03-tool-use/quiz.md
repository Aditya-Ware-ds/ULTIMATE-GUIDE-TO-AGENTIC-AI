# Module 03 quiz

**1. What two pieces of information does a `ToolDefinition` give the model, and which one matters most for disambiguating similar tools?**

<details><summary>Answer</summary>

A schema (JSON Schema for the arguments) and a natural-language description. The
description matters most for disambiguation -- it's where you say *when* to use
this tool versus a similarly-named or similarly-purposed one; the schema alone
doesn't convey intent.

</details>

**2. Why does a `required` list in a tool's parameter schema matter beyond documentation?**

<details><summary>Answer</summary>

It shapes what the model attempts to produce -- an unconstrained schema invites
the model to omit fields your code actually needs, causing preventable runtime
errors. Structuring the schema tightly (required fields, enums) narrows what the
model tries to generate before your code ever runs.

</details>

**3. What is a tool registry, and why is it kept separate from the tool definitions sent to the model?**

<details><summary>Answer</summary>

A registry is a dict mapping tool names to real Python callables -- it's your
code's view of the tools. Tool definitions (schema + description) are the
model's view. They describe the same tools for two different audiences and must
be kept in sync deliberately.

</details>

**4. Why should `dispatch()` check whether a tool name exists in the registry before calling it, instead of just trying and catching a `KeyError`?**

<details><summary>Answer</summary>

Either approach can work, but an explicit check makes the "unknown tool" case a
distinct, clearly-named failure path with its own message, rather than relying
on catching a generic `KeyError` that could also mean something else went wrong
inside dispatch itself. Explicit is more debuggable.

</details>

**5. Why must tool call arguments from a model be treated as untrusted input, even though the model isn't "attacking" you?**

<details><summary>Answer</summary>

The arguments come from the same generation process as any other model output --
they can be malformed, unexpected, or (via prompt injection, Module 18)
adversarial regardless of the model's own intent. Passing them unvalidated into
sensitive operations (a database query, a shell command) is a real vulnerability
class, the same as trusting raw HTTP request data.

</details>

**6. A tool call fails because the model passed a city name with a typo. Should your dispatch code raise an exception or return a `ToolResult`?**

<details><summary>Answer</summary>

Return a `ToolResult` with `is_error=True` and an actionable message. This is a
model-recoverable error -- feeding it back lets the model retry with a corrected
value on its next turn. Raising an exception would crash the whole loop over a
fixable problem.

</details>

**7. Give an example of an error that should NOT be silently converted into a `ToolResult(is_error=True)` and retried by the model.**

<details><summary>Answer</summary>

A genuine bug in your tool's own code (e.g. an unhandled type error from a
programming mistake, not from bad model input) shouldn't be treated as a normal
recoverable tool failure -- it should surface (log it, alert) so you actually
fix the bug, not get silently papered over as "the model will just try again."

</details>

**8. Why would you retry a tool call after a network timeout, but not after a `ValueError` from bad arguments?**

<details><summary>Answer</summary>

A network timeout is transient -- the same call might succeed on a retry with no
change. A `ValueError` from bad arguments will fail identically every time you
retry with the same arguments; what actually helps is reporting the error back
so the model (or a human) can supply different arguments.

</details>

**9. Why does this module's lab implement `calculate()` using `ast.parse()` and a restricted node walk instead of `eval()`?**

<details><summary>Answer</summary>

`eval()` on a model-produced string is arbitrary code execution -- a model
(or an attacker via prompt injection) could produce an expression that does
anything Python can do, not just arithmetic. The `ast`-based approach only
allows a small, explicitly safe set of operations (basic arithmetic), rejecting
everything else.

</details>

**10. In a multi-step tool-calling exchange, why must the assistant's tool-call message be appended to `messages` before the tool result message, rather than skipping straight to the result?**

<details><summary>Answer</summary>

Most current providers expect the conversation history to show the actual
sequence of events: the model's decision to call a tool, then the result of
that specific call. Without the assistant's tool-call message in history, the
tool result has no clear context for which call it's responding to, and some
providers will reject or mishandle the request.

</details>
