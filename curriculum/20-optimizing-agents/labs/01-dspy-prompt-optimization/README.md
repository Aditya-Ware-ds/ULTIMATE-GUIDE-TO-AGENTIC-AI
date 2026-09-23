# Lab 20.01 -- DSPy prompt optimization

**Difficulty:** ★★★★★ · **Time:** ~2-3 hours

## Task

Build a DSPy program (a `Signature` run via `dspy.Predict`) and a metric
function, then optimize it with a real optimizer (`dspy.BootstrapFewShot`)
against a small training set -- entirely offline, using a scripted,
deterministic LM. No API key needed.

**Dependency note**: `dspy` is not part of this repo's default
dependencies (same reasoning as Module 11's 9 frameworks). Run these tests
with `uv run --with dspy pytest ...`; without `dspy` installed,
`pytest.importorskip("dspy")` makes this lab's tests show as **skipped**,
not failed, so the default `make test` stays green.

## Files

- `starter/dspy_optimizer.py` -- skeleton with the pieces to implement
- `solution/dspy_optimizer.py` -- complete reference implementation
- `tests/` -- tests that exercise the scripted LM, the metric, and the optimizer

## Requirements

Implement these in `starter/dspy_optimizer.py`:

- `ScriptedLM.forward(self, prompt=None, messages=None, **kwargs)` -- record
  the call, find which question (a key of `self._knowledge_base`) appears
  in the joined content of `messages`, and return an object shaped like
  DSPy's legacy LM contract expects: `.choices[0].message.content` set to
  `'{"answer": "<matched answer, or "unknown">"}'`, plus `.usage` (a dict)
  and `.model`.
- `def configure_scripted_lm(knowledge_base: dict[str, str]) -> ScriptedLM`
  -- create a `ScriptedLM`, call
  `dspy.configure(lm=lm, adapter=dspy.JSONAdapter())`, return the LM.
- `def build_program() -> dspy.Predict` -- return
  `dspy.Predict("question -> answer")`.
- `def exact_match_metric(example, prediction, trace=None) -> bool` --
  case-insensitive comparison of `example.answer` vs. `prediction.answer`.
- `def build_trainset(knowledge_base: dict[str, str]) -> list[dspy.Example]`
  -- one `dspy.Example(question=..., answer=...).with_inputs("question")`
  per entry.
- `def optimize_program(program, trainset) -> dspy.Predict` -- compile
  `program` with `dspy.BootstrapFewShot(metric=exact_match_metric,
  max_bootstrapped_demos=2, max_labeled_demos=2)` against `trainset`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/dspy_optimizer.py`.
- `configure_scripted_lm` + `build_program` answers a known question
  correctly with **exactly one** real model call (proving `JSONAdapter` is
  configured, avoiding `ChatAdapter`'s parse-failure fallback).
- `optimize_program`'s result has real bootstrapped demonstrations
  (`optimized.demos`) -- concrete proof optimization happened, not just
  that `.compile()` ran without error.
- The optimized program still answers correctly after optimization.

## Running the tests

```bash
uv run --with dspy pytest curriculum/20-optimizing-agents/labs/01-dspy-prompt-optimization/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run --with dspy pytest curriculum/20-optimizing-agents/labs/01-dspy-prompt-optimization/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 21 -- RL and training for agents](../../../21-rl-and-training-for-agents/README.md)
