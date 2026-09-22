# Prompt engineering fundamentals

**Last verified:** 2026-09-22
**Difficulty:** ★★☆☆☆ · **Time:** ~45 minutes

## Learning objectives

- Apply the handful of prompt techniques with the most consistent, evidence-backed impact.
- Explain why "prompt engineering" is really "clear specification," not incantation.
- Recognize when a prompting problem is actually a different problem (retrieval, tooling, model choice) in disguise.

## Intuition

A model responds to what you actually asked, not what you meant. Most
"prompt engineering" is the unglamorous work of noticing the gap between those
two things and closing it -- the same discipline as writing a clear spec for a
human contractor who will follow your instructions extremely literally and has no
way to ask a clarifying question mid-task.

## The concept

### Techniques with consistent impact

- **Be explicit about the output format you want.** "Answer in one sentence."
  "Respond with only the number, no explanation." Vague requests get
  vague-shaped answers.
- **Give examples (few-shot prompting)** when the desired format or style is hard
  to describe precisely but easy to show:

```python
system_prompt = """Classify the sentiment of each review as positive, negative, or neutral.

Example:
Review: "This exceeded my expectations!"
Sentiment: positive

Review: "It broke after two days."
Sentiment: negative
"""
```

- **Put instructions and context in a clear order and structure** -- system
  prompt for stable instructions, then context/data, then the specific question.
  Models handle well-organized prompts (headers, delimiters like `---` or XML-ish
  tags) more reliably than a single unstructured paragraph.
- **Tell the model what NOT to do, specifically, when needed** -- "don't
  speculate; say 'I don't know' if the answer isn't in the provided context" is a
  concrete instruction a model can follow, unlike a vague hope that it'll be
  appropriately cautious on its own.
- **Ask for reasoning before the answer, for hard problems** -- prompting a model
  to work through a problem step-by-step before giving a final answer measurably
  improves accuracy on multi-step problems (this is a lightweight version of what
  reasoning models, Module 01 lesson 05, do more thoroughly and automatically).

### A concrete before/after

```
Bad:  "Tell me about this customer's order."

Better: "Summarize this customer's order in exactly 2 sentences: what they
ordered, and the current status. Do not include their personal contact
information. If the order status is unclear from the data, say 'status
unclear' rather than guessing."
```

The second version specifies length, content, an explicit exclusion, and a
fallback behavior -- each of those is a concrete instruction the model can
actually follow, rather than a hope.

## Deeper: prompting can't fix every problem

If a model doesn't have the information needed to answer correctly (it's not in
the prompt or its training data), no amount of prompt rewording will make it
know that information -- you need retrieval (Module 06), not a better prompt. If
a task genuinely requires an action (checking a live price, running a
calculation precisely), you need tool use (Module 03), not a more clever prompt
asking the model to "be careful" about arithmetic. Recognizing which category a
problem falls into is itself a skill this whole curriculum builds.

## When not to use this

Don't over-engineer a prompt with elaborate role-play framing, threats, or
"think very carefully" filler that research hasn't consistently shown to help --
if a specific technique isn't reliably improving your actual measured output
(Module 16 covers how to measure this rigorously instead of guessing), cut it.
Simpler, more explicit prompts that are wrong less often beat longer, vaguer
ones that occasionally get lucky.

## Common mistakes

- Iterating on a prompt based on a handful of manual spot-checks instead of a
  consistent eval set (Module 16) -- you can easily convince yourself a change
  "helped" when it just happened to fix the one example you were staring at.
- Cramming unrelated instructions into one giant prompt instead of splitting a
  task into smaller steps (Module 08's planning patterns) when the task is
  genuinely multi-part.
- Treating a hallucination or wrong answer as "the prompt wasn't good enough" when
  the real fix is retrieval, a tool call, or accepting the model's genuine limits
  (Module 01, lesson 05) -- not every failure is a prompting failure.

## Key takeaways

- The techniques with the most consistent payoff: explicit output format, few-shot examples, clear structure, explicit "don'ts," and asking for reasoning on hard problems.
- Prompting can't supply information the model doesn't have (that's retrieval) or perform precise actions (that's tool use).
- Measure prompt changes against a consistent eval set, not spot-checks -- Module 16 covers how.

## Lab

[`labs/01-chat-and-extract/`](../labs/01-chat-and-extract/README.md)
