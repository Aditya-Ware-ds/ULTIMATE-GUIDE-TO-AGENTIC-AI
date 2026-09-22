# Module 12 pitfalls

## Confusing "the worker responded" with "the worker succeeded"

The lab's `researcher` worker can return `{"status": "error", ...}` for an
unanswerable claim -- the temptation, when wiring up your own supervisor
logic, is to check `if worker_result["output"]:` (truthy, so it always
passes) instead of `if worker_result["status"] != "success":`. Both a
successful and a failed worker return a populated `output` string; only the
`status` field actually distinguishes them. This is the exact failure mode
lesson 02 names -- a supervisor that can't tell a worker actually finished --
reproduced concretely in a test you can run (`test_supervisor_escalates_
without_synthesizing_on_worker_failure`).

## Letting `route_to_worker` silently default to a worker on an invalid choice

It's tempting to write `worker_name = choice if choice in worker_names else
worker_names[0]` so the system "always does something" -- but this hides a
real failure (the model chose something not in the list) behind output that
looks like ordinary, successful routing. The lab's solution raises
`ValueError` instead, on the same principle as Module 04's explicit
stopping conditions: a silent fallback is a worse failure than a loud one,
because it corrupts results downstream without leaving a trace of what went
wrong.

## Building a system-wide handoff budget but forgetting it needs to be system-wide

It's easy to add a step counter to each *individual* agent's own loop and
believe you've handled runaway behavior -- but two agents that each stay
well within their own per-agent budget can still hand off to each other
forever, since neither one's counter ever resets the other's. The budget
that actually prevents an infinite handoff loop (lesson 02,
`examples/handoff_budget_demo.py`) has to be tracked once, across the whole
multi-agent run, and checked by whatever code drives the handoff loop, not
by either individual agent.

## Reaching for multi-agent because the tools make it easy, not because the task needs it

Once you've built this module's lab, it's tempting to reach for
supervisor-worker as the default shape for any task with more than one
step -- lesson 03 exists specifically to counter this. Before adding a
second agent to any future project in this curriculum, re-run the decision
process from lesson 03: does this need an agent at all, does a single agent
with better tools suffice, and only then does a genuine multi-agent
topology earn its added latency, cost, and debugging surface.
