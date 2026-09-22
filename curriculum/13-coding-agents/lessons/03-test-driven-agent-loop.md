# The test-driven agent loop

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Implement a coding agent loop that edits code, runs the real test suite, and iterates on the result.
- Explain why a mechanical pass/fail signal changes what an agent loop can do compared to Module 04's ReAct loop.
- Apply Module 04's stopping-condition discipline to a loop whose "done" signal is a test suite, not a natural-language judgment.

## Intuition

Module 04's ReAct agent decided it was done when the model stopped
producing tool calls -- a judgment call, not a fact. A coding agent has
something better available: **you can just run the tests**. Whether the fix
worked isn't a matter of the model's opinion; it's `pytest`'s exit code.
This is the single biggest difference between a coding agent's loop and
every general-purpose agent loop built earlier in this curriculum, and it's
exactly the property Anthropic's own Claude Code guidance calls out: "give
Claude a check it can run... the loop closes on its own" (see resources.md).

## The concept

### The loop shape

```python
async def run_coding_agent(client, repo_root: Path, task: str, max_steps: int = 6) -> str:
    messages = [
        Message(role=Role.SYSTEM, content=_SYSTEM_PROMPT),
        Message(role=Role.USER, content=task),
    ]
    for _ in range(max_steps):
        response = await client.complete(messages, tools=TOOLS)
        if not response.message.tool_calls:
            return response.message.content or ""
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            result = dispatch(tool_call, TOOL_REGISTRY, repo_root)
            messages.append(Message(role=Role.TOOL, tool_result=result))
    return f"Stopped after {max_steps} steps without a passing test suite."
```

Structurally this is Module 04's ReAct loop, unchanged -- the difference is
entirely in the **tools**: `read_file`, `write_file` (lesson 02), and
`run_tests` (a thin wrapper around `shared/sandbox/shell_sandbox.run_shell`
running `pytest`, lesson 01). The agent's own reasoning decides what to
read and what to change; the test suite, not the model, decides whether it
worked.

### Why "run the tests" is a strictly better stop signal

Compare this to Module 08's evaluator-optimizer, where a *separate model
call* judges whether a draft is good enough -- useful when "good enough" is
inherently a judgment call (writing quality, tone), but strictly worse than
a mechanical check when one is available (Module 08's own quiz made this
point about using an LLM judge for something code can check directly). A
failing pytest run gives the agent the *exact* failure -- which assertion,
which line, what was expected vs. actual -- as concrete, actionable
feedback for its next edit, not just an approve/reject verdict.

### This is still bounded by a step budget

A test-driven loop is not exempt from Module 04's stopping-condition
discipline: an agent that can't figure out the fix could otherwise edit
forever, alternating between two wrong states. `max_steps` still applies,
and hitting it should say so plainly (per Module 04 lesson 2's
explicit-stopping principle), not silently return whatever the code looked
like on the last attempt as if it were a success.

## Deeper: showing evidence, not asserting success

The current Claude Code best-practices guidance frames this precisely:
"Have Claude show evidence rather than asserting success: the test output...
Reviewing evidence is faster than re-running the verification yourself."
Applied to this lab's loop: the agent's final answer should include *why*
it believes the task is done (the passing test output), not just a bare "I
fixed it" -- the same "explicit status over inferred success" discipline
from Module 12 lesson 02, now grounded in a mechanical check instead of a
worker's self-report.

## When not to use this

Don't build a test-driven loop for a task with no test suite to run against
-- if "did this work?" can't be checked mechanically, you're back to
Module 08's evaluator-optimizer or a human review step, not this pattern.

## Common mistakes

- Treating "the agent stopped calling tools" as success, the same mistake
  Module 04 warned about -- always check the actual test result, not
  whether the model *claims* it fixed the bug.
- No step budget, on the theory that "it'll just keep trying until it
  works" -- a genuinely stuck agent burns unbounded cost with no guarantee
  it ever converges.
- Giving the agent `write_file` but not `read_file` -- it will regenerate
  files from a stale mental model of their contents instead of the actual
  current state, especially after several edits.

## Key takeaways

- A coding agent's loop is Module 04's ReAct loop with file-editing and test-running tools -- the mechanics don't change, the stop signal does.
- A mechanical pass/fail check (the test suite) is a strictly better stop signal than an LLM judgment call, when one is available.
- Step budgets and explicit "didn't finish" messages still apply -- a verifiable check doesn't remove the need for bounded loops.

## Lab

[`labs/01-fix-the-failing-test/`](../labs/01-fix-the-failing-test/README.md)
