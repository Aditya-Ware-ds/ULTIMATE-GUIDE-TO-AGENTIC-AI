# Module 09 pitfalls

## Dispatching before checking `REQUIRES_APPROVAL`

The order of operations in `_continue_loop` matters: check whether
`tool_call.name in REQUIRES_APPROVAL` **before** calling `dispatch`, not
after. A version that dispatches first and only checks approval status
afterward has already performed the risky action by the time it "realizes"
it should have asked first -- the entire point of the gate is to intercept
*before* execution, not to log what happened after the fact.

## Forgetting the one-tool-call-per-turn simplification's limits

This lab's `_continue_loop` only looks at `response.message.tool_calls[0]` --
by design, per the lab's stated simplification. If you extend this pattern
beyond the lab (a real system where the model might call both a gated and a
non-gated tool in the same turn), that simplification breaks down: you'd need
to dispatch the non-gated calls immediately, pause only for the gated one(s),
and track which calls in the batch are already resolved versus still pending
when you resume. Don't carry the single-tool-call assumption into a
production system without re-examining it.

## Checkpoint format drift between "mid-loop" and "paused for approval"

Module 07's checkpoints never had a `pending_tool_call` field; this module's
do. If code elsewhere in a larger system reads checkpoints without checking
for this field's presence (defaulting it to `None` when absent, as this
lab's `load_checkpoint` does via `data["pending_tool_call"]` returning
`None` when it was saved as `null`), a checkpoint saved by one version of the
code and read by another can behave unexpectedly. Keep checkpoint formats
explicit and versioned in a real system, rather than assuming every reader
and writer agree on the shape implicitly.

## Testing "the model saw an error" without checking `is_error` specifically

`test_rejection_is_seen_by_model_as_tool_result` checks
`m.tool_result.is_error` specifically, not just that *some* tool result
exists in the second call's messages. A version of `resume_after_approval`
that appends a plain, non-error `ToolResult` with rejection text in
`content` (e.g. forgetting `is_error=True`) would still pass a weaker test
that only checked "a tool result was sent," while giving the model a
misleading signal that the action *succeeded* with that text as its output,
rather than that it was *rejected*. Precise assertions catch precise bugs --
vague ones don't.
