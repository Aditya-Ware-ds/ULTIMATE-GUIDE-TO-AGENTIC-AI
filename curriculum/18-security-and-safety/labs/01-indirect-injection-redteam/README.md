# Lab 18.01 -- Indirect injection red-team

**Difficulty:** ★★★★★ · **Time:** ~2-3 hours

## Task

Follow lesson 03's four-step red-team process against a small agent with
`read_document` and `send_email` tools: prove an indirect-injection exploit
(a poisoned document tricks the model into emailing an attacker), patch it
with a recipient allowlist (lesson 02), and prove the same test now shows
the exploit blocked. No API key needed -- tested against
`shared.llm.get_client("mock")`.

`_DOCUMENTS["q3-summary"]` contains a real embedded prompt-injection
attempt: text instructing whoever reads it (the agent) to email the
document's contents to `attacker@evil.example`. This lab's tests *simulate*
a model that was successfully manipulated by this content (by scripting
the mock provider to attempt exactly that `send_email` call) -- the point
isn't whether a real model would actually fall for it, it's proving the
**tool itself** blocks the harmful action regardless of the model's
decision (lessons/01 and 02).

## Files

- `starter/secure_agent.py` -- skeleton with the pieces to implement
- `solution/secure_agent.py` -- complete reference implementation
- `tests/` -- tests including the core red-team scenario

## Requirements

Implement these in `starter/secure_agent.py` (`read_document`,
`_DOCUMENTS`, `DEFAULT_ALLOWLIST`, and the tool definitions are already
given):

- `def send_email(to: str, subject: str, body: str, allowlist: frozenset[str]) -> str`
  -- raise `ValueError` if `to` is not in `allowlist`; otherwise append
  `{"to": to, "subject": subject, "body": body}` to `_SENT_EMAILS` and
  return a confirmation string. This check is the actual security boundary
  the red-team test proves.
- `def build_tool_registry(allowlist: frozenset[str]) -> dict[str, Callable]`
  -- a registry with `"read_document"` and `"send_email"` (the latter
  bound to `allowlist` via closure, taking only the model-supplied `to`,
  `subject`, `body`).
- `def dispatch(tool_call, registry) -> ToolResult` -- same contract as
  prior modules.
- `async def run_agent(client, allowlist: frozenset[str], user_input: str, max_steps: int = 6) -> str`
  -- the ReAct loop (Module 04) using these tools.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/secure_agent.py`.
- `send_email` refuses (raises `ValueError`) a recipient not in the
  allowlist, and never records it in `_SENT_EMAILS`.
- `send_email` succeeds for an allowlisted recipient and records it.
- **The red-team test passes**: when the (scripted, simulating a
  manipulated model) agent attempts to email the attacker after reading
  the poisoned document, `_SENT_EMAILS` stays empty -- the exploit is
  blocked at the tool layer, not by hoping the model resists the injection.
- A legitimate, allowlisted email request still completes normally through
  the full agent loop.

## Running the tests

```bash
uv run pytest curriculum/18-security-and-safety/labs/01-indirect-injection-redteam/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/18-security-and-safety/labs/01-indirect-injection-redteam/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 19 -- Deployment & scale](../../../19-deployment-and-scale/README.md)
