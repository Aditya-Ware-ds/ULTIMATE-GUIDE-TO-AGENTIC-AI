# Module 08 quiz

**1. What's the core difference between plan-and-execute and Module 04's step-by-step agent loop?**

<details><summary>Answer</summary>

Plan-and-execute generates a full plan up front and then executes it;
step-by-step decides only the next single action based on what's happened so
far, never committing to a multi-step plan in advance.

</details>

**2. Why might plan-and-execute be cheaper than a pure step-by-step agent for the same task?**

<details><summary>Answer</summary>

Once a plan exists, executing each individual step is often simpler than
solving the whole task, so a cheaper model can frequently execute well-specified
steps even if a stronger model was needed to produce the plan.

</details>

**3. What's the main weakness of plan-and-execute compared to step-by-step reasoning?**

<details><summary>Answer</summary>

A fixed plan doesn't automatically adapt if an early step's result reveals
that a later planned step should change -- it executes the original plan
regardless, unless you add an explicit re-planning step.

</details>

**4. Why is a separate evaluation call generally more effective than asking a model to check its own answer inline, in the same response?**

<details><summary>Answer</summary>

The same generation pass that produced a flawed answer is prone to the same
blind spot when reviewing it inline -- there's no fresh perspective. A
genuinely separate evaluation call is more likely to catch what the
generation pass missed.

</details>

**5. Why shouldn't you use evaluator-optimizer for checking whether generated code passes its tests?**

<details><summary>Answer</summary>

That's mechanically, deterministically checkable (run the tests) -- using an
LLM judge for something a direct check can verify is slower, costs more, and
is less reliable than the mechanical check.

</details>

**6. Before parallelizing two sub-tasks with `asyncio.gather`, what must you verify?**

<details><summary>Answer</summary>

That the sub-tasks are genuinely independent -- neither one's input depends on
the other's output. Parallelizing dependent steps (like a multi-hop question)
produces wrong results, not just no speedup.

</details>

**7. How does orchestrator-workers differ from plain parallelization?**

<details><summary>Answer</summary>

Plain parallelization runs a predetermined, fixed list of independent
sub-tasks concurrently. Orchestrator-workers dynamically decides (at runtime,
based on the actual task) how to split the work and what each worker should
do, then dispatches and synthesizes -- more flexible, closer to a multi-agent
system.

</details>

**8. Why should each worker in an orchestrator-workers system get only its own sub-task's context, not the orchestrator's full history?**

<details><summary>Answer</summary>

Per Module 05's context-budget lesson, giving every worker everything the
orchestrator has seen wastes context budget and risks context rot on
irrelevant information -- each worker only needs what's relevant to its
specific piece of the problem.

</details>

**9. What's the decision test for choosing a workflow versus an agent for a given task?**

<details><summary>Answer</summary>

Can you enumerate, in advance, the fixed sequence of steps that solves every
instance of this task? If yes, use a workflow (your code controls the
sequence). If it genuinely varies by input in ways you can't enumerate ahead
of time, use an agent (the model decides the next action).

</details>

**10. Why is "always build an agent, it's more flexible" a costly default?**

<details><summary>Answer</summary>

An agent's flexibility comes with real costs: more model calls, less
predictable behavior, and harder testing/debugging (Module 16) than a fixed
workflow covering the same ground. Paying that cost for a task whose steps
were actually fixed and well-understood buys nothing.

</details>
