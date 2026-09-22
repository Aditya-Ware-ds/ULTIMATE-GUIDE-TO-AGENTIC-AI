# Module 12 quiz

**1. How does this module's supervisor-worker pattern relate to Module 08's orchestrator-workers?**

<details><summary>Answer</summary>

They're structurally the same pattern -- a coordinator decides how to route
or split work, dispatches to workers, and synthesizes results. Module 12
frames the workers as distinct *specialists* (a researcher, a writer, a
critic) rather than generic parallel sub-tasks, and gives the overall idea
its full multi-agent vocabulary.

</details>

**2. What distinguishes the handoff topology from supervisor-worker?**

<details><summary>Answer</summary>

In supervisor-worker, a central coordinator retains control and dispatches
to workers, then synthesizes their results itself. In handoff, agents
transfer control (and context) directly to each other based on what's
needed next -- there's no central coordinator retaining control throughout.

</details>

**3. Why does debate avoid the shared-bias risk that evaluator-optimizer (Module 08) can have?**

<details><summary>Answer</summary>

Evaluator-optimizer often uses the same model to both draft and revise, so a
systematic blind spot can persist across iterations. Debate uses independent
attempts (potentially different agents/models) compared by a separate judge,
so no single model's bias dominates the whole process.

</details>

**4. Why is a per-agent step budget insufficient to prevent infinite handoff loops?**

<details><summary>Answer</summary>

Each individual handoff decision can look reasonable in isolation (agent A
reasonably decides it needs agent B; agent B reasonably decides it needs
agent A) even though the system as a whole never converges. Preventing this
requires a budget tracked across the *entire* multi-agent run, not reset
per-agent.

</details>

**5. Why is "the worker produced a response" not sufficient evidence that the worker succeeded?**

<details><summary>Answer</summary>

A worker that got confused and gave up can produce output that looks, from
the supervisor's perspective, identical to a worker that actually succeeded.
Workers should report an explicit status (succeeded/failed/needs
clarification) that the supervisor checks mechanically, rather than the
supervisor inferring success from mere presence of output.

</details>

**6. Why do multi-agent systems need more observability than single agents, not less?**

<details><summary>Answer</summary>

Failures can emerge from the *interaction* between agents rather than any
single agent's individual behavior, so debugging requires visibility into
the whole conversation/handoff graph -- staring at one agent's log in
isolation can miss a bug that's really in how two agents' outputs interact.

</details>

**7. A task has three sequential steps, and each step uses the same tools and system prompt. Should you use multi-agent?**

<details><summary>Answer</summary>

No. Multi-agent's value is specialization and parallelism; "more than one
step" alone is what Module 04's ReAct loop or Module 08's plan-and-execute
already handle. Splitting a single coherent task into "agents" that share
the same prompt and tools adds coordination overhead with no real
specialization.

</details>

**8. What's the first question to ask before adding a second agent to a system?**

<details><summary>Answer</summary>

Does this need an agent at all, or is the task deterministic enough for
plain code? If plain code solves it, stop there -- don't reach for
multi-agent (or even a single agent) by default.

</details>

**9. What real costs does multi-agent add that a single well-tooled agent doesn't have?**

<details><summary>Answer</summary>

Latency (every hop is at least one extra model round-trip, compounding with
topology depth), cost (token spend multiplies across every agent involved),
and debuggability (failures can emerge from inter-agent interaction, which
is harder to trace than a single agent's behavior).

</details>

**10. In the supervisor-worker lab, why does the supervisor return `"status": "escalated"` instead of calling `synthesize` when a worker fails?**

<details><summary>Answer</summary>

Calling synthesize on a failed worker's output would produce a polished
answer that hides the fact that the underlying work never actually
succeeded -- exactly the "supervisor can't tell a worker actually finished"
failure mode this module warns about. Escalating surfaces the failure
instead of masking it.

</details>
