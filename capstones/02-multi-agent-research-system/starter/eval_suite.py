"""Capstone 2: eval suite scoring the research pipeline's citation
accuracy across a set of topics. See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest capstones/02-multi-agent-research-system/tests
"""

from __future__ import annotations

DEFAULT_TOPICS = [
    "renewable energy adoption",
    "the history of the printing press",
    "octopus cognition",
]


async def evaluate_citation_accuracy(pipeline_fn, client_factory, topics=None) -> dict:
    """For each topic in `topics` (default DEFAULT_TOPICS): get a fresh
    client from client_factory(), call pipeline_fn(client, topic), and
    record {"topic": ..., "status": ..., "citation_accuracy": <outcome's
    citation_accuracy, or 0.0 if missing>}.

    Return {"total": <int>, "succeeded": <count of status=="success">,
    "mean_citation_accuracy": <mean citation_accuracy over only the
    succeeded results, or 0.0 if none succeeded>, "results": [...]}.

    TODO: implement this.
    """
    raise NotImplementedError
