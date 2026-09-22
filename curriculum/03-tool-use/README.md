# Module 03 -- Tool use / function calling

**Difficulty:** ★★★☆☆ · **Time estimate:** 5-7 hours

## Objectives

By the end of this module you can:

- Design a tool's JSON Schema so a model reliably picks the right tool and fills in valid arguments.
- Dispatch a model's tool call to real Python code and feed the result back correctly.
- Handle tool failures (bad arguments, exceptions, missing tools) without crashing the loop or silently hiding the failure from the model.
- Explain why tool code must never trust a model's arguments the way you'd trust your own code's inputs.

## Prerequisites

[Module 02 -- Talking to LLMs](../02-talking-to-llms/README.md)

## Why this module exists

This is where "a chatbot" becomes "an agent that can act." Every agent pattern in
every later module -- the agent loop (Module 04), memory (Module 07), multi-agent
systems (Module 12), coding agents (Module 13) -- is built on top of tool calling.
You're building it by hand here, with no framework, so Module 11's framework tour
later shows you *abstractions over this*, not magic.

## Contents

- [`lessons/01-tool-schemas.md`](lessons/01-tool-schemas.md)
- [`lessons/02-dispatch-and-execution.md`](lessons/02-dispatch-and-execution.md)
- [`lessons/03-error-handling-and-retries.md`](lessons/03-error-handling-and-retries.md)
- [`examples/`](examples/) -- small runnable demos (against the mock provider -- no API key needed)
- [`labs/01-tool-calling-loop/`](labs/01-tool-calling-loop/) -- a hand-written calculator + weather-lookup tool-calling loop
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 04 -- The agent loop from scratch](../04-agent-loop/README.md)
