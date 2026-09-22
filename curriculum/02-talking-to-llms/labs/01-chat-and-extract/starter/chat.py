"""Lab 02.01: chat loop, structured extraction, and cost estimation.
See ../README.md for the full spec.

Fill in the five functions below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/02-talking-to-llms/labs/01-chat-and-extract/tests
"""

from __future__ import annotations

import json  # noqa: F401 -- used once you implement extract_structured below

import jsonschema  # noqa: F401 -- used once you implement extract_structured below

from shared.llm import LLMClient, Message, Role  # noqa: F401 -- Role used in build_messages below
from shared.llm.pricing import estimate_cost  # noqa: F401 -- used in estimate_call_cost below
from shared.llm.types import Usage


def build_messages(system_prompt: str, history: list[tuple[str, str]]) -> list[Message]:
    """Build a Message list: system prompt, then one Message per history entry.

    TODO: implement this.
    """
    raise NotImplementedError


async def chat_once(
    client: LLMClient,
    system_prompt: str,
    history: list[tuple[str, str]],
    user_input: str,
) -> str:
    """Append the user's turn, call the model, append its reply, return the reply text.

    TODO: implement this.
    """
    raise NotImplementedError


async def extract_structured(client: LLMClient, text: str, schema: dict) -> dict:
    """Ask the model to extract structured data from `text`, matching `schema`.

    TODO: implement this. Parse as JSON, validate against schema, let exceptions
    propagate.
    """
    raise NotImplementedError


async def stream_and_collect(client: LLMClient, messages: list[Message]) -> str:
    """Consume client.stream(messages) and return the fully concatenated text.

    TODO: implement this.
    """
    raise NotImplementedError


def estimate_call_cost(provider: str, usage: Usage) -> float:
    """Return the estimated USD cost of a call given its token usage.

    TODO: implement this (one line, using shared.llm.pricing.estimate_cost).
    """
    raise NotImplementedError
