import pytest

from shared.llm.pricing import PRICING, estimate_cost


def test_all_providers_have_pricing_entries():
    for provider in ("anthropic", "openai", "gemini", "ollama"):
        assert provider in PRICING
        price = PRICING[provider]
        assert price.last_verified
        assert price.source.startswith("http")


def test_estimate_cost_zero_tokens_is_zero():
    assert estimate_cost("anthropic", 0, 0) == 0.0


def test_estimate_cost_matches_manual_calculation():
    cost = estimate_cost("openai", input_tokens=1_000_000, output_tokens=1_000_000)
    price = PRICING["openai"]
    assert cost == pytest.approx(price.input_per_million + price.output_per_million)


def test_ollama_is_free():
    assert estimate_cost("ollama", 1_000_000, 1_000_000) == 0.0


def test_unknown_provider_raises_key_error():
    with pytest.raises(KeyError):
        estimate_cost("not-a-provider", 1, 1)
