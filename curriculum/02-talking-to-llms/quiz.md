# Module 02 quiz

**1. Why do you have to resend the assistant's previous reply on the next call, instead of the API remembering it?**

<details><summary>Answer</summary>

LLM APIs are stateless -- each call only knows what's in the `messages` list you
send. There's no server-side memory of a prior call unless you build it yourself
(Module 07) or use a provider-specific stateful feature.

</details>

**2. What's special about the `system` role compared to `user`?**

<details><summary>Answer</summary>

It's meant to carry stable, higher-authority instructions for the whole
conversation, sent once rather than as part of the back-and-forth. Providers
generally give it more resistance to being overridden by later user content --
which is directly relevant to prompt-injection risks in Module 18.

</details>

**3. Does streaming reduce the total time or cost of a completion?**

<details><summary>Answer</summary>

No. The model still generates the same number of tokens either way. Streaming
improves *perceived* latency (time to first visible output) and enables
progressive UIs, not total generation time or token cost.

</details>

**4. Why should you still validate a model's structured output against your schema even when the provider "guarantees" it matches?**

<details><summary>Answer</summary>

Provider guarantees can have edge cases, your schema might have a bug, and your
own tests against a mock provider (which enforces nothing) need real validation
to actually test anything. Defensive validation costs a few lines and catches
real failure modes.

</details>

**5. What's the difference between asking a model to "extract structured JSON" via structured outputs versus via forced tool use?**

<details><summary>Answer</summary>

Per Anthropic's own framing, they're the same underlying primitive from the
model's point of view -- a tool call's input schema and a structured-output
schema serve the same constraining purpose. Native structured outputs are
usually simpler for pure extraction with no actual tool execution involved.

</details>

**6. Give two concrete prompt-engineering techniques with consistent evidence of impact.**

<details><summary>Answer</summary>

Any two of: explicit output-format instructions, few-shot examples, clear
structure/ordering (system instructions, then context, then the question),
explicit "don't do X" instructions, and asking for step-by-step reasoning before
a final answer on hard problems.

</details>

**7. A model gives a wrong factual answer. Is rewriting the prompt always the right fix?**

<details><summary>Answer</summary>

No. If the model doesn't have the needed information, that's a retrieval problem
(Module 06), not a prompting problem -- no prompt rewording supplies missing
information. If the task requires a precise action (a calculation, a live
lookup), that's a tool-use problem (Module 03).

</details>

**8. Why does a longer model response typically cost more than a longer *input*, per token?**

<details><summary>Answer</summary>

Output tokens are usually priced several times higher than input tokens for the
same model -- check `shared/llm/pricing.py`'s `ModelPrice.output_per_million` vs.
`input_per_million` for concrete current numbers.

</details>

**9. Why does this repo's `MockLLMProvider` not enforce a `response_schema` you pass to `complete()`?**

<details><summary>Answer</summary>

It's a scriptable fake that returns whatever response you told it to return,
regardless of what parameters you passed -- it doesn't simulate provider-side
schema enforcement. That's exactly why lab code must validate output itself
rather than relying on the request parameter alone.

</details>

**10. Why does this repo default every lab's real-provider path to the cheapest current model (e.g. Claude Haiku 4.5, GPT-5 nano)?**

<details><summary>Answer</summary>

So working through the curriculum with real API calls costs cents rather than
dollars (Ground Rule: "default to cheap/small models"), while still exercising
the real API shape. Production systems apply the same idea more granularly via
model routing (Module 19): cheap models for most steps, expensive ones only
where they're actually needed.

</details>
