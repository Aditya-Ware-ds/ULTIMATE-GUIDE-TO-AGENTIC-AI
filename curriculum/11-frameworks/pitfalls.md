# Module 11 pitfalls

## Trusting a tutorial's code sample over the installed package

Building this module surfaced multiple cases where search results and even
recent-looking tutorials described an API that didn't match the actually
installed package version: `mcp.server.fastmcp.FastMCP` (Module 10; the
current class is `mcp.server.MCPServer`), `langgraph.prebuilt.create_react_agent`
(now deprecated in favor of `langchain.agents.create_agent`), and an
assumed `ChatAgent` class name for Microsoft Agent Framework (the actual
class is `Agent`). In a field moving this fast, install the package and run
`dir(...)`/`inspect.signature(...)` on the actual objects before writing
code against them -- don't trust a single written source, however
authoritative it looks, per Ground Rule 1.

## Assuming every framework's tool-calling loop looks like Module 03/04's

Most frameworks in this module do follow the "model returns a structured
tool-call object, executor dispatches it, result fed back" shape you built
by hand -- but CrewAI's `BaseLLM.call()` doesn't: it hands the LLM
implementation `available_functions` directly and expects it to decide
whether to invoke them. Writing a CrewAI fake model that tries to mimic the
other frameworks' pattern (return a structured "I want to call X" signal for
an external executor to interpret) simply won't be called the way you expect
-- read each framework's actual extension point rather than assuming they're
all the same shape underneath.

## Missing a required mixin with no error message

Microsoft Agent Framework's `FunctionInvocationLayer` mixin is required for
a custom chat client to support tool calling -- omitting it produces a
logged warning ("does not support function invoking") and then a *silently
wrong* result (empty final answer), not an exception at the point of the
actual mistake. When a framework produces an unexpectedly empty or
placeholder-looking result with no traceback, check for exactly this class
of issue: a missing capability declaration or mixin, not a bug in your own
tool logic.

## Testing the wrong layer when a framework needs a real ToolContext

Both the OpenAI Agents SDK and the Claude Agent SDK wrap tool logic in a
handler that needs the framework's own internal context object to run
correctly (`ToolContext`, an MCP tool-call context) -- calling
`some_tool.on_invoke_tool(None, ...)` directly, expecting it to work like a
plain function, produces a confusing `AttributeError` deep in framework
internals rather than a clean test result. The fix used throughout this
module: keep the actual business logic (the arithmetic evaluator) in a
separate plain function, and only exercise the framework-wrapped version
through the framework's own real call path (or not at all, for logic-only
unit tests).

## Assuming "installed successfully" means "compatible with everything else"

Several of these frameworks have large, fast-moving dependency trees that
can directly conflict with this project's own dependencies (Microsoft Agent
Framework requires `mcp<2`; this project requires `mcp>=2.0.0`, per Module
10). Attempting to add all 9 frameworks as persistent project dependencies
made `uv sync` fail outright for the *entire* project, not just the
conflicting framework -- which is why this module uses `uv run --with
<package>` ephemeral overlays instead of a shared, persistent dependency set.
If you extend this pattern to a real multi-framework project of your own,
expect the same class of conflict and plan for isolated environments (one
per framework, or even one per project) rather than one shared one.
