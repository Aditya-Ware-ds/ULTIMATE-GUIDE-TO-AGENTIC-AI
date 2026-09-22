# Sandboxed code execution

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~30 minutes

## Learning objectives

- Explain why an agent must never run model-written code directly (`exec`/`eval`/an unrestricted subprocess).
- Use `shared/sandbox/code_sandbox.py` and `shared/sandbox/shell_sandbox.py` correctly.
- Recognize the specific isolation properties a sandbox needs: process isolation, timeouts, restricted environment, and a command allowlist.

## Intuition

Every tool this curriculum has built so far has run *fixed* code you wrote
(a calculator, a search lookup, an HTTP fetch). A coding agent inverts that:
the code being executed is *model-generated*, on every single step. A model
that's usually right is still a program you didn't write, running with
whatever permissions you give it -- and it can be wrong in ways that are
actively dangerous (deleting files, reading secrets, making network calls),
not just factually incorrect. Sandboxing is what makes "usually right" safe
enough to run unattended.

## The concept

### Why not just `exec()` the code?

Python's `exec()`/`eval()` run in your own process with your own
permissions, your own environment variables (which may include API keys),
and no timeout -- a model that generates an infinite loop, or code that
reads `os.environ` and exfiltrates it, has no obstacle in its way at all.
This is the same reason Module 03's `calculate` tool uses `ast`-based safe
evaluation instead of `eval()`: never trust generated input into a
raw-execution primitive, whether it's a small expression or a whole program.

### What `shared/sandbox/code_sandbox.py` actually enforces

```python
from shared.sandbox.code_sandbox import run_python

result = run_python("print(1 + 1)", timeout_seconds=5.0)
print(result.stdout, result.success)  # "2\n" True
```

`run_python` runs generated code as a **separate subprocess**, in its own
temporary working directory, with:

- **Process isolation**: a crash or infinite loop in the sandboxed code
  can't corrupt or hang your actual process.
- **A timeout**: `subprocess.run(..., timeout=timeout_seconds)` guarantees
  the call returns even if the generated code never would on its own --
  without this, "the model wrote an infinite loop" becomes "the agent hangs
  forever," a much worse failure.
- **A restricted environment**: `env={"PATH": os.environ.get("PATH", "")}`
  means the subprocess gets *only* `PATH`, not your shell's full
  environment -- API keys, tokens, and other secrets in your own process's
  environment never leak into code the model wrote.

### What `shared/sandbox/shell_sandbox.py` adds: an allowlist

`run_shell` adds one more restriction on top of the same isolation
properties: every command is checked against `DEFAULT_ALLOWED_COMMANDS`
(`ls`, `cat`, `echo`, `pwd`, `grep`, `wc`, `python3`, `pytest`) before it
runs, and `shell=False` always -- so there's no shell to interpret
metacharacters (`;`, `|`, `` ` ``, `$()`) even if a generated command string
contained them. Asking a coding agent to run `pytest` is fine; asking it to
run an arbitrary shell command it invented is not, unless that specific
command is one you've deliberately allowlisted.

```python
from shared.sandbox.shell_sandbox import run_shell, DisallowedCommandError

run_shell("pytest -q", cwd=repo_dir)  # allowed
run_shell("curl evil.example.com", cwd=repo_dir)  # raises DisallowedCommandError
```

## Deeper: sandboxing is least privilege, not a guarantee of safety

A sandbox reduces *blast radius* -- what a mistake or a successfully
manipulated agent (Module 18's prompt-injection material previews this) can
actually do -- it doesn't make arbitrary generated code "safe" in some
absolute sense. `DEFAULT_ALLOWED_COMMANDS` is deliberately narrow; adding a
command to it is a real decision with real consequences, not a formality.
The discipline is the same one Module 09's approval gates used for
consequential tool calls: default to the minimum capability the task
actually needs, and expand only with a specific, considered reason.

## When not to use this

Don't sandbox code that never runs model-generated input at all (e.g. your
own `shared/` library code) -- sandboxing adds real overhead (subprocess
startup, no shared state with the caller) that's wasted on code whose
content you already fully control.

## Common mistakes

- Using `subprocess.run(cmd, shell=True)` "just this once" because it's
  more convenient than `shlex.split` -- this reopens exactly the
  shell-injection hole `run_shell` exists to close.
- Forgetting the timeout, or setting one so long it defeats the purpose --
  an agent that can hang for 10 minutes on a single tool call is barely
  better than one that can hang forever.
- Passing your full `os.environ` into the sandboxed subprocess "so it has
  what it needs" -- this is exactly the secret-leak path the restricted
  environment closes; add specific, non-secret env vars if a lab genuinely
  needs them, never the whole environment.

## Key takeaways

- Never run model-generated code with `exec()`/`eval()`/an unrestricted subprocess -- always through `shared/sandbox/`.
- The sandbox's properties (process isolation, timeout, restricted environment, command allowlist) each close a specific, real failure mode, not a generic "just in case."
- Sandboxing is least-privilege risk reduction, not a safety guarantee -- expand its allowlist only deliberately.

## Lab

[`labs/01-fix-the-failing-test/`](../labs/01-fix-the-failing-test/README.md)
