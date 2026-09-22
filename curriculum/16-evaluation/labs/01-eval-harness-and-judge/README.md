# Lab 16.01 -- Eval harness and judge

**Difficulty:** ★★★★☆ · **Time:** ~2 hours

## Task

Build a small golden-dataset eval harness with an LLM-as-judge (lessons 01
and 02), able to score any agent function against a fixed set of reference
answers and report both an aggregate accuracy and per-item results. No API
key needed -- tested against `shared.llm.get_client("mock")`.

`simple_agent` stands in for "the agent under test" -- in a real project
you'd pass in Module 04's ReAct agent, Module 13's coding agent, or any
other agent function with a compatible signature; this lab keeps the agent
itself trivial so the eval harness is what you're actually building and
testing.

## Files

- `starter/eval_harness.py` -- skeleton with the pieces to implement
- `solution/eval_harness.py` -- complete reference implementation
- `tests/` -- tests that exercise the judge and the full harness

## Requirements

Implement these in `starter/eval_harness.py`:

- `async def simple_agent(client, question: str) -> str` -- send `question`
  as a single user message, return the model's text response.
- `async def judge(client, question: str, reference_answer: str, candidate_answer: str) -> dict`
  -- request a structured `{"correct": bool, "reasoning": str}` verdict
  (see lessons/02-llm-as-judge.md).
- `async def evaluate_dataset(client, agent_fn, dataset: list[dict]) -> dict`
  -- for each `{"question": ..., "reference_answer": ...}` item: call
  `agent_fn(client, item["question"])` to get an answer, then `judge()` it.
  Return `{"total": ..., "correct": ..., "accuracy": ..., "results": [...]}`
  where each result is `{"question": ..., "answer": ..., "correct": ..., "reasoning": ...}`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/eval_harness.py`.
- `evaluate_dataset` calls `agent_fn` then `judge` once per dataset item, in
  that order (verify via `client.provider.call_count` and the scripted
  response sequence).
- `accuracy` is `correct / total` as a float (`1.0` for a perfect score,
  `0.5` for one right and one wrong out of two).
- `results` preserves each item's question, the agent's actual answer, and
  the judge's verdict -- not just the aggregate count.

## Running the tests

```bash
uv run pytest curriculum/16-evaluation/labs/01-eval-harness-and-judge/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/16-evaluation/labs/01-eval-harness-and-judge/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 17 -- Observability & debugging](../../../17-observability-and-debugging/README.md)
