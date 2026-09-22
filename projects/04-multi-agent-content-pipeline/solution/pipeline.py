"""Project 04: multi-agent content pipeline -- reference solution.
See ../README.md.
"""

from __future__ import annotations

import json

from shared.llm import Message, Role


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
    return json.loads(response.message.content)


async def draft(client, topic: str, facts: list[str], feedback: str | None) -> str:
    prompt = f"Write a short article about {topic!r} using these facts:\n" + "\n".join(facts)
    if feedback is not None:
        prompt += f"\n\nRevise your previous draft based on this feedback: {feedback}"
    response = await client.complete([Message(role=Role.USER, content=prompt)])
    return response.message.content or ""


async def critique(client, topic: str, article: str) -> tuple[bool, str]:
    schema = {
        "type": "object",
        "properties": {"approved": {"type": "boolean"}, "feedback": {"type": "string"}},
        "required": ["approved", "feedback"],
    }
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
    result = json.loads(response.message.content)
    return result["approved"], result["feedback"]


async def run_pipeline(client, topic: str, max_revisions: int = 2) -> dict:
    research_result = await research(client, topic)
    if research_result["status"] != "success":
        return {"status": "escalated", "reason": research_result.get("reason", "research failed")}

    facts = research_result["facts"]
    feedback: str | None = None
    article = await draft(client, topic, facts, feedback)

    for revision in range(max_revisions + 1):
        approved, feedback = await critique(client, topic, article)
        if approved:
            return {"status": "success", "article": article, "revisions": revision}
        if revision == max_revisions:
            break
        article = await draft(client, topic, facts, feedback)

    return {
        "status": "escalated",
        "reason": f"not approved after {max_revisions} revision(s): {feedback}",
        "article": article,
    }
