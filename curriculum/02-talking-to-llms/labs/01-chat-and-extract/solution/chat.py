"""Lab 02.01: chat loop, structured extraction, and cost estimation.
Reference solution. See ../README.md.
"""

from __future__ import annotations

import json

import jsonschema

from shared.llm import LLMClient, Message, Role
from shared.llm.pricing import estimate_cost
from shared.llm.types import Usage

_ROLE_BY_NAME = {"user": Role.USER, "assistant": Role.ASSISTANT}


def build_messages(system_prompt: str, history: list[tuple[str, str]]) -> list[Message]:
    messages = [Message(role=Role.SYSTEM, content=system_prompt)]
    for role_name, content in history:
        messages.append(Message(role=_ROLE_BY_NAME[role_name], content=content))
    return messages


async def chat_once(
    client: LLMClient,
    system_prompt: str,
    history: list[tuple[str, str]],
    user_input: str,
) -> str:
    history.append(("user", user_input))
    messages = build_messages(system_prompt, history)
    response = await client.complete(messages)
    reply_text = response.message.content or ""
    history.append(("assistant", reply_text))
    return reply_text


async def extract_structured(client: LLMClient, text: str, schema: dict) -> dict:
    messages = [Message(role=Role.USER, content=f"Extract structured data as JSON from: {text}")]
    response = await client.complete(messages, response_schema=schema)
    data = json.loads(response.message.content or "")
    jsonschema.validate(data, schema)
    return data


async def stream_and_collect(client: LLMClient, messages: list[Message]) -> str:
    full_text = ""
    async for chunk in client.stream(messages):
        if chunk.delta:
            full_text += chunk.delta
    return full_text


def estimate_call_cost(provider: str, usage: Usage) -> float:
    return estimate_cost(provider, usage.input_tokens, usage.output_tokens)
