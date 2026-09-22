# Module 10 pitfalls

## Forgetting `if __name__ == "__main__": mcp.run()`

An `MCPServer` script that only defines `@mcp.tool()`-decorated functions and
never calls `mcp.run()` does nothing when executed -- the decorators register
tools on the `mcp` object, but nothing serves them over any transport. This
is easy to miss because the script *runs without error* (it just exits
immediately) -- there's no exception pointing you at the problem, just a
client that can't connect to anything.

## Confusing `result.content` with `result.structured_content`

`client.call_tool(...)`'s result carries the response two ways:
`result.content` (a list of content blocks, typically `TextContent` objects
with a `.text` string) and `result.structured_content` (the typed return
value, e.g. `{"result": 5.0}` for a function returning a `float`). Code that
does `result.content` expecting a plain string, or `result.structured_content`
expecting it to always exist (it may be `None` for tools with less
structured return types), will break in ways that are easy to misdiagnose as
"the tool call failed" when it actually succeeded and returned data in a
different shape than assumed.

## Testing against stale documentation for a protocol that just changed

This module's own build process ran directly into this: web search results
for the `mcp` Python package described APIs (`FastMCP` imported from
`mcp.server.fastmcp`, for instance) that don't match the actual installed
package (`MCPServer` imported from `mcp.server`, in the version verified for
this module). When a spec or SDK has recently undergone a major rework (this
one moved from a 1.x to 2.x line to support the 2026-07-28 spec), search
results and even official-looking tutorials can lag the current reality by
months. The reliable fix, demonstrated while building this module: install
the actual package and inspect it directly (`dir(SomeClass)`,
`inspect.signature(...)`) rather than trusting any single written source,
however authoritative it looks.

## A2A lab: allowing an invalid transition to silently "succeed"

If `start_work`/`provide_input`/`complete`/`fail` don't check the task's
current state before transitioning (or catch-and-ignore a mismatch instead of
raising), a task can end up in a state that doesn't reflect what actually
happened -- e.g. `complete()` called on a task that's still `SUBMITTED`
marks it done without any work ever having occurred. This lab's tests check
every invalid transition raises `ValueError` specifically because a silently
"successful" invalid transition is a correctness bug that's easy to miss in
casual testing (the call doesn't crash, so it "looks fine") but corrupts the
task's history as a record of what actually happened.

## Writing a `SKILL.md` description that restates the name instead of saying when to use it

`description: "A calculator skill"` passes the "not too short" check in this
module's lab but fails the actual point of a skill description (lesson 03's
discovery stage depends entirely on it). Compare to
`description: "Evaluate a basic arithmetic expression... Use this whenever
the user asks for a calculation..."` -- the second version tells the agent
*when* to activate the skill, which is the entire mechanism progressive
disclosure depends on. A mechanical length check (this lab's validator)
catches obvious placeholders; it can't verify the description is actually
useful -- that's still on you.
