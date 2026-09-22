# Module 01 quiz

**1. Why do LLMs use sub-word tokens instead of characters or whole words?**

<details><summary>Answer</summary>

Characters make sequences too long and force the model to learn spelling from
scratch; whole words need an unbounded vocabulary and can't handle unseen/rare
words. Sub-word BPE tokens compress common words into single tokens while
splitting rare/long words into reusable pieces, handling any input with a
bounded vocabulary.

</details>

**2. Why can't you use `tiktoken` to get an exact Claude token count?**

<details><summary>Answer</summary>

`tiktoken` implements OpenAI's tokenizer/vocabulary, not Anthropic's -- they're
different BPE models trained differently. It undercounts Claude usage by roughly
15-20% on typical text. Use Anthropic's own `count_tokens` endpoint for an exact
number.

</details>

**3. A model has a 128K-token context window. You send a 50K-token system prompt + history, and ask for a 4K-token response. Is that a problem?**

<details><summary>Answer</summary>

No -- 50K + 4K = 54K, well under 128K. Input and output share the same budget for
most current providers, so the relevant check is (input + expected output) vs.
the total window, not input alone.

</details>

**4. Why does a long-running chat conversation cost more per turn as it goes on, even if each new message is short?**

<details><summary>Answer</summary>

Every call is stateless -- you resend the entire prior conversation as input each
time. Turn 50 pays (as input tokens) for all 49 prior turns' worth of history,
every single call.

</details>

**5. What does temperature actually do to a model's output distribution?**

<details><summary>Answer</summary>

It scales the logits before softmax. Temperature < 1 sharpens the distribution
(more deterministic, concentrated on the highest-probability tokens); temperature
> 1 flattens it (more variety, more risk of incoherence or a wrong tool choice).

</details>

**6. Why would you set temperature near 0 for a tool-calling step in an agent, but not for a creative-writing task?**

<details><summary>Answer</summary>

Tool selection usually has one correct answer -- you want the model to reliably
pick its highest-confidence choice, not add randomness. Creative writing
benefits from variety, which higher temperature provides.

</details>

**7. What's the difference between top-k and top-p?**

<details><summary>Answer</summary>

Top-k keeps a fixed number of the highest-probability tokens before sampling.
Top-p keeps the smallest set of top tokens whose cumulative probability reaches a
threshold `p` -- it adapts to how peaked or flat the distribution is at each
step, rather than using a fixed count.

</details>

**8. What does cosine similarity measure, and why is it preferred over raw dot product for comparing embeddings?**

<details><summary>Answer</summary>

It measures the angle between two vectors (1.0 = same direction, 0.0 =
unrelated, -1.0 = opposite), ignoring magnitude. Raw dot product is sensitive to
vector length, which can correlate with things like text length rather than
meaning -- cosine similarity normalizes that away.

</details>

**9. True or false: if two texts have high embedding cosine similarity, the second is necessarily a good answer to the first as a query.**

<details><summary>Answer</summary>

False. High similarity means similar *meaning/topic*, not that one answers the
other. "What is the capital of France?" and "What is the capital of Germany?"
are embedding-similar but neither answers the other -- this is why real
retrieval systems combine embedding search with other signals (Module 06).

</details>

**10. Why is hallucination described as "structural" rather than a fixable bug?**

<details><summary>Answer</summary>

Every token -- correct or hallucinated -- comes from the same next-token
sampling process. The model has no separate mechanism that flags "this claim is
unsupported" before generating it; it samples plausible-looking continuations
regardless of truth. Grounding, structured outputs, and verification reduce the
impact but don't eliminate the underlying mechanism.

</details>

**11. When would you deliberately choose a reasoning model with hidden thinking (e.g. OpenAI's o-series) over one with visible extended thinking (e.g. Claude)?**

<details><summary>Answer</summary>

There's no universal answer, but a common reason: if you don't need to inspect
*why* the model reached its answer (only the final result matters) and want the
provider's own internal reasoning implementation, hidden reasoning is fine.
Visible thinking is more valuable when you need to debug or audit an agent's
decision process (Module 17) -- you can actually read the reasoning trace.

</details>

**12. Why shouldn't you route every single step of an agent through a reasoning model?**

<details><summary>Answer</summary>

Reasoning models spend extra tokens (cost) and time (latency) on thinking before
answering. That overhead pays off on genuinely hard, multi-step problems but
adds cost and delay with no accuracy benefit on simple steps like a lookup or a
one-line classification (see Module 19's model-routing pattern).

</details>
