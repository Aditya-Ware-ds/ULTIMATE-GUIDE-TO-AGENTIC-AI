# Reasoning models, limitations, and hallucination

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45-60 minutes

## Learning objectives

- Explain what a "reasoning model" does differently from a standard model.
- Explain the difference between hidden and visible reasoning traces across current providers.
- Explain why hallucination is structural, and what actually reduces its impact (not "fixes" it).

## Intuition

A standard model generates its final answer token-by-token in one pass. A
**reasoning model** spends extra tokens *before* the final answer working through
the problem step by step -- breaking it down, checking intermediate steps,
sometimes backtracking -- similarly to how a person might work through a hard
problem on scratch paper before writing a final answer. This extra "thinking" is
itself just more generated tokens, sampled the same way as any other output; the
difference is architectural/training, not a fundamentally different generation
mechanism.

## The concept

### Two different approaches to exposing the reasoning

As of 2026, the two major current approaches differ specifically in whether you
see the reasoning:

- **Hidden reasoning** (OpenAI's o-series/reasoning-tier models): the model's
  internal reasoning tokens are generated but not shown to you -- you receive only
  the final answer and a token count that includes the hidden reasoning.
- **Visible extended thinking** (Anthropic's Claude): the model exposes its
  reasoning as readable "thinking" content, and you set a *thinking budget*
  (a token allowance) it can spend before responding. You can inspect this
  reasoning, which is useful for debugging why an agent made a particular
  decision.

Both approaches trade latency and cost (thinking tokens are billed, and take real
time to generate) for improved performance on harder, multi-step problems
(math, complex code, and multi-constraint planning are where the gap between
reasoning and non-reasoning models is usually largest).

### When to reach for a reasoning model in an agent

Reasoning models generally help most on tasks with genuine multi-step logical
structure: planning (Module 08), debugging (Module 13), and math/logic-heavy tool
use. They generally help *least* -- and cost more for no benefit -- on simple,
single-step tasks: a lookup, a format conversion, a one-line classification.
Matching model choice to task difficulty is itself an agent-design decision
(revisited in Module 19's "model routing").

### Hallucination is structural, not a bug

A model has no built-in mechanism that distinguishes "I am generating a
well-supported claim" from "I am generating a plausible-sounding but unsupported
claim" -- both come from the exact same next-token sampling process described in
lesson 03. The model is optimized to produce fluent, plausible continuations, not
to flag its own uncertainty. This is why hallucination can't be "patched out" the
way a software bug can -- it's an inherent consequence of how the generation
process works, not a defect isolated to specific bad code.

### What actually reduces hallucination's *impact* (not eliminates it)

- **Grounding with retrieval** (Module 06): giving the model relevant source
  documents in context so it can draw from real information rather than parametric
  "memory" alone.
- **Structured outputs and constrained generation** (Module 02): reducing the
  surface area for confident-but-wrong free text by constraining the shape of the
  answer.
- **Verification and evaluator-optimizer loops** (Module 08, Module 16): having a
  second pass (a tool call, a check, another model call) verify claims before they
  reach the user.
- **Asking for citations/sources and checking them** -- a model can still
  hallucinate a citation, so this only helps if you actually verify the citation
  resolves to something real, not just that one was provided.

None of these eliminate hallucination; they reduce the rate and the blast radius.
Any agent you ship should assume hallucination is possible and design around that
assumption, not treat a low observed rate in testing as a guarantee.

## Deeper: reasoning models can hallucinate too

Extra "thinking" tokens improve performance on problems with genuine logical
structure, but a reasoning model can still confidently reason its way to a wrong
conclusion, especially when a problem depends on facts the model wasn't trained
on or retrieval hasn't supplied. More thinking is not a substitute for grounding.

## When not to use this

Don't reach for a reasoning model as a default for every call in an agent -- the
latency and cost overhead is real and unnecessary for simple steps. Module 19's
model-routing pattern -- using a cheap/fast model for simple steps and a
reasoning model only for the hard ones -- is the production-appropriate version of
this idea.

## Common mistakes

- Treating a reasoning model's confident, well-structured-looking reasoning trace
  as proof the final answer is correct -- fluent reasoning and correct reasoning
  are not the same thing.
- Using a reasoning model for latency-sensitive, simple agent steps (a single tool
  call, a short classification) where the extra thinking adds cost and delay with
  no accuracy benefit.
- Believing a low hallucination rate in your own testing means it's "solved" for
  your use case -- test on your actual failure-prone edge cases (Module 16),
  not just happy-path examples.

## Key takeaways

- Reasoning models spend extra generated tokens on step-by-step reasoning before answering; providers differ on whether that reasoning is shown to you.
- Hallucination comes from the same token-sampling process as correct output -- there's no separate "I don't know" signal.
- Grounding, structured outputs, and verification reduce hallucination's impact; none of them eliminate it.

## Lab

[`labs/01-token-sampling-visualizer/`](../labs/01-token-sampling-visualizer/README.md)
