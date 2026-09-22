"""Run: uv run python curriculum/00-programming-prerequisites/examples/json_demo.py

Round-trips a tool-definition-shaped dict through JSON, and shows the parse-error
handling you should always wrap around JSON you don't fully control (e.g. from a
model's output), as covered in lessons/02-json-and-data.md.
"""

from __future__ import annotations

import json

TOOL_DEFINITION = {
    "name": "get_weather",
    "description": "Get the current weather for a city",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["city"],
    },
}


def main() -> None:
    text = json.dumps(TOOL_DEFINITION, indent=2)
    print("Serialized:\n", text)

    parsed = json.loads(text)
    assert parsed == TOOL_DEFINITION
    print("\nRound-trip OK. Required fields:", parsed["parameters"]["required"])

    malformed = '{"name": "get_weather", "arguments": {city: "Paris"}}'  # unquoted key
    try:
        json.loads(malformed)
    except json.JSONDecodeError as exc:
        print(f"\nExpected failure on malformed JSON: {exc}")


if __name__ == "__main__":
    main()
