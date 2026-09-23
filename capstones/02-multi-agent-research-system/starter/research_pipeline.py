"""Capstone 2: multi-agent research system. See ../README.md and
../ARCHITECTURE.md for the full spec.

Extends projects/04-multi-agent-content-pipeline/'s researcher/writer/critic
topology (unchanged core logic, given below) with numbered-fact citations,
citation verification, and full tracing (Module 17) of each worker as its
own nested span.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest capstones/02-multi-agent-research-system/tests
"""

from __future__ import annotations

import json
import re  # noqa: F401 -- used once you implement extract_citations below

from shared.llm import Message, Role
from shared.tracing import chat_span, invoke_agent_span  # noqa: F401 -- used below


async def research(client, topic: str) -> dict:
    schema = {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "facts": {"type": "array", "items": {"type": "string"}},
            "reason": {"type": "string"},
        },
        "required": ["status"],
    }
    with chat_span(model=client.default_model, provider="mock") as span:
        response = await client.complete(
            [
                Message(
                    role=Role.USER,
                    content=(
                        f"Find 3 short factual bullet points about: {topic!r}. "
                        'Reply as {"status": "success", "facts": [...]}, or '
                        '{"status": "error", "reason": "..."} if this topic has no '
                        "reliable factual basis."
                    ),
                )
            ],
            response_schema=schema,
        )
        span.set_attribute("gen_ai.usage.input_tokens", response.usage.input_tokens)
        span.set_attribute("gen_ai.usage.output_tokens", response.usage.output_tokens)
    return json.loads(response.message.content)


async def draft(client, topic: str, facts: list[str], feedback: str | None) -> str:
    numbered_facts = "\n".join(f"[{i + 1}] {fact}" for i, fact in enumerate(facts))
    prompt = (
        f"Write a short article about {topic!r} using these numbered facts:\n{numbered_facts}\n"
        "Cite each fact you use with its bracketed number, e.g. 'Revenue grew 12% [1].'"
    )
    if feedback is not None:
        prompt += f"\n\nRevise your previous draft based on this feedback: {feedback}"
    with chat_span(model=client.default_model, provider="mock") as span:
        response = await client.complete([Message(role=Role.USER, content=prompt)])
        span.set_attribute("gen_ai.usage.input_tokens", response.usage.input_tokens)
        span.set_attribute("gen_ai.usage.output_tokens", response.usage.output_tokens)
    return response.message.content or ""


async def critique(client, topic: str, article: str) -> tuple[bool, str]:
    schema = {
        "type": "object",
        "properties": {"approved": {"type": "boolean"}, "feedback": {"type": "string"}},
        "required": ["approved", "feedback"],
    }
    with chat_span(model=client.default_model, provider="mock") as span:
        response = await client.complete(
            [
                Message(
                    role=Role.USER,
                    content=f"Topic: {topic}\nArticle draft: {article}\n"
                    "Review this draft for accuracy and clarity.",
                )
            ],
            response_schema=schema,
        )
        span.set_attribute("gen_ai.usage.input_tokens", response.usage.input_tokens)
        span.set_attribute("gen_ai.usage.output_tokens", response.usage.output_tokens)
    result = json.loads(response.message.content)
    return result["approved"], result["feedback"]


def extract_citations(article: str) -> list[int]:
    """Return every bracketed integer citation found in `article`
    (e.g. "...grew 12% [1]. Costs fell [2]." -> [1, 2]), in order of
    appearance.

    TODO: implement this.
    """
    raise NotImplementedError


def verify_citations(article: str, facts: list[str]) -> dict:
    """Extract citations from `article` (via extract_citations) and check
    each one is a valid 1-indexed reference into `facts`. Return
    {"total_citations": <int>, "valid_citations": <int>, "citation_accuracy": <float>}.
    If there are no citations at all, return
    {"total_citations": 0, "valid_citations": 0, "citation_accuracy": 0.0}.

    TODO: implement this.
    """
    raise NotImplementedError


async def run_traced_pipeline(client, topic: str, max_revisions: int = 2) -> dict:
    """Same control flow as projects/04-multi-agent-content-pipeline/'s
    run_pipeline, with two additions:
      1. Wrap the whole run in invoke_agent_span("research-pipeline", ...),
         and wrap each worker call (research, each draft, each critique) in
         its own invoke_agent_span("researcher"/"writer"/"critic") -- so
         the exported spans show a real nested multi-agent trace (Module
         17), not a flat list.
      2. On a "success" or final "escalated" result, add the citation
         check (verify_citations(article, facts)) into the returned dict.

    Return shape (matching projects/04's run_pipeline, plus citation fields
    -- "..." below stands for total_citations/valid_citations/citation_accuracy):
      {"status": "escalated", "reason": ...}  -- if research failed
      {"status": "success", "article": ..., "revisions": <int>, ...citation fields...}
      {"status": "escalated", "reason": ..., "article": ..., ...citation fields...}
      (the last case is if never approved within max_revisions)

    TODO: implement this.
    """
    raise NotImplementedError
