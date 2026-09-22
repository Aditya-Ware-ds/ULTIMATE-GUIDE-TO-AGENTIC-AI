# Module 04 -- The agent loop from scratch

**Difficulty:** ★★★★☆ · **Time estimate:** 5-7 hours

## Objectives

By the end of this module you can:

- Explain and implement the observe -> think -> act cycle that defines an agent, as distinct from a single tool-calling exchange.
- Design and implement stopping conditions (natural completion, max-steps, explicit "done" signals) so an agent loop can't run forever.
- Explain the ReAct pattern (interleaved reasoning and acting) and implement it by hand.
- Trace through a multi-hop agent run and predict what happens at each step.

## Prerequisites

[Module 03 -- Tool use / function calling](../03-tool-use/README.md)

## Why this module exists

Module 03 built a loop that called tools and fed results back -- that loop *is*
already a small agent, but it stopped as soon as the model produced any text.
This module generalizes that into the real thing: a loop that can take many
steps, reason about what to do next at each one, and know when to stop. Every
framework in Module 11 is, underneath, a more polished version of exactly this
loop -- you're building the reference you'll compare them against.

## Contents

- [`lessons/01-the-agent-loop.md`](lessons/01-the-agent-loop.md)
- [`lessons/02-stopping-conditions.md`](lessons/02-stopping-conditions.md)
- [`lessons/03-react-pattern.md`](lessons/03-react-pattern.md)
- [`examples/`](examples/) -- small runnable demos (against the mock provider -- no API key needed)
- [`labs/01-react-agent/`](labs/01-react-agent/) -- a hand-rolled ReAct agent answering multi-hop questions
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 05 -- Context engineering](../05-context-engineering/README.md)
