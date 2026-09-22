"""Run: uv run python curriculum/02-talking-to-llms/examples/cost_estimate_demo.py

Back-of-envelope daily cost estimate across providers, using this repo's verified
pricing table. See lessons/05-cost-and-latency.md.
"""

from __future__ import annotations

from shared.llm.pricing import PRICING, estimate_cost

CALLS_PER_DAY = 10_000
AVG_INPUT_TOKENS = 2_000
AVG_OUTPUT_TOKENS = 500


def main() -> None:
    print(
        f"{CALLS_PER_DAY:,} calls/day, avg {AVG_INPUT_TOKENS} input + "
        f"{AVG_OUTPUT_TOKENS} output tokens each\n"
    )
    for provider, price in PRICING.items():
        per_call = estimate_cost(provider, AVG_INPUT_TOKENS, AVG_OUTPUT_TOKENS)
        daily = per_call * CALLS_PER_DAY
        print(f"{provider:>10} ({price.model:<16}): ${per_call:.6f}/call -> ${daily:,.2f}/day")


if __name__ == "__main__":
    main()
