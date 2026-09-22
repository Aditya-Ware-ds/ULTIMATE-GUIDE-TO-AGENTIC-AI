# Dispatch and execution

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~1 hour

## Learning objectives

- Build a tool registry that maps tool names to real Python functions.
- Dispatch a model's tool call to the right function and feed the result back correctly.
- Explain why tool arguments from a model must be treated as untrusted input.

## Intuition

Once the model decides to call a tool, *your code* is responsible for actually
running it -- the model only produces a name and a JSON arguments object; it has
no ability to execute anything itself. Dispatch is the translation layer between
"the model asked for `get_weather(city='Paris')`" and "actually call the Python
function `get_weather` with `city='Paris'`, and send the result back as a
`tool` message."

## The concept

### A minimal tool registry

```python
from collections.abc import Callable

TOOL_REGISTRY: dict[str, Callable[..., object]] = {
    "get_weather": get_weather,  # a real Python function
    "calculate": calculate,  # another real Python function
}
```

A registry is just a dict from tool name to callable. The tool *definitions*
(Module lesson 01, sent to the model) and the tool *registry* (used by your
code) describe the same tools but serve different audiences -- keep them in sync
deliberately, ideally generated from one source of truth in a real system.

### Dispatching a tool call

```python
from shared.llm.types import ToolCall, ToolResult


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    if tool_call.name not in registry:
        return ToolResult(
            tool_call_id=tool_call.id,
            content=f"Unknown tool: {tool_call.name}",
            is_error=True,
        )
    function = registry[tool_call.name]
    try:
        result = function(**tool_call.arguments)
        return ToolResult(tool_call_id=tool_call.id, content=str(result))
    except Exception as exc:  # noqa: BLE001 -- deliberately broad; see lesson 03
        return ToolResult(
            tool_call_id=tool_call.id,
            content=f"Tool execution failed: {exc}",
            is_error=True,
        )
```

Three things this does deliberately: it checks the tool name exists before
calling anything (a model can, and occasionally will, call a tool name that
doesn't exist or was misspelled), it calls the function with keyword arguments
unpacked from the model's JSON (`**tool_call.arguments`), and it catches *any*
exception rather than letting a bad argument crash your whole agent loop --
lesson 03 covers this broad exception handling in depth.

### Feeding the result back

```python
from shared.llm.types import Message, Role

messages.append(Message(role=Role.TOOL, tool_result=result))
# ... then call client.complete(messages) again so the model sees the result
```

The model doesn't know what happened when it "called" a tool until you send the
result back as a new message and make another API call. This is why a
tool-calling exchange is always at least two model calls: one where the model
decides to call a tool, and (at least) one more where it sees the result and
responds.

## Deeper: arguments from a model are untrusted input

`tool_call.arguments` came from the model's generation process (Module 01) --
which means it's just as capable of producing an unexpected, malformed, or
adversarial-looking value as any other model output. A model can output
`{"city": "'; DROP TABLE users; --"}` for a string field with zero malicious
intent of its own (or because of a prompt-injection attack, Module 18) -- your
tool implementation must validate and safely handle arguments exactly as
carefully as you would handle raw user input from an HTTP request. `**tool_call.arguments`
unpacked directly into a function that does something sensitive (a database
query, a shell command) without validation is a real vulnerability class, not a
hypothetical one -- Module 18 covers this systematically.

## When not to use this

Don't build a generic "eval this Python expression the model wrote" dispatch
mechanism as a shortcut instead of well-defined tools with real schemas --
that's arbitrary code execution with extra steps, and belongs (if you need it at
all) behind `shared/sandbox/`'s isolation, covered properly in Module 13.

## Common mistakes

- Not checking whether `tool_call.name` exists in the registry before calling it
  -- an `IndexError`/`KeyError` there crashes your loop instead of producing a
  recoverable error the model can react to.
- Passing `tool_call.arguments` straight into a function that performs a
  sensitive operation without validating types, ranges, or content first.
- Forgetting to set `tool_call_id` correctly on the `ToolResult` -- some
  providers require it to match the exact call it's responding to, especially
  when the model made multiple tool calls in one turn.

## Key takeaways

- A tool registry maps names to real callables; dispatch translates a model's tool call into an actual function call.
- Always check the tool exists and catch execution errors before they crash the loop -- return them as a `ToolResult` with `is_error=True` instead.
- Model-produced tool arguments are untrusted input, exactly like data from an HTTP request -- validate before using them for anything sensitive.

## Lab

[`labs/01-tool-calling-loop/`](../labs/01-tool-calling-loop/README.md)
