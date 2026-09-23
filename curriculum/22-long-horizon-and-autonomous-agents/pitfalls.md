# Module 22 pitfalls

## Saving progress only at the end of `run_long_horizon_agent`

It's tempting to accumulate results in memory and call `save_progress`
once, after the whole loop finishes -- simpler code, and it passes a naive
"does it work" test that always runs the full loop in one call. It
completely fails the actual point of this module: a crash between tasks 2
and 3 would lose tasks 1-2's results too, since they were never persisted.
`save_progress` must be called inside `run_one_task_and_persist`, after
*each* task, which is exactly what this lab's kill-and-resume test (calling
the single-task function directly, not the full loop) is designed to catch
if you get this wrong.

## Testing resumability by letting the full loop run in one call

If a test only ever calls `run_long_horizon_agent` start-to-finish in a
single call, it can pass even with a fundamentally broken resume path
(e.g. `run_long_horizon_agent` ignoring `load_progress`'s result entirely)
-- the bug only shows up when a *second*, separate call is made against an
already-partially-completed progress file. Always test resumability the
same way Module 07's lab does: call the single-step function directly to
simulate a crash, then make a genuinely separate call to the resuming
function and check it picks up correctly, rather than trusting a single
uninterrupted run to prove anything about resume behavior.

## Trusting a task's "done" status without it ever having been genuinely verified

This lab's `run_one_task_and_persist` marks a task `"done"` as soon as
`run_task` returns, with no independent check that the result is actually
correct (unlike Module 13's coding agent, which re-runs the tests before
trusting a fix). For a genuinely long-horizon, high-stakes plan, marking a
task done based only on "the model produced *some* response" reintroduces
exactly the "inferred success, not verified" failure mode Module 12 lesson
02 named -- a real long-horizon system should verify each task's result
(Module 16's eval harness, or a mechanical check per Module 13) before
persisting `"status": "done"`, not just persist whatever came back.

## Choosing task granularity that doesn't match the plan's actual structure

Splitting a genuinely atomic, indivisible unit of work into several
"tasks" just to have more progress-file checkpoints adds bookkeeping
overhead without reducing what a crash actually costs (since the atomic
unit still has to be redone as a whole either way). Conversely, treating
several genuinely independent, hours-apart pieces of work as a single
"task" means a crash costs all of them, when tracking them separately
would have preserved most of the work. Match the granularity to the plan's
real structure, not to an arbitrary choice of how many entries to track.
