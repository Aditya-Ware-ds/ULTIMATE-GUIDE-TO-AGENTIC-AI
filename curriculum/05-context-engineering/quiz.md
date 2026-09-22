# Module 05 quiz

**1. List the five categories of content that compete for space in one agent call's context window.**

<details><summary>Answer</summary>

System prompt, tool definitions, conversation history, retrieved documents, and
the current turn's input.

</details>

**2. Why is "how many tools should this agent have available" a context-engineering question, not just a capabilities question?**

<details><summary>Answer</summary>

Every available tool's schema and description costs tokens on every single
call, whether or not it's used, and more available tools mean the model has to
disambiguate between more options at each decision point -- both a cost and (per
lesson 03) an accuracy consideration.

</details>

**3. What's the key difference between truncation and summarization as compaction strategies?**

<details><summary>Answer</summary>

Truncation drops old content outright with no attempt to preserve its
information. Summarization replaces old content with a condensed representation
that tries to preserve the gist, at the cost of extra complexity (and, for real
summarization, an extra model call).

</details>

**4. Why should a compaction check happen before a model call, not after?**

<details><summary>Answer</summary>

Checking before lets you shrink the request so it fits and performs well.
Checking after means you've already sent an over-budget (or quality-degraded)
request -- the damage, in cost or in a failed call, is already done.

</details>

**5. Why should a compaction strategy always preserve the system prompt?**

<details><summary>Answer</summary>

The system prompt sets the model's behavior and constraints for the whole
conversation. Losing it mid-conversation changes the model's behavior
unpredictably -- exactly the kind of instability compaction shouldn't introduce.

</details>

**6. What are the two distinct failure modes that make up "context rot"?**

<details><summary>Answer</summary>

Positional degradation ("lost in the middle" -- accuracy depends on where
information sits, U-shaped by position) and length degradation (accuracy
declines as total input grows, even with fixed, favorably-positioned
information).

</details>

**7. Does a 1M-token context window fix context rot for a task using, say, 200K tokens of that window?**

<details><summary>Answer</summary>

No. Context rot begins well before a window is full and is about how well the
model *uses* what's in context, not whether the content technically fits. A
huge window raises the ceiling of what's possible; it says nothing about
quality at any given length within it.

</details>

**8. If you control the ordering of retrieved documents in a prompt, where should the most important one go, given the "lost in the middle" effect?**

<details><summary>Answer</summary>

Near the start or the end of the context, not buried in the middle -- the
U-shaped accuracy curve means information there is read less reliably than
information at the edges.

</details>

**9. Why might including five loosely-relevant retrieved documents actually be worse than including two clearly relevant ones, beyond just token cost?**

<details><summary>Answer</summary>

Per context rot, more tokens (even irrelevant ones) compete with the
information that actually matters and can measurably reduce the model's
accuracy on the task -- it isn't just "more cost for the same quality," it can
be worse quality too.

</details>

**10. Why is compaction not a substitute for persistent memory (Module 07)?**

<details><summary>Answer</summary>

Compaction manages the current conversation's context window within one run --
it's inherently lossy and can discard information the current run no longer
needs. Persistent memory is about deliberately retaining specific information
across separate runs/sessions, which requires a different mechanism (external
storage), not just a smarter way to shrink one conversation's history.

</details>
