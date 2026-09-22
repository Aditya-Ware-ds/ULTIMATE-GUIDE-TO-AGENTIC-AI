"""Run: uv run python curriculum/03-tool-use/examples/retry_demo.py

Shows a bounded exponential-backoff retry around a flaky operation, and that it
gives up (raising) after max_attempts. See lessons/03-error-handling-and-retries.md.
"""

from __future__ import annotations

import random


class TransientError(Exception):
    pass


def call_with_retry(function, *args, max_attempts: int = 3, sleep=lambda _: None, **kwargs):
    last_exception: Exception | None = None
    for attempt in range(max_attempts):
        try:
            return function(*args, **kwargs)
        except TransientError as exc:
            last_exception = exc
            print(f"  attempt {attempt + 1} failed: {exc}")
            sleep(2**attempt)
    raise last_exception


def make_flaky_function(fail_times: int):
    calls = {"count": 0}

    def flaky() -> str:
        calls["count"] += 1
        if calls["count"] <= fail_times:
            raise TransientError(f"simulated transient failure #{calls['count']}")
        return "success"

    return flaky


def main() -> None:
    print("Case 1: succeeds on the 2nd attempt")
    result = call_with_retry(make_flaky_function(fail_times=1), max_attempts=3)
    print(f"  result: {result}\n")

    print("Case 2: never succeeds, exhausts all attempts")
    try:
        call_with_retry(make_flaky_function(fail_times=99), max_attempts=3)
    except TransientError as exc:
        print(f"  gave up after 3 attempts: {exc}")


if __name__ == "__main__":
    random.seed(0)
    main()
