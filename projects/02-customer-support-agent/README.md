# Project 02 -- Customer-support agent with escalation

**Difficulty:** ★★★★☆ · **Time estimate:** 3-4 hours
**Comes after:** Level 2 (Modules 07-09)

## Spec

Build a customer-support agent that answers questions from a small FAQ
knowledge base, requires human approval before issuing a refund (a genuinely
consequential, hard-to-reverse action), and **escalates to a human** -- with a
useful summary of what it already tried -- if it can't resolve the request
within a step budget.

This is an integration project: it reuses Module 09's approval-gate/
checkpoint pattern almost directly and Module 09 lesson 3's escalation
pattern, rather than introducing new agent-loop mechanics. The FAQ lookup is
deliberately simpler than Module 06's hybrid search (a small in-memory dict
with keyword-overlap matching) -- this project's point is approval +
escalation integration, not retrieval sophistication.

No API key needed -- tested against `shared.llm.get_client("mock")`.

## Files

- `starter/support_agent.py` -- skeleton with the pieces to implement
- `solution/support_agent.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

Implement these in `starter/support_agent.py`:

- `FAQ: dict[str, str]` -- at least 3 entries (e.g. `"shipping"`, `"returns"`,
  `"account"`), each a short answer string.
- `def search_faq(query: str) -> str` -- keyword-overlap match `query` against
  `FAQ` values (reuse the `keyword_score` idea from Module 06 -- fraction of
  query words present in each entry -- and return the best-matching entry's
  text). Raise `ValueError` if no entry has any overlap at all.
- `_ISSUED_REFUNDS: list[dict]` and
  `def issue_refund(order_id: str, amount: float) -> str` -- appends
  `{"order_id": order_id, "amount": amount}` to `_ISSUED_REFUNDS`, returns a
  confirmation string.
- `SEARCH_FAQ_TOOL`, `ISSUE_REFUND_TOOL` (`ToolDefinition`s),
  `TOOL_REGISTRY`, and `REQUIRES_APPROVAL = {"issue_refund"}`.
- `def dispatch(tool_call, registry) -> ToolResult` -- same contract as prior modules.
- Checkpoint functions (`message_to_dict`, `message_from_dict`,
  `save_checkpoint`, `load_checkpoint`) -- same shape as Module 09's lab,
  including the `pending_tool_call` field.
- `def build_escalation_summary(messages: list[Message], reason: str) -> str`
  -- render every tool call and its result found in `messages` as a numbered
  list of attempted steps, followed by `reason`, in human-readable form (see
  Module 09 lesson 3 for the shape).
- `@dataclass class AgentResult` with fields `status: str` (one of `"done"`,
  `"paused"`, `"escalated"`), `text: str | None = None`,
  `pending_tool_call: ToolCall | None = None`.
- `async def run_support_agent(client, checkpoint_path, user_input, max_steps=5) -> AgentResult`
  -- same loop shape as Module 09's `_continue_loop`, with one difference: on
  exhausting `max_steps`, instead of a generic "stopped" message, return
  `AgentResult(status="escalated", text=build_escalation_summary(messages, "hit the step limit without resolving the request"))`,
  leaving the checkpoint in place (a human picking up the escalation could
  still choose to let it continue with a higher budget).
- `async def resume_after_approval(client, checkpoint_path, approved: bool, max_steps=5) -> AgentResult`
  -- same contract as Module 09's lab.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/support_agent.py`.
- `search_faq` finds the right entry for an on-topic query and raises
  `ValueError` for a completely unrelated one.
- `issue_refund` is gated: calling it always pauses first; it's only actually
  called (verified via `_ISSUED_REFUNDS`) after `resume_after_approval(..., approved=True)`.
- Hitting `max_steps` returns `status="escalated"` with a summary that
  mentions every tool call attempted, not just a bare "stopped" message.

## Running the tests

```bash
uv run pytest projects/02-customer-support-agent/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest projects/02-customer-support-agent/tests
```
