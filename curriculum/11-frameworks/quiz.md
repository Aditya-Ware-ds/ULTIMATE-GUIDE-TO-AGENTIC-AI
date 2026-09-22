# Module 11 quiz

**1. What do all 9 frameworks in this module have in common, underneath their different syntax?**

<details><summary>Answer</summary>

They all implement some version of the same observe-think-act agent loop
(Module 04) with a tool abstraction (Module 03) -- the differences are in
abstraction level, control-flow explicitness, and how much they hide versus
expose, not in solving a fundamentally different problem.

</details>

**2. Why is `langgraph.prebuilt.create_react_agent` the wrong function to reach for in current LangGraph code?**

<details><summary>Answer</summary>

It's deprecated in favor of `create_agent` from the `langchain` package,
verified directly against the installed 2026 version -- several tutorials
from earlier in 2026 still show the old function, which is exactly why
verifying against the installed package (not just search results) mattered.

</details>

**3. Why couldn't `GenericFakeChatModel` be used to test the LangGraph lab, requiring a custom `BaseChatModel` subclass instead?**

<details><summary>Answer</summary>

It's built for generic text-response testing, not for scripting specific
tool calls with specific arguments -- a custom subclass overriding
`_generate` (and `bind_tools`, which raises `NotImplementedError` by default)
gives full control over exactly what the fake model returns at each step.

</details>

**4. What's structurally different about how CrewAI's `BaseLLM.call()` handles tools, compared to every other framework in this module?**

<details><summary>Answer</summary>

`call()` receives `available_functions` directly and is expected to decide
whether and how to invoke them itself, returning the final text in one
call -- there's no separate structured "tool call" object handed back to an
external executor to interpret, unlike every other framework here.

</details>

**5. What happens if you forget the `FunctionInvocationLayer` mixin when building a custom chat client for Microsoft Agent Framework?**

<details><summary>Answer</summary>

No exception is raised -- the agent logs a warning and silently never
dispatches tool calls back to your client, producing an empty or wrong final
answer instead of a clear error. This is the single easiest mistake to make
in this module, precisely because it fails silently.

</details>

**6. Which two frameworks in this module had the cleanest, most purpose-built offline testing support, and what did they provide?**

<details><summary>Answer</summary>

Pydantic AI (`TestModel` for auto-calling tools, `FunctionModel` for fully
scripted responses) and LlamaIndex Workflows (`MockFunctionCallingLLM` with a
scripted `response_generator`) -- both are official, documented testing
utilities built specifically for this purpose.

</details>

**7. Why can't the Claude Agent SDK's reference agent be tested fully offline, unlike the other 8 frameworks?**

<details><summary>Answer</summary>

It's not a "bring your own model" framework -- it's a thin wrapper around the
actual Claude Code agent loop, which always calls a real Claude model via the
bundled CLI. There's no `Model`/`BaseLlm`-style protocol to substitute a
scripted fake response, verified by inspecting `ClaudeAgentOptions`'s full
field list and `query()`'s signature directly.

</details>

**8. Google ADK's `InMemoryRunner.run_debug(...)` is explicitly documented as being for what purpose?**

<details><summary>Answer</summary>

Quick agent experimentation and testing -- its own docstring says it's
designed for developers who want to test agents "without dealing with
session management, content formatting, or event streaming," and explicitly
warns it's for debugging, not production use.

</details>

**9. Why does this module conclude that "how do I test this framework offline" is a legitimate framework-evaluation criterion, not an afterthought?**

<details><summary>Answer</summary>

Across all 9 builds, frameworks with official, purpose-built testing
mechanisms took less time and produced fewer surprises than ones requiring a
hand-rolled fake client -- and one hand-rolled case (Microsoft Agent
Framework's missing mixin) produced a silently wrong answer, the worst kind
of framework surprise. This predicted real development friction directly.

</details>

**10. Why doesn't picking a framework now lock you into re-learning agent concepts if you switch later?**

<details><summary>Answer</summary>

Because you built the underlying agent loop, tool dispatch, and stopping
conditions by hand in Modules 03-09 -- switching frameworks later means
learning new syntax and abstractions for concepts you already understand
deeply, not re-learning the concepts themselves.

</details>
