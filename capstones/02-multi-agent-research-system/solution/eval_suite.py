"""Capstone 2: eval suite scoring the research pipeline's citation
accuracy across a set of topics. Reference solution. See ../README.md.

Generic over the pipeline implementation (Module 16's evaluate_dataset
shape: the pipeline function and client factory are injected, not
imported).
"""

from __future__ import annotations

DEFAULT_TOPICS = [
    "renewable energy adoption",
    "the history of the printing press",
    "octopus cognition",
]


async def evaluate_citation_accuracy(pipeline_fn, client_factory, topics=None) -> dict:
    topics = DEFAULT_TOPICS if topics is None else topics
    results = []
    for topic in topics:
        client = client_factory()
        outcome = await pipeline_fn(client, topic)
        results.append(
            {
                "topic": topic,
                "status": outcome["status"],
                "citation_accuracy": outcome.get("citation_accuracy", 0.0),
            }
        )

    scored = [r for r in results if r["status"] == "success"]
    mean_accuracy = sum(r["citation_accuracy"] for r in scored) / len(scored) if scored else 0.0
    return {
        "total": len(topics),
        "succeeded": len(scored),
        "mean_citation_accuracy": mean_accuracy,
        "results": results,
    }
