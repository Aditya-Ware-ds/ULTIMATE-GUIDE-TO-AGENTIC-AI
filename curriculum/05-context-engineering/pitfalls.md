# Module 05 pitfalls

## Compacting away the information the next step actually needs

This lab's `compact_messages` always keeps the most recent `keep_recent`
messages -- but if a task requires referencing something further back (e.g. a
tool result from step 3 that's needed again at step 15, with 10+ messages now
between them), naive recency-based compaction will discard exactly the
information the agent needs. This is precisely the "compaction is lossy, and
that's the whole trade-off" point from lesson 02 -- if you find yourself
needing specific old facts to survive indefinitely, that's a signal you need
retrieval or persistent memory (Module 06/07), not a bigger `keep_recent`.

## Checking the token budget against the wrong thing

If `run_agent_with_compaction` checks `count_tokens(messages)` against the
budget *before* appending the current step's new tool-call/tool-result
messages, but compacts based on the *old* message list, the very next
`client.complete()` call can still exceed budget once the new messages are
added. The solution calls `compact_messages` at the top of each loop
iteration, which handles this correctly by re-checking (and re-compacting if
needed) right before every model call -- not just once, at the start.

## Off-by-one in `keep_recent` slicing

`rest[-keep_recent:]` and `rest[:-keep_recent]` are easy to get backwards
(especially under time pressure) -- swapping them silently keeps the *oldest*
messages and discards the *newest* ones, which is the opposite of what you
want and is a subtle bug that a quick glance at the code won't catch (both
versions "run" and "compact something"). This module's tests check the
specific content of the retained messages
(`test_compact_messages_keeps_recent_messages`) rather than just checking the
resulting length, precisely to catch this class of bug.

## Assuming the mock provider validates realistic behavior here

As in earlier modules: `MockLLMProvider` happily accepts an over-budget
`messages` list and returns whatever was scripted -- it never simulates a real
provider's context-length error. This lab's tests prove your compaction *logic*
is correct (the final call's messages measure under budget via `count_tokens`);
they don't prove a real provider would have rejected the uncompacted version.
If you want to see that failure mode for real, that's exactly the kind of thing
worth trying once against a real provider behind the `live` marker, with a
tiny, cheap model and a deliberately small `max_tokens`.
