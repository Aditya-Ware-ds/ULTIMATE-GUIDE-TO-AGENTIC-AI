# Module 18 -- Security & safety

**Difficulty:** ★★★★★ · **Time estimate:** 6-8 hours

## Objectives

By the end of this module you can:

- Explain direct and indirect prompt injection, and why indirect injection is the harder problem for tool-using agents.
- Design tool permissions (allowlists, least privilege) that contain an exploit's blast radius even when the model itself is successfully manipulated.
- Name the current OWASP Top 10 for LLM Applications risks and where agentic-specific security guidance fits alongside it.
- Red-team your own agent: prove an exploit works with a failing test, patch it, prove the same test now passes.

## Prerequisites

[Module 17 -- Observability & debugging](../17-observability-and-debugging/README.md)

## Why this module exists

Every prior module that added a capability -- Module 13's file tools,
Module 14's browser navigation, this repo's MCP/tool integrations in
Module 10 -- also quietly added an allowlist or a scoping check
(`resolve_within_repo`, a URL allowlist, `DEFAULT_ALLOWED_COMMANDS`). This
module names that recurring pattern directly and gives it its full security
framing: those weren't incidental implementation details, they were the
actual defense against a model doing something it shouldn't, whether from a
mistake or from a successful manipulation. The lab proves this concretely
by red-teaming an agent with a real indirect-injection scenario.

## Contents

- [`lessons/01-prompt-injection.md`](lessons/01-prompt-injection.md)
- [`lessons/02-tool-permissions-and-least-privilege.md`](lessons/02-tool-permissions-and-least-privilege.md)
- [`lessons/03-owasp-and-red-teaming.md`](lessons/03-owasp-and-red-teaming.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed)
- [`labs/01-indirect-injection-redteam/`](labs/01-indirect-injection-redteam/) -- prove an indirect-injection exploit, then patch and re-prove it's blocked
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 19 -- Deployment & scale](../19-deployment-and-scale/README.md)
