"""Lab 21.01: a verifiable reward function plus GRPO-style group-relative
advantage computation over sampled candidates. Reference solution. See
../README.md.

This is illustrative of RLVR/GRPO's reward and advantage math -- it does
NOT implement a real policy-gradient update or train any model weights
(see lessons/03-grpo-and-group-relative-advantages.md's "Deeper" section).
"""

from __future__ import annotations

from shared.sandbox.code_sandbox import run_python


def verify_math_answer(candidate_code: str, target: int) -> float:
    result = run_python(f"print({candidate_code})")
    if not result.success:
        return 0.0
    try:
        return 1.0 if int(result.stdout.strip()) == target else 0.0
    except ValueError:
        return 0.0


def group_relative_advantages(rewards: list[float]) -> list[float]:
    n = len(rewards)
    mean_reward = sum(rewards) / n
    variance = sum((r - mean_reward) ** 2 for r in rewards) / n
    std_reward = variance**0.5
    if std_reward == 0:
        return [0.0] * n
    return [(r - mean_reward) / std_reward for r in rewards]


def best_candidate(candidates: list[str], advantages: list[float]) -> str:
    best_index = max(range(len(candidates)), key=lambda i: advantages[i])
    return candidates[best_index]


def run_verifiable_reward_loop(candidates: list[str], target: int) -> dict:
    rewards = [verify_math_answer(candidate, target) for candidate in candidates]
    advantages = group_relative_advantages(rewards)
    return {
        "candidates": candidates,
        "rewards": rewards,
        "advantages": advantages,
        "best": best_candidate(candidates, advantages),
    }
