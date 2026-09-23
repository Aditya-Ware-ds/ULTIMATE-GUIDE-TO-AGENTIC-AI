# Threat model -- Production coding agent

Following Module 18's four-step red-team process (pick a realistic
scenario, prove it with a test, patch, prove the fix), applied here to a
coding agent's specific attack surface. Every threat below maps to a
specific, currently-passing test in `tests/` -- per Module 18 lesson 03,
these are kept as a living regression suite, not a one-time check.

## Threat 1: path traversal via a malicious `relative_path`

**Scenario**: the model (whether through its own error or a successful
indirect-injection attempt via a poisoned task description or file
content, per Module 18 lesson 01) is induced to call
`write_file(relative_path="../../etc/passwd", content=...)` or a similar
path designed to escape the sandboxed repo directory.

**Defense**: `resolve_within_repo` (Module 13 lesson 02's pattern) resolves
the full path and checks `is_relative_to(repo_root.resolve())`, raising
`ValueError` for any path that escapes the root -- checked by full path
resolution, not a string match for `".."`, so it also catches absolute
paths and other escape routes a naive check would miss.

**Proof**: `test_resolve_within_repo_rejects_path_traversal`.

## Threat 2: arbitrary shell command execution

**Scenario**: if a future version of this agent exposed a more general
"run a shell command" tool instead of the fixed `run_tests`, a
manipulated model could attempt to run an arbitrary, harmful command.

**Defense**: this capstone deliberately exposes **no general shell-command
tool at all** -- `run_tests` always runs exactly `pytest -q`, nothing else,
via `shared.sandbox.shell_sandbox.run_shell`'s allowlist mechanism (Module
13 lesson 01). The narrowest possible action vocabulary (Module 14 lesson
01's "small, typed action vocabulary" principle) is the actual defense
here: there is no broader command surface to exploit in the first place.

**Proof**: by construction -- `TOOLS` (in both `starter/coding_agent.py`
and `solution/coding_agent.py`) contains exactly `read_file`, `write_file`,
and `run_tests`; there is no shell-command tool to audit for this threat.

## Threat 3: a false claim of success masking an unfixed bug

**Scenario**: the model produces a final text response claiming the bug is
fixed, without the underlying repo's tests actually passing -- either
because it gave up, misunderstood the bug, or was manipulated into a
premature "done" claim.

**Defense**: `run_coding_agent` never trusts the model's own final message
as the success signal -- it independently re-runs the sandboxed test suite
after the loop ends and reports `"status"` based on that mechanical result
alone (Module 12 lesson 02's "explicit status, not inferred success,"
applied here to a mechanical check instead of a worker's self-report).

**Proof**: `test_run_coding_agent_does_not_trust_a_false_claim_of_success`.

## Threat 4: an unbounded, runaway agent loop

**Scenario**: a repo whose bug the agent can't figure out could otherwise
loop indefinitely, alternating between wrong fixes, consuming unbounded
cost with no guarantee of ever converging.

**Defense**: `max_steps` bounds the loop (Module 04's stopping-condition
discipline); hitting it still runs the independent test check and reports
`"status": "failed"` explicitly, rather than looping forever or returning
an ambiguous result.

**Proof**: `test_run_coding_agent_stops_at_max_steps_and_still_reports_failed`.

## Threat 5: the eval harness itself mutating the checked-in sample repos

**Scenario**: if `run_eval` ran the agent directly against
`sample_repo/{name}/` instead of a copy, a buggy or malicious agent run
could corrupt the checked-in template repos, breaking every subsequent
test/eval run and polluting the git history.

**Defense**: `run_eval` copies each repo into a fresh
`tempfile.TemporaryDirectory()` before running the agent against it,
identical to Module 13's `repo_copy` fixture pattern.

**Proof**: implicit in every eval-harness test passing repeatedly without
the checked-in `sample_repo/` templates changing -- `git status` after
running the full test suite should show no modification to any file under
`sample_repo/`.

## What this threat model does not cover

This capstone's agent only runs a fixed test command (`pytest -q`) and
never executes arbitrary model-generated Python directly (unlike Module
13's data-analysis-adjacent labs or Module 21's RLVR lab) -- so threats
specific to arbitrary code execution inside the sandbox (beyond what
`pytest` itself can do) are out of scope for this specific agent's actual
capability surface. A coding agent with a broader capability set (e.g. a
general "run this script" tool) would need the additional analysis Module
13 lesson 01 and Module 21 lesson 01 give to that broader surface.
