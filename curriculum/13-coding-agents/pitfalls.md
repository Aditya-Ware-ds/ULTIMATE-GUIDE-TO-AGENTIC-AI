# Module 13 pitfalls

## Trusting the model's own "it's fixed now" instead of re-running the tests

It's tempting to have `run_coding_agent` return success as soon as the model
stops calling tools, on the theory that "it wouldn't stop unless it thought
it was done." The lab's
`test_run_coding_agent_does_not_trust_a_false_claim_of_success` test exists
specifically to catch this: a model that claims success without ever calling
`write_file` should still get `"status": "failed"`, because the *actual*
tests, re-run independently after the loop ends, are what determines status
-- never the model's text. This is the single most important idea in this
module, and it's easy to accidentally lose if you write `run_coding_agent`
to short-circuit on the model's final message instead of always checking
reality afterward.

## A path-traversal check that works for the test cases but not the general case

It's tempting to write `if ".." in relative_path: raise ValueError(...)` and
move on once the obvious test passes -- but this misses an absolute path
(`/etc/passwd`, no `".."` at all) and doesn't generalize to symlinks. The
robust version resolves the *full* path (`(repo_root / relative_path).resolve()`)
and checks `is_relative_to(repo_root.resolve())` -- one check that correctly
handles every escape route, rather than a growing list of special cases for
each one you happen to think of.

## Forgetting that `run_shell`'s allowlist applies to the *binary name*, not the full command string

`DEFAULT_ALLOWED_COMMANDS` checks `Path(args[0]).name` -- the program being
run, not the full command including its arguments. This means `pytest -q`
and `pytest --collect-only` are both allowed (both start with the `pytest`
binary), which is intended, but it also means the allowlist can't restrict
*which* pytest arguments are used -- if that matters for a task, you need
additional argument-level validation on top of the binary allowlist, not a
replacement for it.

## Running the sandboxed test suite inside this git repo instead of a copied-out temp directory

If you write a coding-agent lab's test fixture to operate on `sample_repo/`
in place (or in a temp directory that's still nested under this project),
the sandboxed `pytest -q` subprocess can pick up *this project's own*
`pyproject.toml` (`[tool.pytest.ini_options]`, `addopts = "-m 'not live'"`,
etc.) instead of running cleanly against just the sample repo -- pytest
walks up parent directories looking for config. Always copy the sample repo
out to a location outside the git tree (e.g. `tempfile.TemporaryDirectory()`,
which lands under the OS's temp directory, not under this repo) before
letting an agent's sandboxed test runs operate on it.
