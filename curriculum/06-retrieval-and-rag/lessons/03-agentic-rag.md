# Agentic RAG

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~45-60 minutes

## Learning objectives

- Distinguish naive RAG (always retrieve, then answer once) from agentic RAG (the model decides when and what to search, possibly multiple times).
- Implement retrieval as a tool call inside Module 04's agent loop.
- Know when naive RAG is actually the better (simpler, cheaper) choice.

## Intuition

**Naive RAG** is a fixed pipeline: embed the query, retrieve top-k chunks,
stuff them into the prompt, generate one answer. It's simple and works well
when a question can be answered from one retrieval pass. **Agentic RAG** treats
retrieval as a *tool* the model can call -- zero, one, or several times, with
follow-up queries informed by what it already found -- inside the agent loop
from Module 04. This matters for questions that naive RAG's single-shot
retrieval handles poorly: multi-hop questions (Module 04's ReAct example),
questions where the first search's results reveal that a *different* search
is actually needed, or questions where partial information needs a follow-up
lookup to complete.

## The concept

### Retrieval as a tool

```python
from shared.llm.types import ToolDefinition

SEARCH_DOCUMENTS = ToolDefinition(
    name="search_documents",
    description=(
        "Search the document collection for relevant passages. Use this whenever "
        "you need information to answer the user's question; call it again with "
        "a refined query if the first results aren't sufficient."
    ),
    parameters={
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
)
```

The tool's *description* matters exactly as much here as it did in Module 03 --
telling the model it's allowed (and expected) to call it again with a refined
query is what actually enables multi-step retrieval, rather than the model
assuming one search is all it gets.

### The loop is unchanged from Module 04

```python
async def run_agentic_rag(client, index, user_input: str, max_steps: int = 5) -> str:
    messages = [
        Message(
            role=Role.SYSTEM, content="Answer using search_documents. Cite which passage you used."
        ),
        Message(role=Role.USER, content=user_input),
    ]
    for _ in range(max_steps):
        response = await client.complete(messages, tools=[SEARCH_DOCUMENTS])
        if not response.message.tool_calls:
            return response.message.content or ""
        messages.append(response.message)
        for call in response.message.tool_calls:
            results = hybrid_search(call.arguments["query"], index)  # lesson 02
            messages.append(
                Message(
                    role=Role.TOOL,
                    tool_result=ToolResult(tool_call_id=call.id, content="\n---\n".join(results)),
                )
            )
    return f"Stopped after {max_steps} steps without reaching a final answer."
```

This is, structurally, the exact same loop as Module 04's `run_react_agent` and
Module 03's `run_tool_loop` -- the only new thing is that one of the tools
happens to be a retrieval call. This is a good example of the point made back
in Module 04, lesson 01: complexity in later modules mostly comes from richer
tools and observations plugged into the same loop, not a different loop shape.

## Deeper: agentic RAG costs more, and that cost needs to be justified

Every retrieval call inside the loop is an extra model call (Module 02's cost
lesson) plus the retrieval operation itself. Agentic RAG is strictly more
expensive than naive RAG for the same question, in both tokens and latency --
it's worth it specifically when questions in your actual use case need
multiple, dependent retrieval steps (measured, per Module 16, not assumed). A
system serving mostly single-fact lookups gains little from agentic RAG's extra
cost and complexity.

## When not to use this

Don't default to agentic RAG for a use case dominated by simple, single-hop
questions -- naive RAG (one retrieval, one generation) is cheaper, faster, and
easier to reason about, and is the right choice when it measurably performs as
well as the agentic version for your actual query distribution.

## Common mistakes

- Building agentic RAG without a tool description that tells the model it's
  allowed to search again -- without that permission being explicit, many
  models default to a single search attempt, undermining the entire point.
- Not capping `max_steps` on an agentic RAG loop -- the same stopping-condition
  discipline from Module 04 applies here; retrieval loops can also fail to
  converge.
- Assuming agentic RAG is strictly better than naive RAG -- it's better for
  multi-hop, exploratory retrieval needs specifically, and worse (more
  expensive, no accuracy benefit) for simple lookups. This is the same
  "workflow vs. agent" judgment call from Module 08, applied to retrieval.

## Key takeaways

- Naive RAG retrieves once and generates; agentic RAG makes retrieval a tool the model can call repeatedly, with follow-up queries informed by prior results.
- Agentic RAG uses the exact same agent loop as Module 04 -- retrieval is just another tool.
- Agentic RAG costs more per question; use it where multi-hop/exploratory retrieval is actually needed, not by default.

## Lab

[`labs/01-agentic-rag/`](../labs/01-agentic-rag/README.md)
