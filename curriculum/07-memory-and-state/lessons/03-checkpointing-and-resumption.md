# Checkpointing and resumption

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~1 hour

## Learning objectives

- Explain why a long-running agent needs to survive a process restart, not just a bad model response.
- Serialize an agent's in-progress state (messages, step count) to durable storage.
- Resume an agent run from a checkpoint without repeating already-completed work.

## Intuition

Every agent loop so far (Modules 03-06) lives entirely in one Python process's
memory -- if that process crashes, gets redeployed, or is killed mid-run, all
progress is lost and the agent starts over from scratch. For a short exchange
that's a minor inconvenience. For a long-running agent (Module 22 covers
multi-hour tasks) that's already made real tool calls -- possibly with real
side effects -- restarting from zero can mean redoing expensive work or, worse,
repeating a side-effecting action a second time. **Checkpointing** is
periodically saving enough state to durable storage that a fresh process can
pick up where the last one left off.

## The concept

### What needs to be in a checkpoint

At minimum: the full `messages` list (so the model has its complete history on
resume) and any loop-specific counters (how many steps have already run,
against `max_steps`). This is exactly the state Module 04's loop already holds
in local variables -- checkpointing just means writing it somewhere durable
instead of only keeping it in memory.

### Serializing messages

```python
import json
from dataclasses import asdict
from shared.llm.types import Message, Role, ToolCall, ToolResult


def message_to_dict(message: Message) -> dict:
    return {
        "role": message.role.value,
        "content": message.content,
        "tool_calls": [asdict(tc) for tc in message.tool_calls],
        "tool_result": asdict(message.tool_result) if message.tool_result else None,
    }


def message_from_dict(data: dict) -> Message:
    return Message(
        role=Role(data["role"]),
        content=data["content"],
        tool_calls=[ToolCall(**tc) for tc in data["tool_calls"]],
        tool_result=ToolResult(**data["tool_result"]) if data["tool_result"] else None,
    )
```

Dataclasses (Module 00, lesson 01) don't serialize to JSON automatically --
`Message` contains nested dataclasses and an enum, both of which need explicit
conversion. This is a common, slightly tedious but necessary step whenever you
persist structured objects across a process boundary.

### Save after every step, load before starting

```python
def save_checkpoint(path, messages, step):
    path.write_text(
        json.dumps(
            {
                "step": step,
                "messages": [message_to_dict(m) for m in messages],
            }
        )
    )


def load_checkpoint(path):
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    return [message_from_dict(m) for m in data["messages"]], data["step"]
```

The agent loop checks for an existing checkpoint at start; if one exists, it
resumes from the saved `messages`/`step` instead of starting fresh. It saves
again after every completed step, so at most one step's worth of work is ever
lost to an interruption -- not the entire run.

## Deeper: checkpointing interacts with side effects, not just state

If a tool call has a real side effect (sent an email, charged a payment) and
the process crashes *after* the side effect happened but *before* the
checkpoint saved that step completed, resuming naively could repeat the
side-effecting action. Robust systems handle this with idempotency (Module 19
covers this for production APIs) -- designing tools so that repeating a call
with the same identifying information is safe, rather than assuming
checkpointing alone prevents duplicate actions.

## When not to use this

Don't add checkpointing to a short-lived agent run (a handful of steps,
completing in seconds) where a full restart is an acceptable, cheap fallback --
the added complexity and I/O cost of checkpointing every step is only worth it
for longer-running or higher-stakes agent processes.

## Common mistakes

- Checkpointing only at the very end of a run -- this protects nothing, since a
  crash before completion loses everything just like having no checkpoint at
  all. Checkpoint incrementally, after each meaningful step.
- Forgetting to clean up (delete) the checkpoint file after successful
  completion -- a stale checkpoint from a finished run being accidentally
  loaded by a new, unrelated run is a real correctness bug.
- Assuming checkpointing alone makes side-effecting tool calls safe to
  resume -- it prevents *state* loss, not necessarily duplicate *actions*;
  that needs idempotent tool design (Module 19).

## Key takeaways

- Checkpointing serializes an agent's in-progress state (messages + counters) to durable storage so a restart doesn't lose all progress.
- Dataclasses and enums need explicit to/from-dict conversion for JSON serialization -- it doesn't happen automatically.
- Checkpointing protects against lost state, not automatically against repeated side effects -- that requires idempotent tool design (Module 19).

## Lab

[`labs/01-resumable-agent/`](../labs/01-resumable-agent/README.md)
