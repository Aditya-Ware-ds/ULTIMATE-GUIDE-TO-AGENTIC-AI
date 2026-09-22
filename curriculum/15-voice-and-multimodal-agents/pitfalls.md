# Module 15 pitfalls

## Assuming every provider adapter supports `Message.images`

`Message.images` exists on the shared, provider-agnostic type, but only
`AnthropicProvider` currently reads it. Running a vision-input agent with
`LLM_PROVIDER=openai` (or gemini, or ollama) won't raise an error -- the
image is simply never sent, and the model answers as if it never received
one, which can look like a confusing model failure ("why didn't it see the
image?") rather than the actual cause (the adapter you're using doesn't
support it yet). Always check which provider you're actually running
against before debugging a vision task that seems to be ignoring the image.

## Testing "the agent works" only against the mock provider for a vision task

The mock provider (`shared/llm/mock.py`) never inspects a message's actual
content -- it just returns whatever was scripted, regardless of whether an
image was attached correctly or not. This makes it perfect for testing
control flow (Module 04's loop shape) but useless for verifying the *image
itself* was correctly loaded, encoded, and attached. This lab's tests
specifically separate these concerns: `test_load_image_produces_valid_
base64_png` verifies the encoding is actually correct (independent of any
model call), while the mock-provider test verifies only that the resulting
`Message` carries the image through to the request. Neither test alone
proves a real provider would receive a genuinely valid image -- the
live-gated test is what actually proves that end-to-end.

## Sending a needlessly large image "just in case"

It's tempting to attach a full-resolution image without considering size,
since it "can't hurt to give the model more detail." Per Anthropic's current
resolution/token-cost table (lesson 01), a large image can cost several
times more tokens than a modestly downsized version that answers the same
question just as well -- for tasks that don't need fine visual detail,
resize before encoding, not after noticing the bill.

## Treating the realtime-voice architecture lesson as "not real work"

Because lesson 02 has no runnable lab, it's tempting to skim it. The
architecture concepts there (direct audio processing to minimize latency,
voice activity detection for turn-taking, barge-in support) are real,
current, verified facts about how production voice agents are actually
built -- skipping them because there's no code to run in this module means
missing the one part of this curriculum that covers voice agents at all.
