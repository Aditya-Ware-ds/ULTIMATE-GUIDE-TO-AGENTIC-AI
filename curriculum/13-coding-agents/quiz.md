# Module 13 quiz

**1. Why must model-generated code never be run with a raw `exec()`/`eval()`?**

<details><summary>Answer</summary>

`exec()`/`eval()` run in your own process, with your own permissions and
environment (including any secrets in `os.environ`), and with no timeout --
a model that generates dangerous or runaway code has nothing standing in
its way. This is the same reasoning behind Module 03's `ast`-based safe
arithmetic evaluation, scaled up to arbitrary code.

</details>

**2. What three isolation properties does `shared/sandbox/code_sandbox.py`'s `run_python` provide?**

<details><summary>Answer</summary>

Process isolation (a subprocess, so a crash/hang can't affect your own
process), a timeout (guarantees the call returns even if the code would
otherwise run forever), and a restricted environment (only `PATH` is
inherited, so secrets in your own environment can't leak into the
sandboxed code).

</details>

**3. Why does `run_shell` check every command against an allowlist and always pass `shell=False`?**

<details><summary>Answer</summary>

The allowlist enforces least privilege -- a coding agent should only be able
to run commands you've deliberately decided are safe, not anything it
invents. `shell=False` means there's no shell to interpret metacharacters
(`;`, `|`, backticks), closing the shell-injection hole that `shell=True`
would open for model-generated command strings.

</details>

**4. Why does a repo-scoped file tool need to resolve the full path and check `is_relative_to`, rather than just checking whether the path string contains `".."`?**

<details><summary>Answer</summary>

A string check for `".."` misses other ways to escape the intended root --
an absolute path, or a symlink that points outside the root -- that don't
literally contain `".."`. Resolving the full path and checking it's still
inside the root catches every case uniformly.

</details>

**5. How does a coding agent's loop differ structurally from Module 04's ReAct loop?**

<details><summary>Answer</summary>

It doesn't, structurally -- it's the same loop (call the model with tools,
dispatch tool calls, repeat until no more tool calls or a step budget is
hit). What differs is the tools (`read_file`/`write_file`/`run_tests`
instead of `search`/`calculate`) and, critically, the stop signal.

</details>

**6. Why is "the model stopped calling tools" not sufficient evidence that a coding agent's task succeeded?**

<details><summary>Answer</summary>

A model can stop calling tools because it (incorrectly) believes it's
finished, not because the bug is actually fixed. A coding agent has a
mechanical check available -- the test suite -- and should independently
re-run it rather than trusting the model's own claim, the same "explicit
status, not inferred success" discipline from Module 12 lesson 02.

</details>

**7. Why is a real test suite a "strictly better" stop signal than an LLM-judge evaluation (Module 08's evaluator-optimizer), when one is available?**

<details><summary>Answer</summary>

A test suite gives a deterministic pass/fail plus the exact failure detail
(which assertion, expected vs. actual) as concrete feedback for the next
edit -- an LLM judge is a probabilistic approximation of correctness, useful
when no mechanical check exists, but strictly worse than a real check when
one does.

</details>

**8. According to current Claude Code guidance, why should exploration be separated from implementation ("explore, then plan, then code")?**

<details><summary>Answer</summary>

Letting an agent jump straight to coding can produce a solution to the
wrong problem -- exploring the relevant code first, then planning an
approach, catches misunderstandings before any files are changed, the same
reasoning Module 08's plan-and-execute lesson gives for agents generally.

</details>

**9. Why is context-window management called the "primary constraint" on a coding agent's effectiveness, per current guidance?**

<details><summary>Answer</summary>

Every file read and command output consumes context, and model performance
degrades as the context window fills -- a single debugging session can burn
tens of thousands of tokens. This is Module 05's context-engineering
material, now identified as the main lever for keeping a coding agent
effective over a long session.

</details>

**10. In this module's lab, why is the sample repo copied into a temp directory outside the git repo before the agent operates on it, rather than editing it in place?**

<details><summary>Answer</summary>

Two reasons: editing the checked-in template in place would make test runs
non-repeatable (each run would start from whatever the previous run left
behind) and pollute the actual git-tracked files; and running `pytest`
inside a directory still nested under this project would pick up this
project's own `pyproject.toml` test configuration, interfering with the
sandboxed test run.

</details>
