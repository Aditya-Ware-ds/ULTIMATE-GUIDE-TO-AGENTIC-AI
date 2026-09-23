"""Run (from the repo root):
    uv run python curriculum/22-long-horizon-and-autonomous-agents/\\
        examples/reliability_math_demo.py

Shows how naive multi-step success probability compounds, and how
checkpointing changes the effective cost of a failure from "redo
everything" to "redo one step." No API key needed. See
lessons/02-reliability-math.md.
"""

from __future__ import annotations


def naive_chain_success_probability(step_success_probability: float, num_steps: int) -> float:
    return step_success_probability**num_steps


def expected_steps_redone_on_failure(num_steps: int, checkpointed: bool) -> float:
    """Illustrative only: without checkpointing, a failure anywhere in the
    chain means redoing all num_steps; with checkpointing, it means redoing
    just the one failed step.
    """
    return float(num_steps) if not checkpointed else 1.0


def main() -> None:
    p = 0.95
    print(f"Per-step success probability: {p}")
    print(f"{'Steps':>6} {'Chain success':>15}")
    for n in (1, 5, 10, 20, 50):
        chain_p = naive_chain_success_probability(p, n)
        print(f"{n:>6} {chain_p:>14.1%}")

    print()
    n = 50
    print(f"For a {n}-step plan, on a single step's failure:")
    without = expected_steps_redone_on_failure(n, checkpointed=False)
    with_checkpoint = expected_steps_redone_on_failure(n, checkpointed=True)
    print(f"  Without checkpointing: redo {without:.0f} steps")
    print(f"  With checkpointing:    redo {with_checkpoint:.0f} step")


if __name__ == "__main__":
    main()
