# Module 00 -- Programming prerequisites

**Difficulty:** ★☆☆☆☆ · **Time estimate:** 4-8 hours (skip/skim if you already code)

## Objectives

By the end of this module you can:

- Read and write Python using the features this repo leans on: type hints, dataclasses, `async`/`await`, context managers, and f-strings.
- Explain what JSON is, why LLM APIs are built around it, and convert between JSON and Python objects.
- Explain what HTTP and REST are well enough to read any API's docs, and make requests with `httpx`.
- Explain why LLM APIs are async-first and write basic `async def` code with `asyncio`.
- Use git well enough to clone, branch, commit, and diff -- this repo's own workflow.
- Set up an isolated Python environment with `uv` and use a terminal comfortably.

## Prerequisites

None. This is the starting point.

## Why this module exists

Every later module assumes you can read Python without stopping to look up syntax,
and that "make an HTTP request" or "parse this JSON" doesn't need explaining. If any
of the objectives above are already true for you, skim the lessons and go straight
to the lab to confirm, then move to
[Module 01](../01-how-llms-work/README.md).

## Contents

- [`lessons/01-python-essentials.md`](lessons/01-python-essentials.md)
- [`lessons/02-json-and-data.md`](lessons/02-json-and-data.md)
- [`lessons/03-http-and-rest.md`](lessons/03-http-and-rest.md)
- [`lessons/04-async-await.md`](lessons/04-async-await.md)
- [`lessons/05-git-and-environments.md`](lessons/05-git-and-environments.md)
- [`examples/`](examples/) -- small runnable demos for each lesson
- [`labs/01-async-fetch-cli/`](labs/01-async-fetch-cli/) -- build a small async HTTP + JSON CLI tool
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 01 -- How LLMs work](../01-how-llms-work/README.md)
