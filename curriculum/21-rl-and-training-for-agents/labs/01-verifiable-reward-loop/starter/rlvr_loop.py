"""Lab 21.01: a verifiable reward function plus GRPO-style group-relative
advantage computation over sampled candidates. See ../README.md for the
full spec.

This is illustrative of RLVR/GRPO's reward and advantage math -- it does
NOT implement a real policy-gradient update or train any model weights.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/21-rl-and-training-for-agents/labs/01-verifiable-reward-loop/tests
"""

from __future__ import annotations

from shared.sandbox.code_sandbox import (
    run_python,  # noqa: F401 -- used once you implement verify_math_answer below
)


def verify_math_answer(candidate_code: str, target: int) -> float:
    """Run `candidate_code` (a Python expression) via
    shared.sandbox.code_sandbox.run_python(f"print({candidate_code})").
    Return 1.0 if it runs successfully and prints exactly `target` (as an
    int), else 0.0. Never raise -- a malformed candidate or non-integer
    output is just a reward of 0.0.

    TODO: implement this.
    """
    raise NotImplementedError


def group_relative_advantages(rewards: list[float]) -> list[float]:
    """Return [(r - mean(rewards)) / std(rewards) for r in rewards]
    (population std, i.e. divide the variance sum by n, not n-1). If
    std(rewards) == 0 (every candidate scored identically), return
    [0.0] * len(rewards) instead of dividing by zero.

    TODO: implement this.
    """
    raise NotImplementedError


def best_candidate(candidates: list[str], advantages: list[float]) -> str:
    """Return the candidate string with the highest advantage.

    TODO: implement this.
    """
    raise NotImplementedError


def run_verifiable_reward_loop(candidates: list[str], target: int) -> dict:
    """For each candidate, compute its reward via verify_math_answer, then
    the group's advantages via group_relative_advantages. Return
    {"candidates": candidates, "rewards": [...], "advantages": [...], "best": <str>}.

    TODO: implement this.
    """
    raise NotImplementedError
