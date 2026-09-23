# Cheatsheet: agent security checklist

From Module 18 (Security & safety). **Last verified:** 2026-09-22 against
[OWASP's Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/) --
re-check this list is still current before citing rankings elsewhere.

## OWASP Top 10 for LLM Applications (2025)

| Rank | Risk | Where this curriculum addresses it |
|---|---|---|
| LLM01 | Prompt Injection | Module 18 lesson 01, its lab |
| LLM02 | Sensitive Information Disclosure | Module 09's approval gates, Module 19's secrets handling |
| LLM03 | Supply Chain | Module 11's dependency choices, Module 20's fine-tuning/distillation |
| LLM04 | Data and Model Poisoning | Module 06's retrieval sources, Module 21's reward design |
| LLM05 | Improper Output Handling | Module 03's tool-argument validation, Module 13's sandboxing |
| LLM06 | Excessive Agency | Module 18 lesson 02's least privilege, Module 09's HITL |
| LLM07 | System Prompt Leakage | Treat system prompts as not fully secret |
| LLM08 | Vector and Embedding Weaknesses | Module 06's RAG lab |
| LLM09 | Misinformation | Module 16's evaluation, Module 01's hallucination material |
| LLM10 | Unbounded Consumption | Module 04/09's step budgets, Module 02's cost accounting |

OWASP's Agentic Security Initiative also publishes separate,
**complementary** (not replacement) threat-and-mitigations guidance for
agent-specific concerns -- see Module 18 lesson 03.

## Before shipping an agent with any consequential tool

- [ ] **Every consequential tool enforces its own boundary** (an allowlist of files/URLs/recipients/channels/amounts) independent of the model's decision -- never rely on prompting alone (Module 13, 14, 18).
- [ ] **Path/URL inputs are resolved and checked**, not string-matched for `".."` -- catches symlinks and absolute paths too (Module 13 lesson 02).
- [ ] **A human-approval gate exists for genuinely high-stakes actions**, composed *with* (not instead of) the tool-level boundary (Module 09 + Module 18 lesson 02).
- [ ] **Untrusted content (retrieved docs, tool results, page text) is treated as a potential indirect-injection vector**, never blindly followed as instructions (Module 18 lesson 01).
- [ ] **A red-team test exists proving each defense holds**, kept as a living regression suite, not a one-time check (Module 18 lesson 03's four-step process: scenario → failing test → patch → passing test).
- [ ] **Step and cost budgets are enforced**, both per-agent and system-wide for multi-agent systems (Module 04, Module 12 lesson 02).
- [ ] **Sandboxed code/shell execution only** -- never `exec()`/`eval()` on model-generated input (Module 13 lesson 01).

See: `curriculum/18-security-and-safety/README.md`.
