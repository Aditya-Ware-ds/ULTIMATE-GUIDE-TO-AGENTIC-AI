# Lab 07.01 -- Resumable agent (checkpoint & resume)

**Difficulty:** ★★★★☆ · **Time:** ~2-3 hours

## Task

Build an agent loop that checkpoints its state after every step and can resume
from a checkpoint file -- proving, via a test, that a simulated "kill and
restart" doesn't repeat already-completed model calls.

No API key needed -- tested against `shared.llm.get_client("mock")`.

## Files

- `starter/resumable_agent.py` -- skeleton with the pieces to implement
- `solution/resumable_agent.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

Implement these in `starter/resumable_agent.py`:

- `def message_to_dict(message: Message) -> dict` and
  `def message_from_dict(data: dict) -> Message` -- round-trip a `Message`
  (including `tool_calls` and `tool_result`) to/from a JSON-serializable dict
  (see `lessons/03-checkpointing-and-resumption.md`).
- `def save_checkpoint(path: Path, messages: list[Message], step: int) -> None`
  and `def load_checkpoint(path: Path) -> tuple[list[Message], int] | None` --
  `load_checkpoint` returns `None` if `path` doesn't exist.
- `def build_initial_messages(system_prompt: str, user_input: str) -> list[Message]`
- `def dispatch(tool_call, registry) -> ToolResult` -- same contract as prior modules.
- `async def run_one_step(client: LLMClient, messages: list[Message], tools: list[ToolDefinition], registry: dict) -> tuple[list[Message], str | None]`
  -- run exactly one loop iteration: call the model, and either (a) return
  `(messages, final_answer_text)` if the response has no tool calls, or (b)
  dispatch every tool call, append the assistant message and tool results to
  `messages`, and return `(messages, None)`.
- `async def run_resumable_agent(client: LLMClient, tools: list[ToolDefinition], registry: dict, checkpoint_path: Path, system_prompt: str, user_input: str, max_steps: int = 10) -> str`
  -- if `checkpoint_path` has an existing checkpoint, resume from it (do not
  rebuild `build_initial_messages` in that case). Otherwise start fresh. Loop
  calling `run_one_step`, saving a checkpoint after every step, until a final
  answer is reached (delete the checkpoint file and return the answer) or
  `max_steps` total steps (across the whole logical run, including any steps
  from before a resume) have elapsed (return a clear "stopped" message,
  leaving the checkpoint in place).

## Acceptance criteria

- All tests in `tests/` pass against your `starter/resumable_agent.py`.
- `message_to_dict`/`message_from_dict` round-trip every field, including a
  message with `tool_calls` and one with a `tool_result`.
- **The key property**: given a checkpoint saved after step 1 of a 3-step
  exchange, calling `run_resumable_agent` again with that checkpoint present
  calls the model only for the *remaining* steps -- it does not re-call the
  model for the step(s) already reflected in the checkpoint.
- On successful completion, the checkpoint file no longer exists.
- On hitting `max_steps`, the checkpoint file is left in place (so a future
  call could still resume further, e.g. after raising the limit) and a clear
  message is returned.

## Hints

- `dataclasses.asdict` handles nested dataclasses (like `ToolCall` inside a
  `Message`) automatically -- you don't need to convert each field by hand.
- The "kill and resume" test doesn't need multiprocessing or an actual crash --
  simulate it by calling `run_one_step` directly once, saving a checkpoint from
  that partial state, and then calling `run_resumable_agent` fresh against the
  same checkpoint path and the same (already-scripted) mock client.

## Running the tests

```bash
uv run pytest curriculum/07-memory-and-state/labs/01-resumable-agent/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/07-memory-and-state/labs/01-resumable-agent/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 08 -- Planning & reasoning patterns](../../../08-planning-and-reasoning/README.md)
