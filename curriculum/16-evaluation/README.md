# Module 16 -- Evaluation

**Difficulty:** ★★★★☆ · **Time estimate:** 6-8 hours

## Objectives

By the end of this module you can:

- Build a golden-dataset eval harness that scores an agent's answers against reference answers.
- Implement an LLM-as-judge and explain its known biases (position, verbosity, self-preference).
- Explain the difference between outcome evals and trajectory evals, and when each is needed.
- Describe what current public agent benchmarks (SWE-bench, GAIA, tau-bench, and others) actually measure.

## Prerequisites

[Module 15 -- Voice & multimodal agents](../15-voice-and-multimodal-agents/README.md)

## Why this module exists

Every module so far has proven individual pieces work with unit tests
against the mock provider -- proving *this function does what it should
given this scripted input*. That's necessary but doesn't answer a different
question production systems need answered continuously: *given real,
varied inputs, how often does the whole agent actually get the right
answer, and has that gotten better or worse since last week?* That's
evaluation, and Level 5 opens with it because everything else in this level
(observability, security, deployment) assumes you already have a way to
tell whether a change helped or hurt.

## Contents

- [`lessons/01-eval-driven-development-and-golden-datasets.md`](lessons/01-eval-driven-development-and-golden-datasets.md)
- [`lessons/02-llm-as-judge.md`](lessons/02-llm-as-judge.md)
- [`lessons/03-trajectory-evals-and-benchmarks.md`](lessons/03-trajectory-evals-and-benchmarks.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-eval-harness-and-judge/`](labs/01-eval-harness-and-judge/) -- a golden-dataset eval harness with an LLM-as-judge
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 17 -- Observability & debugging](../17-observability-and-debugging/README.md)
