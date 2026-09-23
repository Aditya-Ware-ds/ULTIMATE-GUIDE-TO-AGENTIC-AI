# Module 24 quiz

**1. Why is "I completed a course on AI agents" not a portfolio piece?**

<details><summary>Answer</summary>

It's a claim, not evidence -- a credible portfolio piece is specific and
checkable: a real decision made, a real trade-off considered, and a
working, runnable artifact, not a description of having studied the topic.

</details>

**2. Why is evidence of a real problem found and fixed (like Module 18's red-team pattern) more credible than a claim of quality alone?**

<details><summary>Answer</summary>

"I built a secure agent" is an unfalsifiable claim. "I found a real
indirect-injection exploit, proved it with a failing test, and fixed it
with a tool-level permission boundary" shows the actual reasoning process,
which is what a reviewer can actually evaluate and trust.

</details>

**3. Why are this curriculum's five interleaved projects and three capstones better portfolio pieces than individual module labs?**

<details><summary>Answer</summary>

They're built at the scale and integration depth worth showcasing --
individual labs are better used as depth evidence ("I understand X
specifically") within a larger project's writeup than as standalone
portfolio items.

</details>

**4. Where does a genuine first open-source contribution typically come from, per this module?**

<details><summary>Answer</summary>

A gap hit while actually using a tool for real work -- not from browsing
an issue tracker for something impressive-sounding. Module 11's and Module
20's own pitfalls.md files document real friction discovered exactly this
way while building this curriculum.

</details>

**5. Why is a small, precise fix a better first contribution than a large new feature?**

<details><summary>Answer</summary>

A large feature requires a maintainer to trust your design judgment before
seeing any of your work. A small, precise fix (a docs correction, a
minimal bug reproduction) requires much less trust to review and merge,
and builds the track record that makes larger contributions possible later.

</details>

**6. Before submitting a bug report or fix, what should you verify, and why?**

<details><summary>Answer</summary>

That the gap still exists against the project's *current* version -- the
same install-and-inspect discipline this curriculum used throughout
(Modules 10, 11, 14, 20). Reporting an already-fixed issue wastes a
maintainer's review time.

</details>

**7. What's the first step of a strong agent system-design interview answer, before proposing any architecture?**

<details><summary>Answer</summary>

Clarifying constraints: what's the failure cost, the expected volume, the
latency requirement, and whether a human needs to be in the loop for
specific actions -- the same "understand the actual problem before
choosing a pattern" discipline as Module 08's workflow-vs-agent decision.

</details>

**8. Why should cross-cutting concerns (evaluation, observability, security, cost) be named explicitly and unprompted in a system-design answer?**

<details><summary>Answer</summary>

Describing only the happy path is what separates a junior-sounding answer
from a senior one -- naming how your design specifically addresses each of
these, without being asked, signals you're thinking about the system as
something that has to keep working, not just something that works once.

</details>

**9. In the customer-support case study, why is a single agent the right topology rather than multi-agent?**

<details><summary>Answer</summary>

Per Module 12 lesson 03's decision process: the described scope (FAQ
answers, order lookup, refunds) doesn't have genuinely distinct specialist
sub-skills or a real parallelism need -- one well-tooled agent covers it,
and multi-agent would add coordination overhead without adding capability.

</details>

**10. In the multi-agent research system case study, why does multi-agent genuinely earn its cost there, unlike the support-agent case?**

<details><summary>Answer</summary>

The task has real, distinct specialist sub-skills (researching, writing,
critiquing) and genuine parallelism opportunity (multiple sources
investigated concurrently) -- exactly the structural signal Module 12
lesson 03 says should drive the decision, present here and absent in the
support-agent case.

</details>
