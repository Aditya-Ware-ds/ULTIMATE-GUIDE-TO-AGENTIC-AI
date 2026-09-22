# Eval-driven development and golden datasets

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Explain why unit tests against the mock provider don't answer "how good is this agent," and what does.
- Build a golden dataset: a fixed set of representative (input, reference answer) pairs.
- Run an agent against a golden dataset and compute an aggregate accuracy score.

## Intuition

Every lab in this curriculum has a test suite that passes -- and that
proves the *code* does what it's supposed to given a specific scripted
model response. It says nothing about whether the *agent*, given the real
variety of inputs it'll actually see, gets the right answer often enough to
ship. A golden dataset is how you measure that: a fixed, representative set
of real inputs with known-correct answers, scored automatically, so
"did this change make the agent better or worse" has an actual number
behind it instead of a vibe.

## The concept

### What a golden dataset actually is

```python
GOLDEN_DATASET = [
    {"question": "What is the capital of France?", "reference_answer": "Paris"},
    {"question": "What is 12 * 8?", "reference_answer": "96"},
    # ... representative of the real range of inputs the agent will see
]
```

The word "golden" means these are trusted, reviewed answers -- not just
whatever the agent happened to produce once. A golden dataset that's too
small or too narrow (all easy questions, or all one category) gives a
misleadingly high score; one that's representative of real, varied,
including edge-case inputs gives a score you can actually trust.

### Running the eval

```python
async def evaluate_dataset(client, agent_fn, dataset: list[dict]) -> dict:
    results = []
    for item in dataset:
        answer = await agent_fn(client, item["question"])
        verdict = await judge(client, item["question"], item["reference_answer"], answer)
        results.append({"question": item["question"], "answer": answer, **verdict})
    correct = sum(1 for r in results if r["correct"])
    return {
        "total": len(dataset),
        "correct": correct,
        "accuracy": correct / len(dataset),
        "results": results,
    }
```

(`judge` is lesson 02's LLM-as-judge -- exact-string matching rarely works
for free-form answers, which is exactly why grading needs its own lesson.)
The output isn't just a single number: `results` keeps every individual
verdict, so a regression is debuggable ("which specific questions newly
failed"), not just visible ("the score went down").

### Eval-driven development

The practice this enables: before changing a prompt, a tool description, or
a model, run the golden-dataset eval and record the baseline score. After
the change, run it again. If the score drops, you have concrete evidence the
change was a regression, not a hunch -- the same "don't ship based on vibes"
discipline Module 13's test-driven coding loop applies to bug fixes, now
applied to the agent's own behavior.

## Deeper: a golden dataset is itself a maintenance burden

A golden dataset needs to grow as new failure modes are discovered (add the
failing case to the dataset once you've fixed it, so it never silently
regresses again -- the same "add a regression test" discipline from
ordinary software engineering), and needs occasional review as the task
itself evolves (a reference answer that was correct under an old set of
product requirements can become wrong under new ones). Treat it as a living
asset, not a one-time artifact.

## When not to use this

Don't build a golden-dataset eval for a one-off script you'll run once and
discard -- the setup cost (curating representative examples, building a
judge) only pays off for something you'll iterate on repeatedly.

## Common mistakes

- A golden dataset with only easy, unambiguous examples -- it'll report a
  reassuringly high score that doesn't reflect how the agent handles the
  actually-hard inputs that matter in production.
- Never revisiting the dataset after it's built, so it silently drifts out
  of sync with what the agent is actually asked to do in practice.
- Treating a single aggregate accuracy number as the whole picture instead
  of also reading the per-item `results` when something regresses.

## Key takeaways

- A golden dataset is a fixed, representative, trusted set of (input, reference answer) pairs used to score an agent automatically.
- Eval-driven development means running the golden-dataset eval before and after a change to get concrete evidence, not a hunch, about whether it helped.
- Keep per-item results, not just an aggregate score -- that's what makes a regression debuggable.

## Lab

[`labs/01-eval-harness-and-judge/`](../labs/01-eval-harness-and-judge/README.md)
