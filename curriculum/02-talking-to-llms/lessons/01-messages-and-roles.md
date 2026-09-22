# Messages and roles

**Last verified:** 2026-09-22
**Difficulty:** ★★☆☆☆ · **Time:** ~30-45 minutes

## Learning objectives

- Read and construct a messages array with the correct roles.
- Explain what a system prompt is for and how it differs from a user message.
- Explain why this repo defines its own `Message`/`Role` types instead of using each provider's wire format directly.

## Intuition

Every current LLM API takes conversation as a list of turns, each tagged with a
**role** saying who "said" it. This is the same shape as a chat transcript: it's
not a coincidence -- these APIs are modeled directly on multi-turn conversation,
even for single-shot, non-chat use cases.

## The concept

### The roles you'll actually use

- **`system`** -- instructions that shape the model's behavior for the whole
  conversation (persona, constraints, output format expectations). Sent once, not
  as part of the back-and-forth.
- **`user`** -- what the human (or your application, on the human's behalf) said.
- **`assistant`** -- what the model said in a prior turn. You send this back on
  every subsequent call because APIs are stateless (Module 01, lesson 02) --
  the model has no memory of its own prior replies unless you include them.
- **`tool`** (Module 03) -- the result of a tool call, fed back to the model so it
  can continue reasoning with that information.

### A minimal example, this repo's shape

```python
from shared.llm import Message, Role, get_client

client = get_client("mock")
client.provider.add_text("Paris is the capital of France.")

messages = [
    Message(role=Role.SYSTEM, content="You are a concise geography assistant."),
    Message(role=Role.USER, content="What's the capital of France?"),
]
response = await client.complete(messages)
print(response.message.content)
```

Every provider's *wire format* differs slightly (Anthropic takes `system` as a
separate top-level parameter, not a message in the list; OpenAI's Responses API
uses an `input` list; see `shared/llm/providers/`), but this repo's `Message`/
`Role` types (`shared/llm/types.py`) give you one shape to write lab code against,
regardless of provider. This is exactly what Ground Rule "stay provider-agnostic"
means in practice -- you're looking at the actual adapter code that makes it true.

### Multi-turn conversation is just a growing list

```python
messages = [Message(role=Role.SYSTEM, content="Be concise.")]
messages.append(Message(role=Role.USER, content="What's 2+2?"))
# ... call the model, get a response ...
messages.append(Message(role=Role.ASSISTANT, content="4"))
messages.append(Message(role=Role.USER, content="And that times 10?"))
# call the model again with the FULL messages list, not just the new question
```

The model only sees what's in `messages` on this specific call. If you forget to
append the assistant's prior reply before the next user turn, the model loses all
context of what it just said.

## Deeper: why the system prompt is special

Providers generally give the system prompt more "authority" during training and
serving -- it's meant to set boundaries the model should be more resistant to a
user overriding via later messages. This distinction becomes directly relevant in
Module 18 (security): a prompt-injection attack is fundamentally about tricking a
model into treating attacker-controlled content (which arrives as `user` content,
or worse, as tool output) as if it had system-level authority.

## When not to use this

Don't put content that should be immutable instruction (rules the model must
never violate regardless of what a user says) inside a `user` message and expect
system-prompt-level enforcement -- it doesn't have that authority. Conversely,
don't put per-request, changing user data inside the system prompt if you're
using prompt caching (Module 19) -- caching works best when the system prompt is
stable across calls.

## Common mistakes

- Forgetting to append the assistant's previous reply to `messages` before
  sending the next turn -- the model will respond as if the prior exchange never
  happened.
- Putting untrusted, externally-sourced content (e.g. scraped web text, a tool's
  output) directly into a system-prompt-equivalent position, trusting it the way
  you'd trust your own instructions. Treat tool/retrieved content as `user`- or
  `tool`-role data, not instructions -- Module 18 covers why this matters.
- Assuming role names are identical across every provider's actual wire format.
  They're conceptually the same but the exact JSON shape differs -- that's
  precisely why `shared/llm/types.py` exists.

## Key takeaways

- Every API takes a list of role-tagged turns: `system` (instructions), `user`, `assistant`, and (Module 03) `tool`.
- APIs are stateless -- you resend the whole conversation, including prior assistant replies, every call.
- This repo's `Message`/`Role` types are a provider-agnostic shape; each `shared/llm/providers/*.py` adapter translates to/from the real wire format.

## Lab

[`labs/01-chat-and-extract/`](../labs/01-chat-and-extract/README.md)
