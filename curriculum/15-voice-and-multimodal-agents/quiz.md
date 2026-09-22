# Module 15 quiz

**1. Does attaching an image to a message change the shape of Module 04's agent loop?**

<details><summary>Answer</summary>

No. The loop (observe, think, act, repeat until done or max steps) is
unchanged -- only what a single message can *contain* changes. Vision input
is a change to message content, not to agent control flow.

</details>

**2. What are the two fields on `ImageContent`, and why is it kept this minimal?**

<details><summary>Answer</summary>

`media_type` (a MIME type like `image/png`) and `data_base64` (the
base64-encoded image bytes). This mirrors the actual shape every major
vision API's inline-image format converges on, so it's the minimum needed
to build any provider's real request without extra fields nothing uses.

</details>

**3. Which provider adapter in `shared/llm/` currently sends `Message.images` to the real API, and what happens if you use a different one?**

<details><summary>Answer</summary>

Only `AnthropicProvider` currently builds image content blocks from
`Message.images`. The other adapters (OpenAI, Gemini, Ollama) silently
ignore the field -- a documented, deliberate scope limit, not a bug you'd
discover only by reading the source.

</details>

**4. Why should images generally come before accompanying text in a multimodal message's content?**

<details><summary>Answer</summary>

Anthropic's current documentation recommends this ordering for best
results -- the same "long content first" principle Module 05's
context-engineering lesson already covered for long documents, applied to
images.

</details>

**5. Why might attaching an image to a request cost meaningfully more than describing the same content in text?**

<details><summary>Answer</summary>

Images are converted into a number of "visual tokens" based on resolution
(per Anthropic's current per-image token-cost table), which can be larger
than the token cost of a concise text description of the same content --
Module 02's cost lesson applies directly: don't reach for an image input
by default when text would answer the same question just as well.

</details>

**6. Why do current realtime voice APIs process audio directly, rather than chaining separate speech-to-text and text-to-speech steps?**

<details><summary>Answer</summary>

Chaining separate steps, each with its own latency, would make the tight
turnaround real-time conversation needs much harder to hit. Processing
audio directly (verified against OpenAI's current Realtime API docs) is
specifically architected to minimize first-audio latency.

</details>

**7. What is "barge-in," and why does it require more than a fixed silence timeout to implement?**

<details><summary>Answer</summary>

Barge-in is the ability for a user to interrupt the agent mid-response, the
way a human conversation allows. A fixed silence timeout can't distinguish
"the user paused to think" from "the user finished speaking" or "the user
wants to interrupt" -- current systems use voice activity detection to make
this real-time judgment, not a simple timer.

</details>

**8. Why does this module's realtime-voice lesson have no required runnable lab?**

<details><summary>Answer</summary>

A working realtime-audio lab would need either a real, metered per-minute
API dependency (breaking the "tests run offline with no API keys" ground
rule) or substantial audio-streaming transport infrastructure whose
complexity is mostly about the transport layer, not agent concepts. The
architecture is covered conceptually instead.

</details>

**9. In this module's lab, why is the bundled test image generated with pure Python instead of downloaded or using an image library?**

<details><summary>Answer</summary>

To avoid any licensing ambiguity around a downloaded or found image, and to
avoid adding a new dependency (like Pillow) just to produce one small,
simple, static test asset -- a hand-written minimal PNG encoder produces a
real, valid PNG file with neither cost.

</details>

**10. A task needs to summarize a long text document. Should you convert it to an image (e.g. a screenshot) and use vision input instead of sending the text directly?**

<details><summary>Answer</summary>

No -- sending the text directly is cheaper and more reliable; a model reads
plain text more accurately and at lower token cost than it reads the same
content rendered as an image. Vision input earns its cost specifically for
content that is genuinely visual (a chart's layout, a UI screenshot), not
as a substitute for sending text that's already available as text.

</details>
