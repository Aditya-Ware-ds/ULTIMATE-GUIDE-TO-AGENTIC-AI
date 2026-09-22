# Module 10 quiz

**1. What are the three architectural roles in MCP, and what does each do?**

<details><summary>Answer</summary>

Host (the application the user interacts with, embeds clients), client (lives
in the host, maintains a 1:1 connection to one server, translates protocol
messages), and server (a separate process/service exposing tools, resources,
and prompts, with no knowledge of which host or model is calling it).

</details>

**2. What three kinds of capabilities can an MCP server expose?**

<details><summary>Answer</summary>

Tools (callable functions), resources (readable, URI-addressed data), and
prompts (reusable, parameterized prompt templates).

</details>

**3. Why does `mcp.tool()`'s auto-generated schema still depend on writing a good docstring?**

<details><summary>Answer</summary>

The docstring becomes the tool's description, which is what the model
actually reads to decide when and how to use the tool -- Module 03's lesson
that descriptions matter as much as schema structure applies just as much
here, auto-generation or not.

</details>

**4. Why is an in-process `Client(mcp_server_instance)` connection useful for tests, when real deployments typically use stdio or HTTP?**

<details><summary>Answer</summary>

It's fast and deterministic (no subprocess spawn, no network), while
exercising the exact same protocol behavior (`list_tools()`, `call_tool()`,
error handling) a real deployment would use -- the transport differs, the
protocol semantics don't.

</details>

**5. What does A2A standardize that MCP does not?**

<details><summary>Answer</summary>

A2A standardizes agent-to-agent task delegation -- one agent handing off
work to another, with a formal task lifecycle (including interrupted states
like "input-required"). MCP standardizes an agent calling a tool/service, not
agent-to-agent delegation.

</details>

**6. Name two terminal states and one interrupted (non-terminal, paused) state in A2A's task lifecycle.**

<details><summary>Answer</summary>

Terminal: any two of `completed`, `failed`, `canceled`, `rejected`.
Interrupted: `input-required` or `auth-required` -- the task pauses, awaiting
the client, rather than ending.

</details>

**7. What are the minimum required frontmatter fields for a `SKILL.md` file?**

<details><summary>Answer</summary>

`name` and `description`, at minimum.

</details>

**8. What is "progressive disclosure" in Agent Skills, and why does it matter for context budget (Module 05)?**

<details><summary>Answer</summary>

Agents load only every skill's name+description at startup (cheap, always in
context), and only load a specific skill's full instructions when a task
matches its description. This keeps many skills available without paying the
full context cost of all of them simultaneously -- directly connected to
Module 05's point about context being a managed budget.

</details>

**9. Given a task that needs "an agent to call a specific tool," "one agent to delegate work to another," and "reusable domain instructions loaded on demand," which protocol fits each?**

<details><summary>Answer</summary>

MCP for calling a tool; A2A for agent-to-agent delegation; Agent Skills for
reusable, on-demand domain instructions. All three are commonly used together
in a real system, not as alternatives to each other.

</details>

**10. Why would reinventing a custom "agent talks to agent" protocol from scratch, instead of using A2A, be a risky choice?**

<details><summary>Answer</summary>

Task-lifecycle semantics -- especially interrupted vs. terminal states, and
how a paused task resumes -- are easy to get subtly wrong when designed ad
hoc. A2A already standardizes this, the same way reinventing tool-calling
from scratch instead of using MCP risks missing edge cases MCP's spec already
addresses.

</details>
