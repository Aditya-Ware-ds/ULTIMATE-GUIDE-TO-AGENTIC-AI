# Module 04 pitfalls

## Confusing "stopped at max_steps" with "answered successfully"

If `run_react_agent`'s max-steps fallback message and its natural-completion
return value aren't clearly distinguishable by calling code, a caller (or a
test, or a human) can mistake "the agent gave up" for "the agent found an
answer." This lab's tests check the max-steps message contains an identifiable
marker (`"stopped"` or the step count) specifically so this distinction is
testable, not just implied by convention. Carry this forward into every later
module's agent loop -- it's a recurring, easy-to-miss bug class, not a
one-off lab requirement.

## Two-hop questions that don't actually require two hops

It's easy to accidentally write a "multi-hop" test where the second search
query doesn't actually depend on the first search's result (e.g. both queries
are hardcoded in the test regardless of what the first result was). That tests
"can the agent call two tools in a row," which is a real but much weaker claim
than "can the agent chain information across tool calls." The solution's tests
script the model's tool-call arguments directly (since `MockLLMProvider`
doesn't reason about prior results itself), so the *test* isn't proving true
multi-hop reasoning -- it's proving the *loop mechanics* work correctly for a
multi-hop shaped exchange. Proving genuine multi-hop reasoning ability requires
evaluating against a real model (Module 16), not the mock.

## Reusing a system prompt that never mentions stopping

If your system prompt tells the model to use tools but never says "give a
final answer with no further tool calls once you have enough information," you
are relying entirely on the model's default behavior to know when to stop
calling tools -- which is exactly the gap max-steps (lesson 02) exists to
backstop, but an explicit instruction reduces how often you actually hit that
backstop. Compare the lab's system prompt to Module 03's -- Module 03 didn't
need this instruction because it always stopped after any non-tool-call
response; this lab's *multi-step* nature makes the instruction worth stating
explicitly.

## Forgetting `Role` handling for a message that has both text and tool calls

A single assistant message can carry both `content` (reasoning text) and
`tool_calls` (the ReAct "Thought" + "Action" in one response). Code that
assumes a message is *either* text-only *or* tool-calls-only (e.g. an `if
response.message.content: return ...` before checking `tool_calls`) will
incorrectly treat a reasoning-plus-action step as a final answer, ending the
loop one hop too early. Always check `tool_calls` first, as this module's
examples and lab solution do.
