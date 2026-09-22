"""Run: uv run python curriculum/02-talking-to-llms/examples/structured_output_demo.py

Requests a schema-shaped response from the mock provider, then validates it --
demonstrating that even a "guaranteed" structured output should be validated in
your own code. See lessons/03-structured-outputs.md.
"""

from __future__ import annotations

import asyncio
import json

import jsonschema

from shared.llm import Message, Role, get_client

SCHEMA = {
    "type": "object",
    "properties": {
        "city": {"type": "string"},
        "country": {"type": "string"},
    },
    "required": ["city", "country"],
}


async def main() -> None:
    client = get_client("mock")
    client.provider.add_text('{"city": "Paris", "country": "France"}')

    messages = [Message(role=Role.USER, content="Extract the location: I live in Paris, France.")]
    response = await client.complete(messages, response_schema=SCHEMA)

    data = json.loads(response.message.content)
    jsonschema.validate(data, SCHEMA)
    print("Valid structured output:", data)

    print("\nNow showing what invalid output looks like:")
    invalid_client = get_client("mock")
    invalid_client.provider.add_text('{"city": "Paris"}')  # missing required "country"
    invalid_response = await invalid_client.complete(
        [Message(role=Role.USER, content="...")], response_schema=SCHEMA
    )
    invalid_data = json.loads(invalid_response.message.content)
    try:
        jsonschema.validate(invalid_data, SCHEMA)
    except jsonschema.ValidationError as exc:
        print(f"Validation correctly caught the problem: {exc.message}")


if __name__ == "__main__":
    asyncio.run(main())
