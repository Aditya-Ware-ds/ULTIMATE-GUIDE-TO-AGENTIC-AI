# Module 15 -- Voice & multimodal agents

**Difficulty:** ★★★☆☆ · **Time estimate:** 4-5 hours

## Objectives

By the end of this module you can:

- Send an image to a model as part of an agent's input and reason about the response, using `shared/llm/`'s new `ImageContent`/`Message.images` support.
- Explain the current architecture of realtime voice APIs (streaming audio in/out, turn-taking, latency budgets) at a conceptual level.
- Decide when a task needs multimodal input at all, versus when a text description is sufficient.

## Prerequisites

[Module 14 -- Browser & computer-use agents](../14-browser-and-computer-use-agents/README.md)

## Why this module exists

Level 4's agents have all consumed text (Module 13's file contents, Module
14's page text). Some tasks are fundamentally about pixels or audio, not
text -- reading a chart, checking a screenshot against a design, or having
a live spoken conversation. This module extends `shared/llm/` with minimal,
provider-verified image support and covers voice architecture conceptually,
closing out Level 4 before Level 5 turns to production concerns
(evaluation, observability, security, deployment).

## Contents

- [`lessons/01-vision-inputs.md`](lessons/01-vision-inputs.md)
- [`lessons/02-realtime-voice-architecture.md`](lessons/02-realtime-voice-architecture.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-vision-qa-agent/`](labs/01-vision-qa-agent/) -- an agent that answers questions about a bundled image
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

Level 4 is complete after this module. See [`projects/`](../../projects/README.md)
for "data-analysis agent with a code sandbox," then
[Module 16 -- Evaluation](../16-evaluation/README.md) (Level 5 begins).
