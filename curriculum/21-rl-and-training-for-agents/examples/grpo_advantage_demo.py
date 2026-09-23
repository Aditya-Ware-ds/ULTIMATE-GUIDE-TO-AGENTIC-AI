"""Run: uv run python curriculum/21-rl-and-training-for-agents/examples/grpo_advantage_demo.py

Computes GRPO's group-relative advantage for a batch of sampled candidates
with verifiable rewards -- the real formula (reward - group_mean) / group_std,
verified against Hugging Face TRL's current docs. No API key, no training,
no GPU -- this is the reward/advantage math only. See
lessons/03-grpo-and-group-relative-advantages.md.
"""

from __future__ import annotations


def group_relative_advantages(rewards: list[float]) -> list[float]:
    n = len(rewards)
    mean_reward = sum(rewards) / n
    variance = sum((r - mean_reward) ** 2 for r in rewards) / n
    std_reward = variance**0.5
    if std_reward == 0:
        return [0.0] * n
    return [(r - mean_reward) / std_reward for r in rewards]


def main() -> None:
    candidates = [
        "print(2 + 2)",  # correct
        "print(5)",  # incorrect
        "print(2 * 2)",  # correct
        "print(0)",  # incorrect
    ]
    rewards = [1.0, 0.0, 1.0, 0.0]  # verifiable: does it print 4?

    advantages = group_relative_advantages(rewards)

    print("Candidate                Reward   Advantage")
    for candidate, reward, advantage in zip(candidates, rewards, advantages, strict=True):
        print(f"{candidate!r:<25} {reward:>6.1f}   {advantage:>+.3f}")

    print("\nCorrect candidates get a positive advantage (reinforce);")
    print("incorrect candidates get a negative advantage (discourage) --")
    print("computed entirely from the group's own mean and std, no critic model.")


if __name__ == "__main__":
    main()
