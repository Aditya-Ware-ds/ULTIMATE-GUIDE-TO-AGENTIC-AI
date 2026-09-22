# Module 14 -- Browser & computer-use agents

**Difficulty:** ★★★★☆ · **Time estimate:** 5-7 hours

## Objectives

By the end of this module you can:

- Build a browser-automation agent with a small, typed action vocabulary (`goto`/`click`/`get_text`) scoped to an allowlist of URLs.
- Explain the difference between DOM/selector-based browser automation and screenshot-based general computer use, and when each applies.
- Apply reliability techniques (explicit conditions over fixed sleeps, a narrow action vocabulary, step budgets) that make browser/computer-use agents less flaky.

## Prerequisites

[Module 13 -- Coding agents](../13-coding-agents/README.md)

## Why this module exists

Module 13's coding agent operated on files and a test suite -- deterministic,
text-based, and easy to sandbox. A browser or a full desktop is a much less
predictable environment: the same action can succeed or fail depending on
page-load timing, layout shifts, or an element that isn't there yet. This
module applies Module 13's same sandboxing and tool-scoping discipline (a
narrow, allowlisted action vocabulary; a step budget) to that less
predictable environment, and draws an explicit, currently-verified
distinction between two different technical approaches real products use:
DOM-based browser automation (this module's lab) and screenshot-based
general computer use (Claude, OpenAI, and Gemini's current computer-use
tools, covered conceptually).

## Contents

- [`lessons/01-browser-automation.md`](lessons/01-browser-automation.md)
- [`lessons/02-screenshots-vs-the-dom.md`](lessons/02-screenshots-vs-the-dom.md)
- [`lessons/03-reliability-tricks.md`](lessons/03-reliability-tricks.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-browser-task-agent/`](labs/01-browser-task-agent/) -- a browser-automation agent navigating a small bundled local page
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 15 -- Voice & multimodal agents](../15-voice-and-multimodal-agents/README.md)
