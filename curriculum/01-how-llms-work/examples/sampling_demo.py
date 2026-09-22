"""Run: uv run python curriculum/01-how-llms-work/examples/sampling_demo.py

Shows how temperature reshapes a probability distribution over a toy vocabulary,
as covered in lessons/03-sampling-and-decoding.md. No API key needed -- this
works on fixed example logits, not a real model call.
"""

from __future__ import annotations

import math

VOCAB = ["get_weather", "get_time", "search_web", "do_nothing"]
LOGITS = [4.0, 1.0, 0.5, -2.0]  # a model strongly prefers "get_weather" here


def softmax(logits: list[float], temperature: float) -> list[float]:
    scaled = [logit / temperature for logit in logits]
    max_scaled = max(scaled)
    exps = [math.exp(s - max_scaled) for s in scaled]
    total = sum(exps)
    return [e / total for e in exps]


def main() -> None:
    for temperature in (0.1, 1.0, 2.0):
        probs = softmax(LOGITS, temperature)
        print(f"temperature={temperature}")
        for token, prob in sorted(zip(VOCAB, probs, strict=True), key=lambda p: -p[1]):
            bar = "#" * int(prob * 40)
            print(f"  {token:>12}: {prob:.3f} {bar}")
        print()


if __name__ == "__main__":
    main()
