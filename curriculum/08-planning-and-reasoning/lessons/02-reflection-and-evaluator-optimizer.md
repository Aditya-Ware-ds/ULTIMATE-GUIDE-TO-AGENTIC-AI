# Reflection and evaluator-optimizer

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~1 hour

## Learning objectives

- Explain the generate -> critique -> revise loop and why a separate evaluation step catches things self-continuation doesn't.
- Implement an evaluator-optimizer loop with structured pass/fail feedback.
- Know how many iterations are worth running before diminishing returns set in.

## Intuition

Asking a model to produce an answer and asking it to *check* that answer are
different tasks, even for the same model -- evaluating existing text against
criteria is often a more tractable problem than generating correct text from
scratch, similar to how proofreading someone else's paragraph is easier than
writing the same paragraph perfectly the first time. **Reflection** (or
self-critique) exploits this: after generating an answer, run a separate
evaluation pass against explicit criteria, and if it doesn't pass, revise and
try again.

## The concept

### The loop

```python
async def generate_draft(client: LLMClient, task: str, feedback: str | None = None) -> str:
    prompt = task if feedback is None else f"{task}\n\nPrevious attempt feedback: {feedback}"
    response = await client.complete([Message(role=Role.USER, content=prompt)])
    return response.message.content or ""


async def evaluate_draft(client: LLMClient, task: str, draft: str) -> tuple[bool, str]:
    schema = {
        "type": "object",
        "properties": {"approved": {"type": "boolean"}, "feedback": {"type": "string"}},
        "required": ["approved", "feedback"],
    }
    response = await client.complete(
        [
            Message(
                role=Role.USER,
                content=f"Task: {task}\nDraft: {draft}\nDoes this fully satisfy the task?",
            )
        ],
        response_schema=schema,
    )
    result = json.loads(response.message.content)
    return result["approved"], result["feedback"]


async def evaluator_optimizer(client: LLMClient, task: str, max_iterations: int = 3) -> str:
    feedback = None
    draft = ""
    for _ in range(max_iterations):
        draft = await generate_draft(client, task, feedback)
        approved, feedback = await evaluate_draft(client, task, draft)
        if approved:
            return draft
    return draft  # return the last attempt even if never approved
```

This is structurally similar to Module 04's stopping-condition discipline:
bound the loop (`max_iterations`), and decide explicitly what happens if it's
never approved (here: return the best attempt so far, rather than raising or
looping forever).

### Why a separate evaluation call, not just "think it over"

Asking a single model call to "write and then double check your own answer in
the same response" is weaker than a genuinely separate evaluation call,
because the same generation pass that produced a flawed answer is often
*prone to the same blind spot* when asked to review it inline -- there's no
fresh perspective. A separate call (sometimes with a different, even more
capable model) evaluating already-generated text is more likely to catch
issues the generation pass missed.

### Diminishing returns

Each iteration costs a generation call plus an evaluation call (Module 02's
cost lesson, doubled). In practice, most of the improvement from this pattern
happens in the first 1-2 revision cycles; further iterations increasingly
either converge on "good enough" or oscillate without meaningfully improving.
`max_iterations` of 2-3 is a reasonable default to start from and tune against
real evals (Module 16), not an arbitrary safety-only number.

## Deeper: evaluator-optimizer is not a substitute for a real eval suite

It's tempting to treat a passing evaluator-optimizer loop as proof of quality.
The evaluator is itself a model call with its own failure modes (Module 16
covers "LLM-as-judge" biases in depth) -- it can approve a flawed draft or
reject a fine one. This pattern improves *typical* output quality; it doesn't
replace measuring quality against a real, human-validated eval set before
trusting a system in production.

## When not to use this

Don't add an evaluator-optimizer loop to tasks with objectively, mechanically
checkable correctness (does this code pass its tests? does this JSON validate
against its schema?) -- use the mechanical check directly; it's cheaper, faster,
and more reliable than an LLM judging the same thing.

## Common mistakes

- Using the same prompt/framing for both generation and evaluation, making the
  evaluator prone to the same mistakes as the generator instead of providing
  genuinely independent scrutiny.
- No `max_iterations` bound -- the same unbounded-loop risk from Module 04
  applies here, doubled in cost per iteration.
- Treating the evaluator's `approved: true` as ground truth rather than one
  model's judgment, without ever validating that judgment against real outcomes
  (Module 16).

## Key takeaways

- Reflection separates generation and evaluation into distinct calls, which tends to catch more issues than asking a model to self-check inline.
- Structure the evaluation call's output (approved/feedback) the same way Module 02 covered, so the loop can act on it programmatically.
- Bound iterations, decide what happens if never approved, and don't mistake a passing loop for a real, measured quality guarantee (Module 16).

## Lab

[`labs/01-plan-vs-evaluate/`](../labs/01-plan-vs-evaluate/README.md)
