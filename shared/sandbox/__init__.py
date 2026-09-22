"""Sandboxed execution primitives every lab uses instead of raw exec()/subprocess calls.

from shared.sandbox import run_python, run_shell
"""

from shared.sandbox.code_sandbox import ExecutionResult, run_python
from shared.sandbox.shell_sandbox import DisallowedCommandError, ShellResult, run_shell

__all__ = [
    "run_python",
    "ExecutionResult",
    "run_shell",
    "ShellResult",
    "DisallowedCommandError",
]
