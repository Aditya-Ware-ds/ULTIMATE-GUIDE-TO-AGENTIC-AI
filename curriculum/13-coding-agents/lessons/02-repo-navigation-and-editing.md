# Repo navigation and editing

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Design `read_file`/`write_file` tools that are scoped to a single repository root.
- Explain why path-traversal validation is a required part of a file-editing tool, not an edge case.
- Give a coding agent only the file operations a task actually needs.

## Intuition

A coding agent's most basic capability -- reading and writing files -- is
also its most dangerous if left unscoped. Module 03's tool-design lesson
already established that a tool's *interface* shapes what an agent can do;
here that principle has real teeth: a `write_file(path, content)` tool that
accepts any path can overwrite anything the underlying process can reach,
not just files inside the repo the agent is supposed to be working on.

## The concept

### Scoping file tools to a repo root

```python
from pathlib import Path


def _resolve_within_repo(repo_root: Path, relative_path: str) -> Path:
    candidate = (repo_root / relative_path).resolve()
    if not candidate.is_relative_to(repo_root.resolve()):
        raise ValueError(f"Path {relative_path!r} escapes the repo root")
    return candidate


def read_file(repo_root: Path, relative_path: str) -> str:
    return _resolve_within_repo(repo_root, relative_path).read_text()


def write_file(repo_root: Path, relative_path: str, content: str) -> str:
    path = _resolve_within_repo(repo_root, relative_path)
    path.write_text(content)
    return f"Wrote {len(content)} characters to {relative_path}"
```

`_resolve_within_repo` is doing the actual security work: `..` segments, a
leaked absolute path, or a symlink pointing outside `repo_root` would all
resolve to something outside `repo_root`, and `is_relative_to` catches every
one of those cases the same way, rather than trying to pattern-match on
`".."` in the string (which is easy to get wrong -- e.g. a path that's
technically safe but contains `".."` as part of a filename).

### Narrow the toolset to the task

A general-purpose coding agent might need `list_files`, `read_file`,
`write_file`, and a search tool. This module's lab needs only `read_file`,
`write_file`, and `run_tests` (lesson 03) -- per Module 03's tool-design
lesson, a smaller, well-scoped toolset is easier for the model to use
correctly and easier for you to reason about than a large general one "just
in case" it's needed.

### Editing vs. rewriting

`write_file` above replaces a file's *entire* contents -- the model has to
regenerate the whole file even to fix one line, which wastes tokens
(Module 02's cost lesson) and risks the model silently dropping unrelated
content it was supposed to leave untouched. Real coding agents typically
expose a more surgical edit primitive (e.g. "replace this exact snippet with
this one," matching this repo's own `Edit` tool) precisely to avoid full
in-place rewrites for small changes -- this module's lab uses whole-file
writes for simplicity, but a production coding agent should not.

## Deeper: this is the same sandboxing discipline as lesson 01, applied to files

Just as `shared/sandbox/shell_sandbox.py` allowlists *commands*, a
repo-scoped file tool allowlists *paths* -- both are the same underlying
idea (least privilege, a hard boundary the agent's mistakes or a
manipulated response can't cross) applied to a different resource. Module 18
generalizes this further (least-privilege tool permissions as a security
practice, not just a coding-agent one).

## When not to use this

Don't add path-traversal validation to a tool that already only ever
receives paths your own code constructs (never a model-supplied path
string) -- the validation exists specifically because the *model* chooses
the path argument here.

## Common mistakes

- Checking for `".."` in the path string instead of resolving the full path
  and checking `is_relative_to` -- string checks miss symlinks, absolute
  paths, and other ways to escape the root that don't literally contain
  `".."`.
- Giving the agent a `write_file` tool with no corresponding `read_file` --
  an agent that can't see current file contents before editing will
  regularly overwrite content it didn't mean to touch.
- Rewriting an entire large file to change one line, burning tokens and
  risking accidental content loss, instead of a smaller, targeted edit
  operation.

## Key takeaways

- Always resolve a model-supplied relative path against the repo root and verify it's still inside that root before reading or writing.
- Give a coding agent only the file tools its specific task needs, not a maximal general-purpose set.
- Whole-file rewrites are simple but costly and risky for small changes -- acceptable for this module's lab, not for production use.

## Lab

[`labs/01-fix-the-failing-test/`](../labs/01-fix-the-failing-test/README.md)
