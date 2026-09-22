# Lab 05.01 -- Agent loop with compaction

**Difficulty:** ★★★★☆ · **Time:** ~2 hours

## Task

Extend Module 04's agent-loop pattern with a compaction strategy, and prove
(via a test) that it keeps a long-running agent under a token budget that a
naive, unbounded-history loop would blow past.

No API key needed -- tested against `shared.llm.get_client("mock")`. Real token
counts come from `tiktoken` (already a dependency, per Module 01).

## Files

- `starter/compacting_agent.py` -- skeleton with four functions to implement
- `solution/compacting_agent.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

Implement these in `starter/compacting_agent.py`:

- `def count_tokens(messages: list[Message]) -> int` -- sum the token count
  (via `tiktoken.get_encoding("o200k_base")`) of every message's `content`
  (treat `None` content as `""`; you don't need to count tool-call/tool-result
  structured content for this lab, just `content` text).
- `def compact_messages(messages: list[Message], max_tokens: int, keep_recent: int = 4) -> list[Message]`
  -- if `count_tokens(messages) <= max_tokens`, return `messages` unchanged.
  Otherwise: always keep every `Role.SYSTEM` message, keep the most recent
  `keep_recent` non-system messages, and replace everything else (the older
  non-system messages) with a single `Role.USER` message whose content is
  `f"[{n} earlier messages omitted to stay within the context budget.]"` where
  `n` is how many messages were omitted. If there's nothing older to compact
  (fewer than `keep_recent` non-system messages total), return `messages`
  unchanged.
- `async def run_agent_with_compaction(client: LLMClient, system_prompt: str, user_input: str, tools: list[ToolDefinition], registry: dict, max_context_tokens: int, max_steps: int = 20) -> str`
  -- same loop shape as Module 04's `run_react_agent`, except: before *each*
  `client.complete(...)` call, run `messages = compact_messages(messages, max_context_tokens)`.
  Use Module 03/04's `dispatch()` pattern for tool execution (you may copy it
  in, or reimplement it -- keep the same never-raises contract).
- `def dispatch(tool_call, registry) -> ToolResult` -- same contract as prior modules.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/compacting_agent.py`.
- `compact_messages` never drops a `Role.SYSTEM` message, and never compacts
  when already under budget.
- `run_agent_with_compaction` completes a 15+ step scripted tool-calling
  exchange (a budget small enough that an uncompacted history would exceed it)
  without error, and the **actual messages sent on the final call**
  (`client.provider.calls[-1]["messages"]`) are within `max_context_tokens`
  when passed through `count_tokens`.

## Hints

- Reuse `curriculum/04-agent-loop/labs/01-react-agent/solution/agent.py`'s
  `dispatch()` almost verbatim -- the contract hasn't changed.
- Pick a `max_context_tokens` and `keep_recent` in your tests small enough that
  20 scripted tool-call round trips would clearly exceed the budget without
  compaction, so the test is actually exercising compaction, not accidentally
  fitting anyway.

## Running the tests

```bash
uv run pytest curriculum/05-context-engineering/labs/01-compacting-agent/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/05-context-engineering/labs/01-compacting-agent/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 06 -- Retrieval & agentic RAG](../../../06-retrieval-and-rag/README.md)
