# LLM-as-judge

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Implement an LLM-as-judge that grades a candidate answer against a reference answer with structured output.
- Name the well-documented biases LLM judges have (position, verbosity, self-preference) and how to mitigate each.
- Decide when a mechanical check should replace an LLM judge entirely.

## Intuition

Exact-string matching a candidate answer against a reference answer fails
constantly for free-form text: "Paris" and "The capital of France is
Paris." are both correct but don't match as strings. An LLM-as-judge grades
by *meaning*, not exact text -- but it's a model judging another model's
output, which comes with its own real, well-documented failure modes,
distinct from whether the underlying task was answered correctly.

## The concept

### A structured-output judge

```python
async def judge(client, question: str, reference_answer: str, candidate_answer: str) -> dict:
    schema = {
        "type": "object",
        "properties": {"correct": {"type": "boolean"}, "reasoning": {"type": "string"}},
        "required": ["correct", "reasoning"],
    }
    response = await client.complete(
        [
            Message(
                role=Role.USER,
                content=(
                    f"Question: {question}\nReference answer: {reference_answer}\n"
                    f"Candidate answer: {candidate_answer}\n"
                    "Does the candidate answer correctly address the question, "
                    "matching the reference answer's meaning (not necessarily its "
                    "exact wording)?"
                ),
            )
        ],
        response_schema=schema,
    )
    return json.loads(response.message.content)
```

This is Module 02's structured-outputs pattern and Module 08's
evaluator-optimizer shape, applied to grading instead of revising -- a
separate model call, forced into a `{"correct": bool, "reasoning": str}`
shape, so the verdict is mechanically checkable (`verdict["correct"]`) while
still keeping the human-readable `reasoning` for debugging a disagreement.

### Known judge biases

- **Position bias**: when comparing two candidate answers side by side, a
  judge can favor whichever one appears first (or second) regardless of
  actual quality. **Mitigation**: run the comparison twice with the order
  swapped, and only trust a verdict that agrees both times.
- **Verbosity bias**: judges tend to rate longer answers as better, even
  when the extra length adds no real value. **Mitigation**: explicitly
  instruct the judge to evaluate correctness and concision separately, or
  score conciseness as its own criterion rather than an implicit one.
- **Self-preference bias**: a model used as both the agent under test and
  its own judge tends to rate its own outputs more favorably. **Mitigation**:
  use a different model (or at minimum a fresh, independent call with no
  shared context) as the judge -- the same "separate evaluation" principle
  from Module 08's evaluator-optimizer lesson, now applied because the
  grader and the graded share the same underlying model, not just the same
  context.

### When a judge isn't the right tool at all

If a task has a mechanically checkable answer (Module 13's "run the tests"
principle), use the mechanical check, not an LLM judge -- an exact numeric
answer, a well-formed JSON shape, a passing test suite. Reserve LLM-as-judge
for genuinely open-ended correctness (does this response actually answer
the question in a way a person would accept), where no deterministic check
exists.

## Deeper: a judge needs its own evaluation

It's tempting to treat the judge's verdict as ground truth once built, but
the judge is itself an LLM call and can be wrong. A rigorous eval setup
occasionally spot-checks the judge's verdicts against human review,
especially for edge cases where the judge and a human might reasonably
disagree -- treating the judge as a useful, cheap approximation of human
grading, not a perfect oracle.

## When not to use this

Don't use LLM-as-judge for anything with a deterministic ground truth
available -- lesson 01's golden-dataset accuracy on a math question, for
instance, could just as easily be checked by parsing and comparing numbers
directly, which is faster, cheaper, and has zero judge-bias risk.

## Common mistakes

- Using the exact same model instance/session as both the agent and its own
  judge, reintroducing self-preference bias without realizing it.
- Asking a judge to compare two candidates without controlling for position
  bias, then trusting a single unswapped verdict.
- Grading correctness and verbosity/style together as one implicit
  criterion, letting a longer-but-not-more-correct answer win.

## Key takeaways

- LLM-as-judge grades by meaning using structured output, solving exact-string matching's failure on free-form answers.
- Position, verbosity, and self-preference bias are real, documented judge failure modes with specific, known mitigations.
- Use a mechanical check instead of a judge whenever one is available -- reserve judging for genuinely open-ended correctness.

## Lab

[`labs/01-eval-harness-and-judge/`](../labs/01-eval-harness-and-judge/README.md)
