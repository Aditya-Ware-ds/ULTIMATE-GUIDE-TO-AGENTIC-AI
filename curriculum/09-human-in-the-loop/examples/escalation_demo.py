"""Run: uv run python curriculum/09-human-in-the-loop/examples/escalation_demo.py

Shows an escalation triggered by hitting a step limit, with a summary of what
was attempted instead of a bare error. See lessons/03-escalation-and-ux.md.
No API key needed.
"""

from __future__ import annotations


def should_escalate(step_count: int, max_steps: int, out_of_scope: bool) -> bool:
    return step_count >= max_steps or out_of_scope


def build_escalation_summary(attempted_steps: list[str], reason: str) -> str:
    steps_text = "\n".join(f"  {i + 1}. {step}" for i, step in enumerate(attempted_steps))
    return (
        f"Escalating to a human. Reason: {reason}\n"
        f"Steps already attempted:\n{steps_text}\n"
        "Please review the above before starting fresh."
    )


def main() -> None:
    attempted_steps = [
        "Searched documentation for 'refund policy exception'",
        "Searched documentation for 'manager override refund'",
        "Attempted to classify request as standard refund (no match)",
    ]

    if should_escalate(step_count=3, max_steps=3, out_of_scope=False):
        print(build_escalation_summary(attempted_steps, reason="hit max_steps without resolving"))
    else:
        print("No escalation needed.")

    print()
    print("--- Bad escalation UX, for comparison ---")
    print("Error: could not complete task.")


if __name__ == "__main__":
    main()
