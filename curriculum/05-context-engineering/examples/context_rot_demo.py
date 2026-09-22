"""Run: uv run python curriculum/05-context-engineering/examples/context_rot_demo.py

Illustrates the SHAPE of the "lost in the middle" positional effect: this does
NOT call a real model and the numbers below are made up for illustration only,
not measured or quoted from any study -- see resources.md for real research
with real numbers. The point is the U-shape, not these specific values.
"""

from __future__ import annotations

# Fabricated numbers, for shape illustration only -- see the module docstring.
POSITION_LABELS = ["start", "1/4", "middle", "3/4", "end"]
ILLUSTRATIVE_ACCURACY = [0.94, 0.85, 0.68, 0.86, 0.93]


def main() -> None:
    print("Made-up 'lost in the middle' curve, for shape illustration only:\n")
    for label, accuracy in zip(POSITION_LABELS, ILLUSTRATIVE_ACCURACY, strict=True):
        bar = "#" * int(accuracy * 40)
        print(f"  {label:>6}: {accuracy:.2f} {bar}")
    print(
        "\nNotice the U-shape: accuracy is highest when the needed fact is near the "
        "start or end of the context, and lowest in the middle -- even though the "
        "fact itself doesn't change, only its position does."
    )


if __name__ == "__main__":
    main()
