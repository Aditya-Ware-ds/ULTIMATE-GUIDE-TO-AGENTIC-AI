"""Restricted shell command execution for labs where an agent runs shell commands.

Commands are checked against an explicit allowlist of binaries before executing,
run with a timeout in an isolated working directory, and never with `shell=True`
(no shell-metacharacter injection) -- this is what "least privilege" and "never let
an agent execute shell commands outside a sandbox" look like in code, not just in
a lesson's prose.
"""

from __future__ import annotations

import os
import shlex
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

DEFAULT_ALLOWED_COMMANDS: frozenset[str] = frozenset(
    {"ls", "cat", "echo", "pwd", "grep", "wc", "python3", "pytest"}
)


class DisallowedCommandError(Exception):
    pass


@dataclass
class ShellResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool

    @property
    def success(self) -> bool:
        return self.exit_code == 0 and not self.timed_out


def run_shell(
    command: str,
    *,
    allowed_commands: frozenset[str] = DEFAULT_ALLOWED_COMMANDS,
    timeout_seconds: float = 5.0,
    cwd: Path | None = None,
) -> ShellResult:
    args = shlex.split(command)
    if not args:
        raise ValueError("Empty command")
    binary = Path(args[0]).name
    if binary not in allowed_commands:
        raise DisallowedCommandError(
            f"{binary!r} is not in the sandbox allowlist ({sorted(allowed_commands)}). "
            "Add it explicitly if the lab genuinely needs it -- default to least privilege."
        )
    with tempfile.TemporaryDirectory() as tmp:
        workdir = cwd or Path(tmp)
        try:
            completed = subprocess.run(
                args,
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                shell=False,
                env={"PATH": os.environ.get("PATH", "")},
            )
            return ShellResult(
                stdout=completed.stdout,
                stderr=completed.stderr,
                exit_code=completed.returncode,
                timed_out=False,
            )
        except subprocess.TimeoutExpired as exc:
            return ShellResult(
                stdout=exc.stdout or "", stderr=exc.stderr or "", exit_code=-1, timed_out=True
            )
