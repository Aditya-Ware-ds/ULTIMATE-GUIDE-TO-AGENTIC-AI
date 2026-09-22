"""Run: uv run python curriculum/00-programming-prerequisites/examples/dataclass_demo.py

Shows what @dataclass generates for you, and the mutable-default-argument trap
covered in lessons/01-python-essentials.md.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, object] = field(default_factory=dict)


def main() -> None:
    call_a = ToolCall(id="1", name="get_weather", arguments={"city": "Paris"})
    call_b = ToolCall(id="1", name="get_weather", arguments={"city": "Paris"})

    print("repr (auto-generated):", call_a)
    print("equality (auto-generated __eq__):", call_a == call_b)

    call_c = ToolCall(id="2", name="get_time")
    call_c.arguments["timezone"] = "UTC"
    call_d = ToolCall(id="3", name="get_date")
    print(
        "default_factory keeps arguments independent per instance:",
        call_c.arguments,
        call_d.arguments,
    )


if __name__ == "__main__":
    main()
