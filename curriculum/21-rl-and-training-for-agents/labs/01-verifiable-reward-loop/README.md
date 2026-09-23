# Lab 21.01 -- Verifiable reward loop

**Difficulty:** ★★★★★ · **Time:** ~2 hours

## Task

Implement a verifiable reward function for a toy math task and a
GRPO-style group-relative advantage computation over a group of sampled
candidates -- entirely offline, no API key, no training, no GPU. This is
illustrative of RLVR/GRPO's reward and advantage math specifically (see
lessons/01 and 03); it does **not** implement a real policy-gradient update
or train any model weights.

## Files

- `starter/rlvr_loop.py` -- skeleton with the pieces to implement
- `solution/rlvr_loop.py` -- complete reference implementation
- `tests/` -- tests that exercise the reward function and the GRPO formula

## Requirements

Implement these in `starter/rlvr_loop.py`:

- `def verify_math_answer(candidate_code: str, target: int) -> float` --
  run `candidate_code` via
  `shared.sandbox.code_sandbox.run_python(f"print({candidate_code})")`.
  Return `1.0` if it runs successfully and prints exactly `target` (as an
  int), else `0.0`. Never raise -- a malformed candidate or non-integer
  output is just a reward of `0.0`.
- `def group_relative_advantages(rewards: list[float]) -> list[float]` --
  GRPO's real formula: `(r - mean(rewards)) / std(rewards)` for each `r`
  (population std). If `std(rewards) == 0` (every candidate scored
  identically), return `[0.0] * len(rewards)` instead of dividing by zero.
- `def best_candidate(candidates: list[str], advantages: list[float]) -> str`
  -- the candidate with the highest advantage.
- `def run_verifiable_reward_loop(candidates: list[str], target: int) -> dict`
  -- compute rewards, then advantages, then return
  `{"candidates": ..., "rewards": ..., "advantages": ..., "best": ...}`.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/rlvr_loop.py`.
- `verify_math_answer` never raises, even for syntactically invalid or
  non-integer-producing candidates -- it always returns a float reward.
- `group_relative_advantages` matches the exact GRPO formula (verified
  against Hugging Face TRL's current docs): for rewards `[1.0, 0.0, 1.0,
  0.0]`, advantages are `[1.0, -1.0, 1.0, -1.0]`.
- `group_relative_advantages` handles the zero-standard-deviation case
  without a `ZeroDivisionError`.
- `run_verifiable_reward_loop` correctly ranks correct candidates above
  incorrect ones via their advantages.

## Running the tests

```bash
uv run pytest curriculum/21-rl-and-training-for-agents/labs/01-verifiable-reward-loop/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/21-rl-and-training-for-agents/labs/01-verifiable-reward-loop/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 22 -- Long-horizon & autonomous agents](../../../22-long-horizon-and-autonomous-agents/README.md)
