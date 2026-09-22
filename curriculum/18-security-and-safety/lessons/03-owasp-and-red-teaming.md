# OWASP Top 10 and red-teaming your own agent

**Last verified:** 2026-09-22 (against [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) and [OWASP's Agentic AI -- Threats and Mitigations guide](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/))
**Difficulty:** ★★★★☆ · **Time:** ~40 minutes

## Learning objectives

- Name the current OWASP Top 10 for LLM Applications risks and where each shows up in this curriculum.
- Locate agentic-specific security guidance and understand how it relates to (not replaces) the LLM Top 10.
- Red-team your own agent in a structured, test-driven way: prove an exploit, patch it, prove the fix.

## Intuition

Lessons 01-02 covered one specific, high-priority risk (prompt injection)
and one specific, high-leverage defense (tool permissions) in depth.
This lesson zooms out to the full current risk landscape, and gives you a
repeatable process for finding and fixing this kind of problem in your own
agents rather than relying only on the risks this module happened to cover.

## The concept

### OWASP Top 10 for LLM Applications (2025, current as verified 2026-09-22)

| Rank | Risk | Where this curriculum touches it |
|---|---|---|
| LLM01 | Prompt Injection | Lesson 01, this module's lab |
| LLM02 | Sensitive Information Disclosure | Module 09's approval gates, Module 19's deployment secrets handling |
| LLM03 | Supply Chain | Module 11's framework dependency choices, Module 20's fine-tuning/distillation |
| LLM04 | Data and Model Poisoning | Module 06's retrieval sources, Module 21's RL reward design |
| LLM05 | Improper Output Handling | Module 03's tool-argument validation, Module 13's sandboxing |
| LLM06 | Excessive Agency | Lesson 02's least privilege, Module 09's human-in-the-loop |
| LLM07 | System Prompt Leakage | Not directly covered -- treat system prompts as not fully secret |
| LLM08 | Vector and Embedding Weaknesses | Module 06's RAG lab |
| LLM09 | Misinformation | Module 16's evaluation, hallucination material in Module 01 |
| LLM10 | Unbounded Consumption | Module 04/09's step budgets, Module 02's cost accounting |

Re-verify this table's exact rankings before quoting it elsewhere -- OWASP's
GenAI Security Project updates this list periodically, and by the time you
read this it may have moved (this is the same caution Module 16 lesson 03
gave for benchmark leaderboards).

### Agentic-specific guidance is separate, complementary material

OWASP's Agentic Security Initiative publishes dedicated, threat-model-based
guidance for agentic systems specifically (its "Agentic AI -- Threats and
Mitigations" guide, first published February 2025) -- this is **additional,
complementary** material addressing agent-specific concerns (multi-step
autonomy, tool orchestration, inter-agent trust) rather than a numbered
top-10 list that replaces the LLM Top 10 above. Treat the two as
layered: the LLM Top 10 covers risks inherent to any LLM application; the
agentic guidance covers what changes once that LLM is given autonomy and
tools, which is this curriculum's subject from Module 04 onward.

### Red-teaming your own agent: a repeatable process

1. **Pick a realistic attack scenario** for your specific agent -- not a
   generic "try to jailbreak it," but a scenario grounded in what your
   agent actually does (an indirect injection through a real content
   source it consumes, per lesson 01).
2. **Write a test that proves the exploit succeeds** against the current,
   unpatched agent -- a real, running, failing-in-the-security-sense test,
   not a hypothetical description. This is Module 13's test-driven
   discipline applied to security: don't trust "should be fine," prove
   what actually happens.
3. **Patch it** -- usually a tool-permission fix (lesson 02), sometimes a
   prompt-level mitigation as a secondary layer.
4. **Prove the same test now shows the exploit blocked** -- the test from
   step 2, now passing in the security sense (the harmful action didn't
   happen), is your evidence the fix actually works, not just that it
   looks reasonable.

This module's lab follows exactly this four-step process for one concrete
indirect-injection scenario.

## Deeper: red-teaming is never "done"

A red-team pass covers the scenarios you thought to test. New attack
patterns emerge continuously (the same reason Module 01's ground rules
insist on dated verification for fast-moving claims) -- treat your red-team
test suite as a living regression suite (Module 16 lesson 03) that grows
every time a new attack vector is discovered, the same way a golden dataset
grows as new failure modes are found.

## When not to use this

Don't build elaborate red-team infrastructure for an agent with no
consequential tools and no untrusted content in its inputs -- the risk
surface this module addresses specifically requires either genuine agency
(tools with real-world effects) or genuine exposure to untrusted content;
an agent with neither has a much smaller attack surface to begin with.

## Common mistakes

- Treating a single successful red-team pass as permanent proof of safety,
  rather than as one point-in-time result that needs to stay in a
  regression suite as the agent (and the threat landscape) evolves.
- Confusing the LLM Top 10 and the Agentic Security Initiative's guidance
  as competing or redundant, rather than understanding they cover different
  (complementary) layers of the same system.
- Red-teaming with only generic, textbook injection phrases instead of
  scenarios grounded in what your specific agent's tools and content
  sources actually are.

## Key takeaways

- The current OWASP Top 10 for LLM Applications (2025) ranks Prompt Injection #1 and Excessive Agency #6 -- re-verify rankings before quoting them, since this list is periodically updated.
- OWASP's Agentic Security Initiative publishes separate, complementary threat-and-mitigations guidance for agent-specific concerns, not a replacement top-10 list.
- Red-team your own agent with a four-step, test-driven process: pick a realistic scenario, prove the exploit with a failing test, patch it, prove the same test now shows it blocked.

## Lab

[`labs/01-indirect-injection-redteam/`](../labs/01-indirect-injection-redteam/README.md)
