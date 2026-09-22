"""Subprocess-isolated Python execution for labs where an agent writes and runs code.

Every "agent runs code" lab (Module 13 especially) executes model-written code
through this sandbox -- never via a raw exec()/eval() or an unrestricted subprocess
call -- per the ground rule that an agent may never execute code outside a sandbox.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ExecutionResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool

    @property
    def success(self) -> bool:
        return self.exit_code == 0 and not self.timed_out


def run_python(
    code: str, *, timeout_seconds: float = 5.0, cwd: Path | None = None
) -> ExecutionResult:
    """Run `code` as a standalone script in a fresh subprocess with a timeout.

    Runs in its own temp directory unless `cwd` is given. The subprocess only
    inherits PATH from the caller's environment -- no API keys or other secrets
    leak into sandboxed code's os.environ.
    """
    with tempfile.TemporaryDirectory() as tmp:
        workdir = cwd or Path(tmp)
        script_path = workdir / "_sandboxed_script.py"
        script_path.write_text(code)
        try:
            completed = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                env={"PATH": os.environ.get("PATH", "")},
            )
            return ExecutionResult(
                stdout=completed.stdout,
                stderr=completed.stderr,
                exit_code=completed.returncode,
                timed_out=False,
            )
        except subprocess.TimeoutExpired as exc:
            return ExecutionResult(
                stdout=exc.stdout or "", stderr=exc.stderr or "", exit_code=-1, timed_out=True
            )
