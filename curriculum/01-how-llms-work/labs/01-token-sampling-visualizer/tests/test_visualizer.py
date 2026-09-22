import random

import pytest


def test_count_tokens_positive_for_nonempty_text(visualizer):
    assert visualizer.count_tokens("Building agents is fun!") > 0


def test_count_tokens_empty_string_is_zero(visualizer):
    assert visualizer.count_tokens("") == 0


def test_token_pieces_join_back_to_original_text(visualizer):
    text = "Building agents is fun!"

    pieces = visualizer.token_pieces(text)

    assert "".join(pieces) == text
    assert len(pieces) == visualizer.count_tokens(text)


def test_softmax_sums_to_one(visualizer):
    probs = visualizer.softmax([4.0, 1.0, 0.5, -2.0], temperature=1.0)

    assert sum(probs) == pytest.approx(1.0, abs=1e-6)
    assert all(p >= 0 for p in probs)


def test_softmax_rejects_nonpositive_temperature(visualizer):
    with pytest.raises(ValueError):
        visualizer.softmax([1.0, 2.0], temperature=0)

    with pytest.raises(ValueError):
        visualizer.softmax([1.0, 2.0], temperature=-1.0)


def test_lower_temperature_concentrates_distribution(visualizer):
    logits = [4.0, 1.0, 0.5, -2.0]

    low_temp_probs = visualizer.softmax(logits, temperature=0.1)
    high_temp_probs = visualizer.softmax(logits, temperature=2.0)

    assert max(low_temp_probs) > max(high_temp_probs)


def test_most_likely_index_matches_argmax(visualizer):
    assert visualizer.most_likely_index([0.1, 0.7, 0.2]) == 1
    assert visualizer.most_likely_index([0.9, 0.05, 0.05]) == 0


def test_sample_index_is_deterministic_for_seeded_rng(visualizer):
    probs = [0.1, 0.6, 0.3]

    first_draws = [visualizer.sample_index(probs, random.Random(42)) for _ in range(20)]
    second_draws = [visualizer.sample_index(probs, random.Random(42)) for _ in range(20)]

    assert first_draws == second_draws


def test_sample_index_respects_weights_over_many_draws(visualizer):
    probs = [0.05, 0.05, 0.9]
    rng = random.Random(7)

    draws = [visualizer.sample_index(probs, rng) for _ in range(2000)]

    assert draws.count(2) > draws.count(0) + draws.count(1)


def test_sample_index_always_in_range(visualizer):
    probs = [0.25, 0.25, 0.25, 0.25]
    rng = random.Random(1)

    for _ in range(100):
        index = visualizer.sample_index(probs, rng)
        assert 0 <= index < len(probs)
