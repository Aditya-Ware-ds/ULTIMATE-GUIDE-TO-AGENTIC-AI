"""Per-million-token USD pricing for the default "cheap" model of each provider.

Prices change monthly. Each entry carries the date it was checked and the page it
came from -- re-verify against that source before trusting these numbers for
anything beyond a rough lab cost estimate. Do not add a provider/model here without
a verified source and date.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelPrice:
    model: str
    input_per_million: float
    output_per_million: float
    last_verified: str
    source: str


PRICING: dict[str, ModelPrice] = {
    "anthropic": ModelPrice(
        model="claude-haiku-4-5",
        input_per_million=1.00,
        output_per_million=5.00,
        last_verified="2026-09-22",
        source="https://www.anthropic.com/claude/haiku",
    ),
    "openai": ModelPrice(
        model="gpt-5-nano",
        input_per_million=0.05,
        output_per_million=0.40,
        last_verified="2026-09-22",
        source="https://developers.openai.com/api/docs/pricing",
    ),
    "gemini": ModelPrice(
        model="gemini-3-flash",
        input_per_million=0.50,
        output_per_million=3.00,
        last_verified="2026-09-22",
        source="https://ai.google.dev/gemini-api/docs/pricing",
    ),
    "ollama": ModelPrice(
        model="qwen3:8b",
        input_per_million=0.0,
        output_per_million=0.0,
        last_verified="2026-09-22",
        source="https://ollama.com/library/qwen3 (runs locally, no per-token API cost)",
    ),
}


def estimate_cost(provider: str, input_tokens: int, output_tokens: int) -> float:
    """Rough USD cost estimate for a single call. See module docstring on freshness."""
    price = PRICING[provider]
    return (input_tokens / 1_000_000) * price.input_per_million + (
        output_tokens / 1_000_000
    ) * price.output_per_million
