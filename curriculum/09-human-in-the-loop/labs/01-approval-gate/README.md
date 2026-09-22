# Lab 09.01 -- Agent with an approval gate

**Difficulty:** ★★★★☆ · **Time:** ~2-3 hours

## Task

Build an agent loop that pauses before calling a "risky" tool
(`send_email`), persists the pending call to a checkpoint (extending Module
07's checkpoint format), and can be resumed later with an approval or
rejection decision -- without repeating any already-completed steps.

**Simplification for this lab**: assume the model calls at most **one** tool
per turn (this keeps the pause/resume logic tractable; a production system
would need to handle a batch of tool calls where only some require approval).

No API key needed -- tested against `shared.llm.get_client("mock")`. The
"human decision" in tests is a plain boolean passed to a function, not a
blocking prompt (see hints).

## Files

- `starter/approval_agent.py` -- skeleton with the pieces to implement
- `solution/approval_agent.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

Implement these in `starter/approval_agent.py`:

- `REQUIRES_APPROVAL: set[str]` -- module-level set containing `"send_email"`.
- `_SENT_EMAILS: list[dict]` -- module-level list. `def send_email(to: str, subject: str) -> str`
  appends `{"to": to, "subject": subject}` to it (so tests can verify the real
  side effect happened, or didn't) and returns a confirmation string. Also
  implement a non-gated `def get_weather(city: str) -> str` (canned data is
  fine, e.g. always `"sunny"`) -- two tools, one gated, one not.
- `TOOLS: list[ToolDefinition]` and `TOOL_REGISTRY: dict[str, Callable]` for both tools.
- `def dispatch(tool_call, registry) -> ToolResult` -- same contract as prior modules.
- Checkpoint functions extending Module 07's shape with a `pending_tool_call`
  field: `def save_checkpoint(path, messages, step, pending_tool_call=None) -> None`
  and `def load_checkpoint(path) -> tuple[list[Message], int, ToolCall | None] | None`
  (reuse/adapt `message_to_dict`/`message_from_dict` from Module 07 directly).
- `async def run_agent_with_approval(client, checkpoint_path, system_prompt, user_input, max_steps=10) -> AgentResult`
  -- runs the loop. On a **non-gated** tool call, dispatch immediately and
  continue (checkpointing after, as in Module 07). On a **gated** tool call,
  save a checkpoint with that call as `pending_tool_call` and return
  immediately with `AgentResult(status="paused", pending_tool_call=tool_call)`
  -- do not dispatch it. On a final text answer, clean up the checkpoint and
  return `AgentResult(status="done", text=...)`. On exhausting `max_steps`,
  return `AgentResult(status="stopped", text="...")` leaving the checkpoint
  in place.
- `async def resume_after_approval(client, checkpoint_path, approved: bool, max_steps=10) -> AgentResult`
  -- load the checkpoint (must have a `pending_tool_call`); if `approved`,
  dispatch it for real; if not, build a
  `ToolResult(is_error=True, content="The user did not approve this action.")`
  instead. Either way, append the result and continue the **same loop** as
  `run_agent_with_approval` (factor the shared continuation logic into a
  private helper rather than duplicating the loop).
- `@dataclass class AgentResult` with fields `status: str`, `text: str | None = None`,
  `pending_tool_call: ToolCall | None = None`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/approval_agent.py`.
- A non-gated tool call (`get_weather`) never pauses -- it dispatches immediately.
- A gated tool call (`send_email`) always pauses with `status="paused"` and
  the correct `pending_tool_call`, without dispatching `send_email` at that point.
- Resuming with `approved=True` actually calls `send_email` (check this via a
  side effect, e.g. a list the test's fake `send_email` appends to) and
  continues to a final answer.
- Resuming with `approved=False` does **not** call `send_email`, and the model
  sees a rejection `ToolResult` on its next turn.
- After a `"done"` result (whether from a fresh run or after a resume), the
  checkpoint file no longer exists.

## Hints

- You can copy `message_to_dict`/`message_from_dict` from Module 07's lab
  almost verbatim -- add one more field (`pending_tool_call`) to the saved
  JSON, serialized/deserialized the same way (`asdict`/`ToolCall(**data)`).
- Structure `run_agent_with_approval` and `resume_after_approval` to both call
  a shared `async def _continue_loop(client, checkpoint_path, messages, step, max_steps) -> AgentResult`
  once they've each set up the right starting `messages`/`step` -- this avoids
  duplicating the loop body.

## Running the tests

```bash
uv run pytest curriculum/09-human-in-the-loop/labs/01-approval-gate/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/09-human-in-the-loop/labs/01-approval-gate/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then the
"customer-support agent with escalation" project in
[`projects/`](../../../../projects/README.md), then
[Module 10 -- Protocols](../../../10-protocols/README.md) (Level 3 begins)
