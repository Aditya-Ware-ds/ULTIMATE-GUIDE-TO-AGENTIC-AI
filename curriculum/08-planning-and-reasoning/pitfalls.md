# Module 08 pitfalls

## Trusting a plan's content because its shape validated

`plan()`'s `ValueError` check only catches an *empty* steps list -- it says
nothing about whether the steps are actually sensible, complete, or correctly
ordered for the task. Structured outputs (Module 02) guarantee the JSON shape
matches your schema; they say nothing about whether the *content* is good. A
plan with three steps that all say roughly the same thing, or that omit a
necessary step entirely, still "validates" against `{"steps": [...]}` --  this
is exactly why the lab's comparison writeup asks you to think about what
happens when the model's arithmetic (the content, not the structure) is
simply wrong.

## Evaluator-optimizer loops that never actually improve

If `generate_draft` doesn't meaningfully incorporate `feedback` into the next
attempt (e.g. the prompt construction has a bug and feedback never reaches the
model), the loop can burn through all `max_iterations` producing near-identical
drafts that keep failing the same evaluation for the same reason. This "looks
like" a working loop (it runs, it terminates, it returns something) while
silently never doing what it's supposed to. If you're debugging a
evaluator-optimizer loop that "isn't improving," check first that feedback is
actually reaching the generation step, not just that the loop mechanics run.

## Off-by-one between "steps executed" and "calls made"

`plan_and_execute`'s call count is `1 + len(steps)` (one plan call, one per
step) -- easy to get wrong if you accidentally call `plan()` twice, or forget
that the plan call itself is a model call too when reasoning about cost
(Module 02). This lab's
`test_plan_and_execute_calls_model_once_per_step_plus_plan` test exists
specifically to catch this arithmetic mistake, which is otherwise easy to miss
since the *output* (the last step's result) can still be correct even if the
call count is off.

## Parallelizing for a lab test's convenience, not because the task actually is independent

It's tempting, once you know `asyncio.gather` exists, to reach for it whenever
multiple things need to happen -- even if a later "sub-task" actually needs an
earlier one's result. Module 04's ReAct multi-hop example is the canonical
counter-example: the second search's query literally depends on the first
search's answer. Before parallelizing anything in your own future work
(beyond this lab, which deliberately doesn't parallelize plan-and-execute's
sequential steps), re-run the independence check from lesson 03 explicitly,
not just "these look like separate things."
