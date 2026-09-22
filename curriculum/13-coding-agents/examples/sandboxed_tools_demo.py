"""Run: uv run python curriculum/13-coding-agents/examples/sandboxed_tools_demo.py

Shows the three building blocks a coding agent needs -- a repo-scoped
read_file/write_file pair and a sandboxed test runner -- working end to end
against a tiny throwaway repo. See lessons/01-sandboxed-code-execution.md and
lessons/02-repo-navigation-and-editing.md. No API key needed.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from shared.sandbox.shell_sandbox import run_shell


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


def run_tests(repo_root: Path) -> str:
    result = run_shell("pytest -q", cwd=repo_root)
    return result.stdout + result.stderr


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        repo_root = Path(tmp)
        write_file(repo_root, "add.py", "def add(a, b):\n    return a - b  # bug: should be +\n")
        write_file(
            repo_root,
            "test_add.py",
            "from add import add\n\ndef test_add():\n    assert add(2, 3) == 5\n",
        )

        print("Before the fix:")
        print(run_tests(repo_root))

        print("Reading the buggy file:")
        print(read_file(repo_root, "add.py"))

        write_file(repo_root, "add.py", "def add(a, b):\n    return a + b\n")

        print("After the fix:")
        print(run_tests(repo_root))

        print("Path-traversal attempt is rejected:")
        try:
            read_file(repo_root, "../../etc/passwd")
        except ValueError as exc:
            print(f"  {exc}")


if __name__ == "__main__":
    main()
