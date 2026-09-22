# Lab 15.01 -- Vision QA agent

**Difficulty:** ★★★☆☆ · **Time:** ~1-2 hours

## Task

Build a small agent that loads a bundled image, attaches it to a message
using `shared/llm`'s `ImageContent`/`Message.images` (lesson 01), and asks
the model a question about it. No API key needed for the default tests --
tested against `shared.llm.get_client("mock")`. One `@pytest.mark.live`
test asks a real question against the real Anthropic API.

`images/red_square_on_blue.png` is a tiny (64x64, 148-byte), synthetically
generated PNG -- a red square centered on a blue background, built with pure
Python (`zlib`/`struct`, no external image library or downloaded asset) to
avoid any licensing ambiguity. It's simple enough that the live test can
assert on an unambiguous, objectively-correct answer ("blue").

## Files

- `starter/vision_agent.py` -- skeleton with the pieces to implement
- `solution/vision_agent.py` -- complete reference implementation
- `images/red_square_on_blue.png` -- the bundled test image
- `tests/` -- offline tests (encoding + mock provider) + one live-gated test

## Requirements

Implement these in `starter/vision_agent.py`:

- `def load_image(path: Path) -> ImageContent` -- read `path`'s bytes,
  base64-encode them, and return an `ImageContent` with the right
  `media_type` (look up `path.suffix.lower()` in `_MEDIA_TYPES`, already
  given). Raise `ValueError` for an unsupported extension.
- `async def ask_about_image(client, image: ImageContent, question: str) -> str`
  -- send `question` as a user message with `image` attached (`Message(...,
  content=question, images=[image])`) and return the model's text response.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/vision_agent.py`.
- `load_image` produces base64 that decodes back to valid PNG bytes (starts
  with the PNG file signature).
- `load_image` raises `ValueError` for a non-image file extension.
- `ask_about_image` sends a message whose `images` list contains exactly the
  `ImageContent` you passed in, and returns the model's response text.
- The live test (`-m live`) passes against the real Anthropic API when you
  have a real `ANTHROPIC_API_KEY` set.

## Running the tests

```bash
uv run pytest curriculum/15-voice-and-multimodal-agents/labs/01-vision-qa-agent/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/15-voice-and-multimodal-agents/labs/01-vision-qa-agent/tests
```

Live, against the real Anthropic API:

```bash
ANTHROPIC_API_KEY=sk-... uv run pytest -m live curriculum/15-voice-and-multimodal-agents/labs/01-vision-qa-agent/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[`projects/`](../../../../projects/README.md) for "data-analysis agent with
a code sandbox," then
[Module 16 -- Evaluation](../../../16-evaluation/README.md)
