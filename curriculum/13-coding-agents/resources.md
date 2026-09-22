# Module 13 resources

Verified 2026-09-22.

- [Claude Code: Best practices](https://code.claude.com/docs/en/best-practices) -- primary source for lesson 04's "explore, plan, code, commit" workflow, "give it a way to verify its work," and context-window management as the primary effectiveness constraint.
- [Claude Code: How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works) -- the agentic loop, tools, and context management this module's lesson 04 references.
- Python `subprocess` docs -- [`subprocess.run`](https://docs.python.org/3/library/subprocess.html#subprocess.run) -- the isolation primitive `shared/sandbox/` is built on (timeout, `shell=False`, restricted `env`).
- [`pathlib.Path.is_relative_to`](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.is_relative_to) -- the check lesson 02's `resolve_within_repo` uses to reject path-traversal attempts robustly.
