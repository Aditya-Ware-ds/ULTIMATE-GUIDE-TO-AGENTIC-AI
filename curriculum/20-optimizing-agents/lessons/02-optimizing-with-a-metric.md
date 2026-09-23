# Optimizing with a metric

**Last verified:** 2026-09-22 (against `dspy` 3.3.1, installed and run directly)
**Difficulty:** ★★★★★ · **Time:** ~1 hour

## Learning objectives

- Write a metric function DSPy's optimizers can use to judge a program's outputs.
- Run `dspy.BootstrapFewShot` to automatically improve a program against a training set.
- Explain what "optimized" actually means here: real few-shot demonstrations selected by outcome, not a vague improvement.

## Intuition

Module 16 taught you to write a metric function to *measure* an agent.
DSPy's optimizers take that same kind of function and use it to *search*
for a better program -- trying different few-shot examples (or, with other
optimizers, different instructions or even weights) and keeping whichever
choice the metric says performs best. Lesson 01's `dspy.Predict` becomes
the search space; your metric becomes the objective function.

## The concept

### The metric function

```python
def exact_match_metric(example, prediction, trace=None) -> bool:
    return example.answer.lower() == prediction.answer.lower()
```

This is structurally identical to Module 16's judge, just simpler (an
exact check instead of an LLM-as-judge call) -- DSPy accepts any callable
with this `(example, prediction, trace) -> bool | float` shape, so a
mechanical check (Module 13's "run the tests" principle) or an LLM-as-judge
(Module 16 lesson 02) both work as a DSPy metric.

### Running the optimizer

```python
import dspy

trainset = [
    dspy.Example(question="What is the capital of France?", answer="Paris").with_inputs("question"),
    dspy.Example(question="What is the capital of Japan?", answer="Tokyo").with_inputs("question"),
]

program = dspy.Predict("question -> answer")
optimizer = dspy.BootstrapFewShot(metric=exact_match_metric, max_bootstrapped_demos=2)
optimized_program = optimizer.compile(program, trainset=trainset)
```

Verified directly (2026-09-22): `BootstrapFewShot.compile()` runs the
*unoptimized* program against `trainset`, keeps only the examples where
`exact_match_metric` returned `True` as "bootstrapped demonstrations," and
attaches them to the returned program. `optimized_program.demos` then
contains real `Example` objects DSPy selected -- not a vague notion of
"better," a concrete, inspectable list of few-shot examples chosen because
they empirically passed your metric.

### What "optimized" concretely means here

Calling `optimized_program(question=...)` now includes those bootstrapped
demonstrations in the prompt DSPy builds, the same way you might have
manually added a few worked examples to a hand-written prompt (Module 02's
prompt-engineering material) -- except DSPy selected *which* examples to
include based on which ones the program actually got right, rather than
you guessing which examples would help.

## Deeper: this is the same "prove it, don't assume it" discipline as every eval in this curriculum

`optimized_program.demos` being inspectable and non-empty is what lets you
verify optimization genuinely happened, rather than trusting that calling
`.compile()` did something useful -- the same principle behind Module 13's
independent test re-run and Module 12's explicit worker status: don't infer
success from the fact that a function returned without error, check what it
actually produced.

## When not to use this

Don't reach for `BootstrapFewShot` (or any DSPy optimizer) without a real
training set that reflects the task's actual variety -- an optimizer can
only bootstrap demonstrations from examples you give it, and a narrow or
unrepresentative training set produces an optimized program that's
narrowly, not genuinely, better (the same "golden dataset must be
representative" caution from Module 16 lesson 01).

## Common mistakes

- Writing a metric that returns `True` too permissively (e.g. checking only
  that the answer field is non-empty), which lets the optimizer "succeed"
  on every example without ever selecting for actual correctness.
- Never inspecting `optimized_program.demos` after compiling, and assuming
  optimization happened just because `.compile()` returned without error.
- Using an unrepresentative or too-small training set and expecting the
  optimized program to generalize well beyond it.

## Key takeaways

- A DSPy metric has the same `(example, prediction) -> bool/float` shape as Module 16's judge -- reuse a mechanical check or an LLM-as-judge, whichever fits the task.
- `BootstrapFewShot.compile()` runs the unoptimized program against a training set, keeps examples that pass the metric as few-shot demonstrations, and returns a program that uses them.
- Verify optimization actually happened by inspecting `optimized_program.demos`, not by trusting that `.compile()` ran without error.

## Lab

[`labs/01-dspy-prompt-optimization/`](../labs/01-dspy-prompt-optimization/README.md)
