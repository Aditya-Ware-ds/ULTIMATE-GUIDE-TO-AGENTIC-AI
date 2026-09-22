# Lab 01.01 -- Token & sampling visualizer

**Difficulty:** ★★★☆☆ · **Time:** ~1.5-2 hours

## Task

Build a small library with two independent pieces, both covered in this module's
lessons:

1. **Token counting/breakdown** using a real tokenizer (`tiktoken`).
2. **Temperature-based sampling** over a toy logit distribution, including a
   deterministic weighted-random draw.

No API key or network call to an LLM provider is needed -- `tiktoken` needs
network access once to download and cache its encoding file (same as any first
`pip`/`uv` install), and everything else is pure math.

## Files

- `starter/visualizer.py` -- skeleton with five functions to implement
- `solution/visualizer.py` -- complete reference implementation
- `tests/` -- tests that exercise both (see "Running the tests" below)

## Requirements

Implement these functions in `starter/visualizer.py`:

- `def count_tokens(text: str, encoding_name: str = "o200k_base") -> int` -- return
  the number of tokens `text` encodes to.
- `def token_pieces(text: str, encoding_name: str = "o200k_base") -> list[str]` --
  return the decoded string for each individual token, in order (e.g.
  `"Hi there!"` -> `["Hi", " there", "!"]`, matching whatever your tokenizer
  actually produces).
- `def softmax(logits: list[float], temperature: float) -> list[float]` -- apply
  temperature scaling then softmax (see `lessons/03-sampling-and-decoding.md` for
  the formula). Raise `ValueError` if `temperature <= 0`.
- `def sample_index(probabilities: list[float], rng: random.Random) -> int` --
  given a probability distribution (sums to ~1.0) and a seeded `random.Random`,
  return a weighted-random index. Use `rng.random()` plus a cumulative-sum walk
  (do not use `rng.choices()` -- the point is to understand the mechanism).
- `def most_likely_index(probabilities: list[float]) -> int` -- return the index
  of the highest probability (this is what "temperature ~0" / greedy decoding
  approximates).

## Acceptance criteria

- All tests in `tests/` pass against your `starter/visualizer.py`.
- `softmax` output always sums to ~1.0 (within floating-point tolerance) and
  raises `ValueError` for `temperature <= 0`.
- Lower temperature makes `softmax`'s output distribution more concentrated on
  the highest logit; higher temperature makes it flatter (your tests will check
  this directly by comparing the max probability at two temperatures).
- `sample_index` is deterministic for a given seeded `rng` (same seed -> same
  sequence of draws) but respects the given probability weights over many draws.

## Hints

- For `token_pieces`, encode the whole string once, then decode each token ID
  individually -- don't try to split the original string yourself.
- For `softmax`, subtract the max scaled logit before exponentiating (numerical
  stability) -- see the lesson's code for the exact pattern.
- For `sample_index`, walk the cumulative sum of `probabilities` and return the
  first index where the cumulative sum exceeds `rng.random()`.

## Running the tests

```bash
uv run pytest curriculum/01-how-llms-work/labs/01-token-sampling-visualizer/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/01-how-llms-work/labs/01-token-sampling-visualizer/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 02 -- Talking to LLMs](../../../02-talking-to-llms/README.md)
