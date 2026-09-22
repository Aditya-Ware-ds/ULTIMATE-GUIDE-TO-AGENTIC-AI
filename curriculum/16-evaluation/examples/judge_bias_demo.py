"""Run: uv run python curriculum/16-evaluation/examples/judge_bias_demo.py

Shows position bias in a pairwise LLM-as-judge comparison, and the
swap-and-check mitigation lesson 02 describes. No API key needed -- the mock
provider is scripted to (unrealistically, but illustratively) prefer
whichever answer is presented first, exactly the failure mode being
demonstrated.
"""

from __future__ import annotations

import asyncio
import json

from shared.llm import Message, Role, get_client


async def compare(client, question: str, answer_a: str, answer_b: str) -> str:
    schema = {
        "type": "object",
        "properties": {"winner": {"type": "string", "enum": ["A", "B"]}},
        "required": ["winner"],
    }
    response = await client.complete(
        [
            Message(
                role=Role.USER,
                content=f"Question: {question}\nAnswer A: {answer_a}\nAnswer B: {answer_b}\n"
                "Which answer is better?",
            )
        ],
        response_schema=schema,
    )
    return json.loads(response.message.content)["winner"]


async def compare_with_position_check(client, question: str, answer_a: str, answer_b: str) -> str:
    first_pass = await compare(client, question, answer_a, answer_b)
    # Swap the order and compare again.
    second_pass_raw = await compare(client, question, answer_b, answer_a)
    second_pass = "B" if second_pass_raw == "A" else "A"  # translate back to original labels

    if first_pass == second_pass:
        return first_pass
    return "inconclusive (judge disagreed after swapping order)"


async def main() -> None:
    question = "What is the capital of France?"
    answer_a = "Paris"
    answer_b = "Paris, the capital of France, is a beautiful city on the Seine."

    client = get_client("mock")
    # A biased judge that always prefers whichever answer is presented first.
    client.provider.add_text(json.dumps({"winner": "A"}))
    naive_winner = await compare(client, question, answer_a, answer_b)
    print(f"Naive single comparison winner: {naive_winner} (both answers are equally correct!)")

    client2 = get_client("mock")
    client2.provider.add_text(json.dumps({"winner": "A"}))  # first pass: A presented first, wins
    client2.provider.add_text(json.dumps({"winner": "A"}))  # second pass: B presented first, wins
    checked_winner = await compare_with_position_check(client2, question, answer_a, answer_b)
    print(f"Swap-checked result: {checked_winner!r} (position bias correctly detected)")


if __name__ == "__main__":
    asyncio.run(main())
