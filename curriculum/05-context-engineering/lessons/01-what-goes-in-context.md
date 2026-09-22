# What goes in context

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~45 minutes

## Learning objectives

- List everything that competes for space in an agent's context window on a real call.
- Treat tool descriptions and system prompts as budgeted content, not free text.
- Make a deliberate call about what an agent needs to see versus what it doesn't.

## Intuition

Module 01 established that the context window is one shared token budget for a
whole call. Context engineering is the practice of deciding, on purpose, what
occupies that budget -- instead of letting it fill up with whatever accumulated
along the way. Every item you put in context is competing with every other item
for the model's attention (Module 05 lesson 03 covers why that competition has
real accuracy costs, not just a token-cost).

## The concept

### The full inventory, for one agent call

1. **System prompt** -- persona, rules, output format expectations. Sent every call.
2. **Tool definitions** -- every tool you make available, every call, whether or
   not the model ends up using it (Module 03's schemas + descriptions are not
   free -- verbose tool descriptions across many tools add up fast).
3. **Conversation history** -- every prior user/assistant/tool message
   (Module 01, lesson 02: resent in full, every call).
4. **Retrieved documents** (Module 06) -- anything fetched and inserted for
   grounding.
5. **The current turn's input.**

Every one of these is a design decision with a cost. A common mistake is
treating only #5 as something you control, and #1-#4 as fixed overhead -- all
of them are actually yours to shape.

### Tool availability is a context decision, not just a capability decision

If an agent has 30 tools available "just in case," every single call pays the
token cost of all 30 schemas and descriptions, and the model has to
disambiguate between more options at every decision point -- both a cost problem
and (per lesson 03) an accuracy problem. Only include tools genuinely relevant
to the current task or conversation; a routing step (Module 08) that narrows
down which toolset applies before the main agent runs is a common production
pattern for exactly this reason.

### System prompts: concise and structural, not exhaustive

A system prompt that tries to cover every possible edge case in prose becomes
long, and long system prompts compete with everything else for context space
*and* attention on every single call. Prefer concise, structural instructions
(the technique from Module 02 lesson 04) over an ever-growing list of "also
remember to..." additions -- if a system prompt keeps growing to patch specific
failures, that's often a sign the failures need a different fix (a tool, a
retrieval step, a smaller more focused prompt for a sub-task) rather than more
prose.

## Deeper: context is a budget you spend, not a container you fill

The most useful mental model: think of the context window as a budget you're
actively allocating across competing needs, not a container that happens to
have a maximum size you bump into eventually. Under this framing, "should this
information be in context for this call" is always a live design question, not
a default "yes, more information can't hurt" -- which, per lesson 03, is
actually false.

## When not to use this

Don't over-optimize context for a short-lived, single-shot task where the total
content is small and well under any real limit -- the discipline in this lesson
earns its keep specifically for long-running agents (many turns, many tool
results, growing retrieved content), not a five-message exchange.

## Common mistakes

- Registering every tool an agent might ever need, for every call, instead of
  scoping tool availability to what's relevant to the current task.
- Treating system-prompt growth as free because "it's just instructions" -- it's
  tokens like everything else, resent every single call.
- Not distinguishing "information the model needs to see this turn" from
  "information that happened to be generated earlier and is still sitting in
  history" -- the latter is exactly what compaction (lesson 02) targets.

## Key takeaways

- Context contains system prompt, tool definitions, conversation history, retrieved content, and the current turn -- all five are yours to shape, not just the last one.
- Unused tool availability is a real, ongoing cost (tokens and disambiguation difficulty), not a free safety margin.
- Treat the context window as an actively-managed budget, not a container you passively fill until it's full.

## Lab

[`labs/01-compacting-agent/`](../labs/01-compacting-agent/README.md)
