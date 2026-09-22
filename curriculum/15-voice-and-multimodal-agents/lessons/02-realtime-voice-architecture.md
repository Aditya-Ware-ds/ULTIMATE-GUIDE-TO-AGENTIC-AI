# Realtime voice architecture

**Last verified:** 2026-09-22 (against [OpenAI's Realtime API guide](https://developers.openai.com/api/docs/guides/realtime))
**Difficulty:** ★★★☆☆ · **Time:** ~30 minutes

## Learning objectives

- Describe the current architecture of realtime voice agent APIs: transport, audio flow, and turn-taking.
- Explain why voice agents have a materially tighter latency budget than text agents.
- Recognize why this lesson is conceptual, with no required runnable lab -- and why that's a deliberate, cost-conscious choice.

## Intuition

Every agent this curriculum has built exchanges text (or, as of lesson 01,
images) in discrete turns -- there's no strict deadline on when a response
must arrive. A voice conversation has a real-time expectation baked in: a
multi-second pause after you finish speaking reads as broken, not thoughtful.
Realtime voice APIs are architected specifically around this constraint.

## The concept

### Transport and audio flow

OpenAI's current Realtime API guide (verified 2026-09-22) describes the
session connecting "over WebRTC in the browser or WebSocket on the server,"
with the model working "directly with audio, maintains conversation state,
and can call tools" -- audio in, audio out, without a separate
speech-to-text-then-text-to-speech pipeline in between. This directness is
what makes low latency achievable: chaining separate transcription,
reasoning, and synthesis steps (each with its own latency) would make the
tight turnaround realtime conversation needs much harder to hit.

### Turn-taking and interruption ("barge-in")

The same current guidance names the target user experience directly:
"barge-in, low first-audio latency, natural turn taking, and realtime tool
use." Voice activity detection (VAD) handles automatic turn detection --
the system needs to distinguish "the user paused to think" from "the user
finished speaking" in real time, and support the user interrupting
("barging in on") the agent mid-response, the same way a human conversation
allows interruption. This is a genuinely different problem from anything
Module 04's turn-based agent loop had to solve -- there, a "turn" is a
discrete, unambiguous unit; in voice, turn boundaries are inferred from
audio signal, and can be wrong.

### Latency budgets are the primary constraint

Text agents mostly avoid a real-time latency budget of their own -- a few
extra seconds rarely breaks the interaction the way it does in a live voice
call. Realtime voice architecture treats "low first-audio latency" as a
first-class design goal, not an afterthought, because it directly determines
whether the conversation feels natural. This is Module 05's cost/latency
material at a different scale: instead of "how many tokens does this cost,"
the operative question is "how many milliseconds until the user hears
something back."

### Architectural separation of concerns

Current SDK guidance separates a `RealtimeAgent` (instructions, tools -- the
same concerns Module 03/04 tools and system prompts already cover) from a
`RealtimeSession` (audio transport, connection lifecycle) -- the same
separation-of-concerns instinct as this repo's own `shared/llm/` (a provider
handles wire-level concerns; an agent's logic stays provider-agnostic),
applied to the additional complexity of a live audio transport layer.

## Deeper: why this lesson has no required runnable lab

Building a working realtime-audio lab would mean either a real, metered,
per-minute API dependency (breaking "tests run offline with no API keys")
or a large amount of audio-streaming infrastructure (WebSocket/WebRTC
plumbing) whose complexity is mostly about the transport layer, not agent
concepts this curriculum is teaching. Per the approved plan, this module
treats realtime voice as conceptual, architecture-level material -- you now
know how these systems are built and why, which is the actual transferable
skill, without this repo taking on a live audio dependency to prove it.

## When not to use this

Don't reach for a realtime voice architecture for a task that's naturally
turn-based and non-urgent (an email assistant, a batch report generator) --
the added transport complexity and latency engineering only pay for
themselves when the interaction genuinely needs to feel like a live
conversation.

## Common mistakes

- Assuming a realtime voice agent is "a text agent with speech-to-text
  bolted on the front and text-to-speech bolted on the back" -- current
  architectures process audio directly, specifically to avoid the added
  latency that pipeline would introduce.
- Treating turn-taking as solved by "wait for silence" -- real
  implementations need voice activity detection plus interruption handling,
  not just a fixed silence timeout.
- Ignoring latency as a design constraint until after a voice feature is
  built, rather than treating it as a first-class requirement from the
  start, the way current vendor guidance does.

## Key takeaways

- Current realtime voice APIs process audio directly (WebRTC/WebSocket transport, no separate transcription step) specifically to minimize latency.
- Turn-taking in voice requires voice activity detection and interruption ("barge-in") support -- a genuinely different problem than text agents' discrete turns.
- This module deliberately has no required runnable voice lab, to avoid a live, metered audio dependency breaking this repo's offline-testing ground rule.

## Lab

This lesson is conceptual; the module's runnable lab is
[`labs/01-vision-qa-agent/`](../labs/01-vision-qa-agent/README.md) (lesson 01).
