# Vision inputs

**Last verified:** 2026-09-22 (against [Anthropic's vision docs](https://platform.claude.com/docs/en/build-with-claude/vision))
**Difficulty:** ★★★☆☆ · **Time:** ~40 minutes

## Learning objectives

- Attach an image to a `Message` using `shared/llm/`'s `ImageContent`, and understand which provider adapter currently supports it.
- Explain why images should generally come before text in a multimodal prompt.
- Decide when a task actually needs an image, versus when a text description would do.

## Intuition

Every message this curriculum has built so far has been text: a string in,
a string (or a tool call) out. A model that can also accept images doesn't
change the agent loop's shape (Module 04's loop is unaffected) -- it changes
what a `Message`'s *content* can contain. This lesson extends `shared/llm/`
with the minimum needed to send an image, verified against Anthropic's
current API, and wires it into `AnthropicProvider` specifically (documented
below as a known, deliberate scope limit).

## The concept

### `ImageContent` and `Message.images`

```python
from shared.llm import ImageContent, Message, Role

message = Message(
    role=Role.USER,
    content="What does this chart show?",
    images=[ImageContent(media_type="image/png", data_base64=encoded_png_bytes)],
)
```

`ImageContent` is deliberately minimal: a MIME type and base64 data, mirroring
the actual shape every major vision API converges on for inline images.
`AnthropicProvider._to_wire` (verified 2026-09-22) converts this into
Anthropic's current base64 image content block:

```python
{
    "type": "image",
    "source": {"type": "base64", "media_type": "image/png", "data": "..."},
}
```

Anthropic's current docs explicitly recommend placing image blocks *before*
the accompanying text in a message's content array (the same "long content
first" ordering principle Module 05's context-engineering lesson already
covered for long documents) -- `AnthropicProvider` follows this ordering.

### A deliberate, documented scope limit

Only `AnthropicProvider` currently builds image content blocks.
`OpenAIProvider`, `GeminiProvider`, and `OllamaProvider` will silently ignore
a `Message.images` list rather than sending it -- extending each of them
would require verifying each vendor's current image-block shape
independently (the same fast-moving-API caution from Module 10/11's
pitfalls), which is out of scope for this module's lab. This is the same
kind of documented, honest limitation as the repo's existing note that
`GeminiProvider.stream()` is a non-native fallback -- a known gap, not a
silent one.

### Encoding an image for a request

```python
import base64
from pathlib import Path

data_base64 = base64.b64encode(Path("chart.png").read_bytes()).decode("ascii")
```

This is the one piece of this lesson worth actually testing offline: given a
real image file, does encoding it produce valid base64 that round-trips
correctly? The lab's tests verify this directly, without needing a live
model call to do so.

## Deeper: multimodal input doesn't change the agent loop

An agent that can "see" an image still runs Module 04's exact loop --
observe (now including image content), think, act. Nothing about tool
calling, stopping conditions, or step budgets changes. The only new surface
is what a single message can contain, which is why this module's lab reuses
the ReAct loop shape directly rather than introducing a new pattern.

## When not to use this

Don't attach an image when a text description would serve the task just as
well (Module 02's cost lesson applies directly -- images cost meaningfully
more tokens than the text describing them would, per Anthropic's current
per-image token-cost table). Reserve vision input for tasks that genuinely
need visual detail a description would lose (reading a chart's exact
values, checking a UI against a design) rather than reaching for it because
a model happens to support it.

## Common mistakes

- Putting the text before the image in a multimodal message, missing the
  "images first" ordering Anthropic's current guidance recommends for best
  results.
- Assuming every provider adapter in `shared/llm/` supports `Message.images`
  just because `AnthropicProvider` does -- check which adapter you're
  actually using before relying on vision support.
- Sending a needlessly large, high-resolution image when a downsized version
  would answer the same question -- this directly inflates token cost per
  Anthropic's current resolution/token-cost table.

## Key takeaways

- `shared/llm/`'s `ImageContent`/`Message.images` gives a minimal, verified way to attach images -- currently wired into `AnthropicProvider` only, a documented scope limit.
- Images should come before accompanying text in a multimodal message, per current vendor guidance.
- Multimodal input doesn't change the agent loop's shape -- it only changes what a message can contain.

## Lab

[`labs/01-vision-qa-agent/`](../labs/01-vision-qa-agent/README.md)
