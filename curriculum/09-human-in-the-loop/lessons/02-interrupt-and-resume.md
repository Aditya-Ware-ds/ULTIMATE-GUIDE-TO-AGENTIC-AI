# Interrupt and resume

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~1 hour

## Learning objectives

- Explain why an approval gate is a pause-and-resume problem, and why Module 07's checkpointing is the right foundation for it.
- Persist a pending, unexecuted tool call as part of a checkpoint.
- Resume an agent correctly whether the human approved or rejected the pending action.

## Intuition

An approval gate isn't fundamentally different from Module 07's
crash-recovery checkpointing -- both are "stop the loop, save enough state to
continue correctly later, resume from that state." The difference is *why*
you're stopping: Module 07 handles an involuntary interruption (a crash);
this lesson handles a deliberate one (waiting for a person). The mechanics --
serialize state, persist it, reload it later, continue -- are the same
mechanics, just triggered on purpose instead of by failure.

## The concept

### What's different about this checkpoint: a pending action

Module 07's checkpoint held `messages` and a `step` counter. An approval-gate
checkpoint needs one more thing: the **pending tool call** itself -- the
specific action awaiting a decision, since it hasn't been dispatched yet and
its result isn't in `messages`.

```python
def save_checkpoint(path, messages, step, pending_tool_call=None):
    data = {
        "step": step,
        "messages": [message_to_dict(m) for m in messages],
        "pending_tool_call": asdict(pending_tool_call) if pending_tool_call else None,
    }
    path.write_text(json.dumps(data))
```

The assistant's message announcing the tool call is already appended to
`messages` before saving (the model *did* decide to call it -- that's a fact
of history); what's missing until a decision is made is the **result** of
that call.

### Resuming after a decision

```python
async def resume_after_approval(
    client, tools, registry, checkpoint_path, approved: bool, max_steps=10
):
    messages, step, pending_tool_call = load_checkpoint(checkpoint_path)
    if approved:
        result = dispatch(pending_tool_call, registry)
    else:
        result = ToolResult(
            tool_call_id=pending_tool_call.id,
            content="The user did not approve this action.",
            is_error=True,
        )
    messages.append(Message(role=Role.TOOL, tool_result=result))
    step += 1
    return await _continue_loop(client, tools, registry, checkpoint_path, messages, step, max_steps)
```

Rejection is modeled as a *tool result* (with `is_error=True`, same as any
other recoverable tool failure from Module 03) rather than as a special
exception or a different code path -- the model already knows how to react to
a failed tool call, so rejection reuses that exact mechanism instead of
inventing a new one.

## Deeper: an approval pause should look, to the rest of the loop, like any other await point

The cleanest implementations treat "waiting for approval" as structurally
identical to "waiting for a checkpoint to be resumed after a crash" -- the
loop doesn't need special-case logic for *why* it stopped, only for *what to
do* once it has an answer (a tool result, either from a real dispatch or a
rejection). This is why lesson 01's "gate" and this lesson's "checkpoint" are
two views of the same mechanism, not two separate systems bolted together.

## When not to use this

Don't build a full checkpoint-based pause/resume system for a single-process,
short-lived interaction where a simple in-memory `await get_human_decision()`
call (blocking until a UI or CLI prompt returns) is sufficient -- the durable,
file-based version earns its complexity specifically when the human's decision
might come much later (minutes, hours) than the agent's run, potentially in a
different process entirely (e.g. a web request handling the approval UI,
separate from whatever process is running the agent).

## Common mistakes

- Forgetting to persist the pending tool call itself, only the messages up to
  that point -- on resume, there's no way to know *what* was awaiting approval
  without it.
- Treating "rejected" as an error condition that should crash or abort the
  whole run, instead of feeding it back to the model as a normal (if
  unwelcome) tool result it can react to.
- Not distinguishing, in your checkpoint format, between a checkpoint saved
  mid-loop (Module 07's shape, no pending action) and one saved specifically
  for approval (this lesson's shape, with a pending action) -- code reading a
  checkpoint needs to know which case it's in.

## Key takeaways

- An approval gate is a pause-and-resume problem, structurally identical to Module 07's checkpointing -- add the pending tool call to what gets persisted.
- Rejection is fed back as a normal `ToolResult(is_error=True)`, reusing Module 03's existing recoverable-failure mechanism rather than a new code path.
- Durable, file-based pause/resume earns its complexity when a human's decision might come much later, possibly from a different process -- a simple blocking prompt is enough for short-lived, single-process cases.

## Lab

[`labs/01-approval-gate/`](../labs/01-approval-gate/README.md)
