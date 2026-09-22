# Module 02 -- Talking to LLMs

**Difficulty:** ★★☆☆☆ · **Time estimate:** 4-6 hours

## Objectives

By the end of this module you can:

- Read and construct the messages/roles array every current LLM API is built around.
- Explain why streaming exists and consume a streamed response correctly.
- Get reliable structured (JSON-schema-conforming) output from a model, and validate it.
- Apply core prompt-engineering techniques: clear instructions, examples, and explicit output format.
- Estimate the cost and latency of a call before making it.

## Prerequisites

[Module 01 -- How LLMs work](../01-how-llms-work/README.md)

## Why this module exists

Module 01 explained what's happening inside the model. This module is about the
*interface* to it -- the shape of the request and response every provider's API
shares, and the practices (streaming, structured outputs, prompt design, cost
awareness) that turn a raw API call into something you'd actually ship. Every
subsequent module builds agents on top of `shared/llm/`, the client this repo
already provides (see `shared/llm/client.py`); this module is where you understand
what that code is doing and why, before Module 03 has you build a tool-calling
loop on top of it.

## Contents

- [`lessons/01-messages-and-roles.md`](lessons/01-messages-and-roles.md)
- [`lessons/02-streaming.md`](lessons/02-streaming.md)
- [`lessons/03-structured-outputs.md`](lessons/03-structured-outputs.md)
- [`lessons/04-prompt-engineering-fundamentals.md`](lessons/04-prompt-engineering-fundamentals.md)
- [`lessons/05-cost-and-latency.md`](lessons/05-cost-and-latency.md)
- [`examples/`](examples/) -- small runnable demos for each lesson (against the mock provider -- no API key needed)
- [`labs/01-chat-and-extract/`](labs/01-chat-and-extract/) -- build a conversation loop, structured extraction, and cost estimation on top of `shared.llm`
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 03 -- Tool use / function calling](../03-tool-use/README.md)
