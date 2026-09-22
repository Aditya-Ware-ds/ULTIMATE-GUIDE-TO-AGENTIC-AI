# Module 18 quiz

**1. What's the difference between direct and indirect prompt injection?**

<details><summary>Answer</summary>

Direct injection comes from the user's own message trying to override
instructions. Indirect injection comes from content the agent reads while
doing its job (a retrieved document, a web page, a tool result) -- the
attacker never talks to the agent directly, they plant the instruction
somewhere the agent will encounter it.

</details>

**2. Why is indirect injection specifically the harder problem for tool-using agents?**

<details><summary>Answer</summary>

Every agent that consumes external content it doesn't fully control the
origin of (retrieval, tool results, page text, file reads) is a potential
target by default -- this is nearly every agent built from Module 04
onward, and the attacker doesn't need any access to the user or the system
prompt at all.

</details>

**3. Why can't prompt injection be fully solved by instructing the model to ignore instructions found in retrieved content?**

<details><summary>Answer</summary>

Prompt-level instructions help but are not a reliable, complete defense --
a sufficiently crafted injection can still succeed against them. This is
why lesson 02 focuses on constraining what a tool is capable of doing
regardless of the model's decision, as the more reliable complementary layer.

</details>

**4. In this module's lab, what specifically proves the indirect-injection exploit is blocked?**

<details><summary>Answer</summary>

That `_SENT_EMAILS` stays empty after the scripted, "successfully
manipulated" model attempts to email the attacker -- not that the model
"resisted" the injection (it didn't, by design of the test), but that the
tool itself refused the call regardless.

</details>

**5. What pattern do Module 13's `resolve_within_repo`, Module 13's `DEFAULT_ALLOWED_COMMANDS`, and Module 14's URL allowlist all have in common, as named explicitly by this module?**

<details><summary>Answer</summary>

They're all instances of least privilege: the tool enforces its own
boundary on what it will do, independent of what the model requests. This
module names that recurring pattern as a security control and applies it
to a new, more consequential kind of tool (sending email).

</details>

**6. Why should a tool's arguments be treated as untrusted input, even though they came from "your own" model?**

<details><summary>Answer</summary>

The model's decision can be wrong or manipulated (via injection), so its
output should be treated the same way a web application treats
client-supplied input: validated and constrained at the boundary,
regardless of what happened upstream (careful prompting, client-side
validation) that was supposed to prevent a bad value from ever being sent.

</details>

**7. What does OWASP's current (2025) Top 10 for LLM Applications rank as the #1 risk, and what rank does Excessive Agency currently hold?**

<details><summary>Answer</summary>

Prompt Injection (LLM01) is #1. Excessive Agency is LLM06 (#6) as of the
2025 list verified in this module -- re-check before quoting either, since
this list is periodically updated by OWASP's GenAI Security Project.

</details>

**8. How does OWASP's Agentic Security Initiative guidance relate to the LLM Top 10 -- does it replace it?**

<details><summary>Answer</summary>

No -- it's separate, complementary, threat-model-based guidance addressing
agent-specific concerns (multi-step autonomy, tool orchestration,
inter-agent trust) layered on top of the LLM Top 10's risks, which apply to
any LLM application regardless of whether it has agentic capabilities.

</details>

**9. What are the four steps of this module's red-team process?**

<details><summary>Answer</summary>

(1) Pick a realistic attack scenario grounded in what the specific agent
actually does; (2) write a test that proves the exploit succeeds against
the current, unpatched agent; (3) patch it (usually a tool-permission fix);
(4) prove the same test now shows the exploit blocked.

</details>

**10. Why is a single successful red-team pass not permanent proof an agent is safe?**

<details><summary>Answer</summary>

A red-team pass only covers the scenarios you thought to test, and new
attack patterns emerge continuously. Treat the red-team test suite as a
living regression suite that grows every time a new attack vector is
discovered, the same way a golden dataset (Module 16) grows as new failure
modes are found.

</details>
