# Context windows

**Last verified:** 2026-09-22
**Difficulty:** ★★☆☆☆ · **Time:** ~30-45 minutes

## Learning objectives

- Define a context window precisely: what counts toward it, and what happens when you exceed it.
- Explain why "the model forgot what I said earlier" is a context-management problem, not a memory failure.
- Do rough token-budget math for a real conversation.

## Intuition

A context window is the model's entire working memory for one call: everything it
can "see" -- system prompt, conversation history, tool definitions, retrieved
documents, and the output it's about to generate -- has to fit inside one fixed
token budget. There's no persistent memory across calls unless *you* build it
(Module 07); each API call is stateless, and the context window is the complete
universe of what the model knows for that call.

## The concept

### What counts toward the window

For essentially every current provider, **input and output tokens share the same
budget** (a model advertised with a "1M-token context window" means input +
output together fit in 1M tokens, not 1M each). Everything in the request body
counts: system prompt, every prior message in the conversation you send back,
every tool definition, and any documents you've retrieved and inserted (Module 06).

### What happens when you exceed it

The request fails -- typically a 400-class error naming the context-length limit
you exceeded. The model does not "forget the oldest part automatically" by
default; *you* are responsible for keeping the conversation under budget, which is
exactly what Module 05 (context engineering) and Module 07 (memory) are about.

### A concrete budget example

Say a model has a 200K-token context window, your system prompt + tool
definitions are 2K tokens, and each conversation turn (user message + assistant
response) averages 300 tokens. Naively, you could fit roughly
`(200,000 - 2,000) / 300 ≈ 660` turns before hitting the limit -- but in practice
you'll want compaction (Module 05) well before that, both because cost scales
with tokens sent on *every* call (you resend the whole history each turn) and
because model quality on long contexts degrades before the hard limit (context
rot -- Module 05).

### Why cost scales with history length even though you're "just chatting"

Every conversational turn re-sends the *entire* prior history as input, because
the API is stateless. Turn 50 of a conversation pays for tokens 1 through 49's
worth of history as input, every single time, even though you already paid for
them in earlier calls. This is a major reason prompt caching (Module 19) exists.

## Deeper: context window size is not the same as effective quality

A model advertising a huge context window (e.g. 1M tokens) can technically accept
that much input, but its accuracy at using information buried in the middle of a
very long context is often measurably worse than its accuracy on the same
information near the start or end -- an effect often called the "lost in the
middle" problem. A bigger window raises the ceiling of what's *possible*; it
doesn't guarantee the model will *use* everything in it equally well. Module 05
covers this under "context rot."

## When not to use this

Don't reflexively stuff everything you might need into context "just in case" --
more context isn't free (cost) and isn't always better (quality, per the point
above). Module 05's whole premise is that what you put in context is a design
decision, not a dumping ground.

## Common mistakes

- Assuming a provider's context window applies to input alone -- check the docs;
  most current providers count input + output against one shared budget.
- Not accounting for tool definitions and system prompts in your budget math --
  they count every single call, even on the first message.
- Building a chat loop that resends full history forever with no compaction
  strategy, then being surprised when either costs balloon or a long-running
  conversation starts failing with a context-length error.

## Key takeaways

- The context window is one shared token budget for input + output, reset each call (no memory unless you build it).
- Exceeding it is an error, not automatic forgetting -- you own the budget.
- Bigger context windows raise the ceiling; they don't fix "the model didn't use information I gave it" on their own.

## Lab

[`labs/01-token-sampling-visualizer/`](../labs/01-token-sampling-visualizer/README.md)
