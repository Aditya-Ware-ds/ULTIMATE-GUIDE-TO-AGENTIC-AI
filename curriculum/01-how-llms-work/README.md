# Module 01 -- How LLMs work

**Difficulty:** ★★☆☆☆ · **Time estimate:** 4-6 hours

## Objectives

By the end of this module you can:

- Explain what a token is, why LLMs operate on tokens rather than characters or
  words, and count tokens for real text with a real tokenizer.
- Explain what a context window is and why "the model forgot" is usually a
  context-window or context-management problem, not a memory bug.
- Explain temperature, top-p, and top-k, and predict how changing them changes a
  model's output distribution.
- Explain what an embedding is at a level useful for Module 06 (RAG).
- Explain what a "reasoning model" does differently from a standard model, and why
  hallucination is a structural property of how LLMs generate text, not a bug that
  gets patched out.

## Prerequisites

[Module 00 -- Programming prerequisites](../00-programming-prerequisites/README.md)

## Why this module exists

Every later module assumes you understand *why* an agent behaves the way it does
at the model level -- why a long conversation degrades, why raising temperature
makes an agent's tool-call choices less predictable, why a model states a wrong
fact with total confidence. You can't reason about agent failures if you think of
the model as a black box; this module opens it just enough.

## Contents

- [`lessons/01-tokens-and-tokenizers.md`](lessons/01-tokens-and-tokenizers.md)
- [`lessons/02-context-windows.md`](lessons/02-context-windows.md)
- [`lessons/03-sampling-and-decoding.md`](lessons/03-sampling-and-decoding.md)
- [`lessons/04-embeddings.md`](lessons/04-embeddings.md)
- [`lessons/05-reasoning-models-and-hallucination.md`](lessons/05-reasoning-models-and-hallucination.md)
- [`examples/`](examples/) -- small runnable demos for each lesson
- [`labs/01-token-sampling-visualizer/`](labs/01-token-sampling-visualizer/) -- count real tokens and simulate temperature-based sampling
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 02 -- Talking to LLMs](../02-talking-to-llms/README.md)
