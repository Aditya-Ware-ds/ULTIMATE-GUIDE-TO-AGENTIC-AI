# Tokens and tokenizers

**Last verified:** 2026-09-22
**Difficulty:** ★★☆☆☆ · **Time:** ~45 minutes

## Learning objectives

- Explain what a token is and why LLMs use tokens instead of characters or whole words.
- Count tokens in real text using `tiktoken`.
- Explain why "how many tokens is this?" depends on *which model's* tokenizer you ask.

## Intuition

An LLM doesn't read text character-by-character or word-by-word. It reads
**tokens** -- chunks of text (often sub-word pieces) produced by a specific
algorithm called Byte Pair Encoding (BPE). "Tokenization" is the same idea as
splitting a sentence into words for a spell-checker, except the "words" a
tokenizer produces are optimized for compression and frequency in training data,
not for matching human intuition about word boundaries. `" agentic"` might be one
token; `"unbelievably"` might be three (`"un"`, `"believ"`, `"ably"`).

## The concept

### Why tokens, not characters or words

- **Characters** would make sequences enormously long (a 500-word essay is ~2500+
  characters), and the model would have to learn spelling and word formation from
  scratch at the character level -- wasteful.
- **Whole words** would need a vocabulary covering every word in every language,
  including ones never seen in training (impossible to handle new/rare words or typos).
- **Sub-word tokens** (BPE) split rare/long words into common pieces while keeping
  frequent words as single tokens -- `"the"` is one token, `"tokenization"` might
  be two or three. This handles any input text, including made-up words, without
  an unbounded vocabulary.

### Counting tokens with `tiktoken`

```python
import tiktoken

encoding = tiktoken.get_encoding("o200k_base")  # used by GPT-4o, o1, o3, GPT-5-class models
tokens = encoding.encode("Building agents is fun!")
print(len(tokens))  # a number, not len(text.split())
print(tokens)  # a list of integer token IDs
print(encoding.decode(tokens))  # back to the original text
```

`tiktoken.get_encoding("o200k_base")` loads OpenAI's current 200k-vocabulary BPE
tokenizer (used by GPT-4o and later models). Different model *families* use
different tokenizers with different vocabularies -- the same English sentence can
produce a different token count depending on which model you're asking about.

### Every provider's tokenizer is different

This is the detail that trips people up: **`tiktoken` is OpenAI's tokenizer.** It
does not match Anthropic's or Google's tokenizers. As of 2026, OpenAI's tiktoken
undercounts Claude's actual token usage by roughly 15-20% on typical English text,
and by more on code or non-English text -- because Claude's tokenizer is a
different BPE vocabulary trained differently. If you need an *exact* Claude token
count (e.g. to precisely predict cost or check you're under a context limit),
call Anthropic's own count-tokens endpoint:

```python
from anthropic import Anthropic

client = Anthropic()
response = client.messages.count_tokens(
    model="claude-haiku-4-5",
    messages=[{"role": "user", "content": "Building agents is fun!"}],
)
print(response.input_tokens)
```

Rule of thumb: use `tiktoken` for OpenAI-family models and for *rough* estimates
across providers; use each provider's own counting endpoint when you need an
exact number for a non-OpenAI model.

## Deeper: why this matters for cost and context budgeting

Every price you'll see quoted in this repo (`shared/llm/pricing.py`) is per
million *tokens*, and every context window (Module 02) is measured in tokens, not
characters or words. A rough mental estimate for English text: **~4 characters per
token, or ~0.75 tokens per word** -- good enough for back-of-envelope cost
estimates, not good enough for anything you're billing a user for.

## When not to use this

Don't hand-roll your own tokenizer or word-splitting logic to estimate cost or
context usage for a real provider call -- use that provider's actual tokenizer or
counting endpoint. A hand-rolled `len(text.split())` estimate can be off by 2x or
more, especially for code, which tokenizes very differently from prose.

## Common mistakes

- Assuming token count ≈ word count. It's close for plain English prose and wildly
  off for code, non-English text, and text with lots of punctuation or whitespace.
- Using `tiktoken` to estimate Claude or Gemini token counts for anything that
  matters (billing, hard context limits) -- use the provider's own counting
  endpoint instead, as shown above.
- Forgetting that the tokenizer for a *fine-tuned or newer* model in the same
  family can change -- `tiktoken`'s model-to-encoding map lags new model releases
  by weeks; wrap `tiktoken.encoding_for_model(name)` in a try/except with a
  fallback to a known encoding (e.g. `"o200k_base"`) rather than assuming it always
  resolves.

## Key takeaways

- Tokens are sub-word BPE chunks, not characters or words -- this is what makes handling any input text tractable with a bounded vocabulary.
- Every model family has its own tokenizer; token counts aren't portable across providers.
- Use `tiktoken` for OpenAI-family estimates; use each provider's own counting endpoint for exact numbers elsewhere.

## Lab

[`labs/01-token-sampling-visualizer/`](../labs/01-token-sampling-visualizer/README.md)
