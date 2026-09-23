"""Capstone 2: multi-agent research system -- reference solution.
See ../README.md and ../ARCHITECTURE.md.

Extends projects/04-multi-agent-content-pipeline/'s researcher/writer/critic
topology (unchanged core logic) with numbered-fact citations, citation
verification, and full tracing (Module 17) of each worker as its own
nested span.
"""

from __future__ import annotations

import json
import re

from shared.llm import Message, Role
from shared.tracing import chat_span, invoke_agent_span


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


_CITATION_RE = re.compile(r"\[(\d+)\]")


def extract_citations(article: str) -> list[int]:
    return [int(match) for match in _CITATION_RE.findall(article)]


def verify_citations(article: str, facts: list[str]) -> dict:
    citations = extract_citations(article)
    if not citations:
        return {"total_citations": 0, "valid_citations": 0, "citation_accuracy": 0.0}
    valid = sum(1 for c in citations if 1 <= c <= len(facts))
    return {
        "total_citations": len(citations),
        "valid_citations": valid,
        "citation_accuracy": valid / len(citations),
    }


async def run_traced_pipeline(client, topic: str, max_revisions: int = 2) -> dict:
    with invoke_agent_span("research-pipeline", **{"gen_ai.request.topic": topic}):
        with invoke_agent_span("researcher"):
            research_result = await research(client, topic)
        if research_result["status"] != "success":
            return {
                "status": "escalated",
                "reason": research_result.get("reason", "research failed"),
            }

        facts = research_result["facts"]
        feedback: str | None = None
        with invoke_agent_span("writer", **{"gen_ai.request.revision": 0}):
            article = await draft(client, topic, facts, feedback)

        for revision in range(max_revisions + 1):
            with invoke_agent_span("critic", **{"gen_ai.request.revision": revision}):
                approved, feedback = await critique(client, topic, article)
            if approved:
                citation_check = verify_citations(article, facts)
                return {
                    "status": "success",
                    "article": article,
                    "revisions": revision,
                    **citation_check,
                }
            if revision == max_revisions:
                break
            with invoke_agent_span("writer", **{"gen_ai.request.revision": revision + 1}):
                article = await draft(client, topic, facts, feedback)

    citation_check = verify_citations(article, facts)
    return {
        "status": "escalated",
        "reason": f"not approved after {max_revisions} revision(s): {feedback}",
        "article": article,
        **citation_check,
    }
