import pytest

from shared.sandbox.code_sandbox import run_python
from shared.sandbox.shell_sandbox import DisallowedCommandError, run_shell


def test_run_python_captures_stdout():
    result = run_python("print('hello from sandbox')")

    assert result.success
    assert "hello from sandbox" in result.stdout


def test_run_python_captures_nonzero_exit_and_stderr():
    result = run_python("import sys; sys.exit(3)")

    assert not result.success
    assert result.exit_code == 3


def test_run_python_times_out():
    result = run_python("import time; time.sleep(5)", timeout_seconds=0.2)

    assert result.timed_out
    assert not result.success


def test_run_python_does_not_leak_arbitrary_env_vars(monkeypatch):
    monkeypatch.setenv("SUPER_SECRET_API_KEY", "sk-should-not-leak")

    result = run_python("import os; print(os.environ.get('SUPER_SECRET_API_KEY'))")

    assert "sk-should-not-leak" not in result.stdout


def test_run_shell_allows_allowlisted_command():
    result = run_shell("echo hello")

    assert result.success
    assert "hello" in result.stdout


def test_run_shell_blocks_non_allowlisted_command():
    with pytest.raises(DisallowedCommandError):
        run_shell("rm -rf /")


def test_run_shell_respects_custom_allowlist():
    with pytest.raises(DisallowedCommandError):
        run_shell("cat foo.txt", allowed_commands=frozenset({"echo"}))
