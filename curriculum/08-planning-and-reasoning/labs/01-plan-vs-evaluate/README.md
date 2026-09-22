# Lab 08.01 -- Plan-and-execute vs. evaluator-optimizer

**Difficulty:** ★★★★☆ · **Time:** ~2-3 hours

## Task

Implement both plan-and-execute (lesson 01) and evaluator-optimizer (lesson
02) for a small arithmetic-word-problem task, then compare their behavior on
the same inputs. No API key needed -- tested against
`shared.llm.get_client("mock")`.

## Files

- `starter/patterns.py` -- skeleton with both patterns to implement
- `solution/patterns.py` -- complete reference implementation
- `tests/` -- tests that exercise both

## Requirements

Implement these in `starter/patterns.py`:

**Plan-and-execute:**

- `async def plan(client: LLMClient, task: str) -> list[str]` -- request a
  structured `{"steps": [...]}` response (see lesson 01) and return the steps.
  Raise `ValueError` if the parsed `steps` list is empty.
- `async def execute_step(client: LLMClient, step: str) -> str` -- send `step`
  as a single user message, return the response text.
- `async def plan_and_execute(client: LLMClient, task: str) -> str` -- call
  `plan`, then `execute_step` for each step in order, then return the **last**
  step's result as the final answer (this task's plans always end with a
  "state the result" step, so the last execution *is* the final answer -- no
  separate synthesis call needed for this lab).

**Evaluator-optimizer:**

- `async def generate_draft(client: LLMClient, task: str, feedback: str | None) -> str`
  -- see lesson 02.
- `async def evaluate_draft(client: LLMClient, task: str, draft: str) -> tuple[bool, str]`
  -- request a structured `{"approved": bool, "feedback": str}` response.
- `async def evaluator_optimizer(client: LLMClient, task: str, max_iterations: int = 3) -> str`
  -- loop: generate, evaluate, return the draft if approved; otherwise
  regenerate with feedback. If never approved after `max_iterations`, return
  the **last** draft anyway (don't raise).

## Acceptance criteria

- All tests in `tests/` pass against your `starter/patterns.py`.
- `plan` raises `ValueError` on an empty `steps` list.
- `plan_and_execute` calls the model exactly `1 + len(steps)` times (one plan
  call, one per step) for a given scripted plan.
- `evaluator_optimizer` stops as soon as a draft is approved, without using
  remaining `max_iterations` budget it didn't need.
- `evaluator_optimizer` returns the last draft (not an exception, not `None`)
  when never approved within `max_iterations`.

## Comparing the two patterns (write this up, no code required)

After your implementation passes its tests, answer in a short comment at the
bottom of `solution/patterns.py` (already filled in for you) or your own notes:
for the specific task "solve this arithmetic word problem," which pattern
would you actually prefer in production, and why? Consider: number of model
calls for a typical case, what happens when the model's arithmetic is simply
wrong (does either pattern catch that, and how would you fix the one that
doesn't?), and which pattern gives you an inspectable intermediate artifact
(the plan; the draft+feedback history) that's useful for debugging.

## Running the tests

```bash
uv run pytest curriculum/08-planning-and-reasoning/labs/01-plan-vs-evaluate/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/08-planning-and-reasoning/labs/01-plan-vs-evaluate/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 09 -- Human-in-the-loop](../../../09-human-in-the-loop/README.md)
