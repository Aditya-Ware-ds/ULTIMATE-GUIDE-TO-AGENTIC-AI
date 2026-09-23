# DSPy signatures and modules

**Last verified:** 2026-09-22 (against `dspy` 3.3.1, installed and inspected directly -- see pitfalls.md for why)
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Express a task's inputs and outputs as a DSPy `Signature` instead of a hand-written prompt string.
- Run a signature with `dspy.Predict` and explain what DSPy is doing on your behalf.
- Configure DSPy against a custom, scriptable LM for offline testing (no API key, no network).

## Intuition

Every module before this one built prompts by hand: a Python string with
placeholders, sent as a `Message` (Module 02). DSPy inverts that -- you
declare *what* a task needs (its input and output fields) as a
**Signature**, and DSPy generates and manages the actual prompt text for
you, in a form its optimizers (lesson 02) can then systematically improve.
The prompt becomes an implementation detail DSPy manages, not something you
hand-tune and then never revisit.

## The concept

### A signature and a call

```python
import dspy

predictor = dspy.Predict("question -> answer")
result = predictor(question="What is the capital of France?")
print(result.answer)  # "Paris"
```

`"question -> answer"` is a shorthand signature: one input field, one
output field. DSPy builds a real prompt from this (a system-style
instruction plus the input, requesting the output in a structured format)
and parses the model's response back into `result.answer` -- you never
write or parse that prompt text yourself.

### Configuring a custom LM for offline testing

DSPy's `dspy.BaseLM` is subclassable for exactly this purpose (verified
directly in the installed package's docstring, 2026-09-22):

```python
import types
import dspy


class ScriptedLM(dspy.BaseLM):
    forward_contract = "legacy"

    def forward(self, prompt=None, messages=None, **kwargs):
        message = types.SimpleNamespace(content='{"answer": "Paris"}')
        choice = types.SimpleNamespace(message=message, finish_reason="stop")
        return types.SimpleNamespace(
            choices=[choice], usage={"prompt_tokens": 5, "completion_tokens": 5}, model=self.model
        )


dspy.configure(lm=ScriptedLM(model="scripted-test"), adapter=dspy.JSONAdapter())
```

This is the same "swap the real provider for a scriptable fake" principle
`shared/llm/mock.py` gives every other module -- now applied to DSPy's own
LM abstraction, so this module's lab needs no API key at all.
`dspy.JSONAdapter()` is configured explicitly here because DSPy's default
`ChatAdapter` expects a different response text format and falls back to
`JSONAdapter` on a parse failure -- configuring `JSONAdapter` directly
avoids that extra, wasted call when scripting plain JSON responses.

## Deeper: this is genuinely current, not a stale API

Search results and older tutorials for fast-moving frameworks routinely
describe outdated APIs (Module 10's and Module 11's pitfalls both name this
explicitly). This lesson's `BaseLM` example was verified by installing
`dspy` for real (`uv run --with dspy python -c "..."`) and reading its
actual installed source with `inspect.getsource()`, then running it, before
writing a single line of this lesson -- the same discipline applied to
every fast-moving dependency in this curriculum since Module 10.

## When not to use this

Don't reach for DSPy's declarative signatures for a task with one, simple,
already-working hand-written prompt you have no plans to systematically
optimize -- the value DSPy adds is specifically in lesson 02's optimization
step; without that, it's more machinery than a hand-written prompt needs.

## Common mistakes

- Assuming DSPy's default adapter will parse any reasonable-looking model
  output -- `ChatAdapter` expects a specific format and silently falls back
  to a second call with `JSONAdapter` on parse failure, doubling the call
  count if you don't configure the adapter explicitly for a scripted test.
- Returning a plain `dict` from a custom `BaseLM.forward()` instead of an
  object with `.choices[0].message.content`-style attribute access -- DSPy's
  legacy contract expects an OpenAI-response-shaped object, not a dict.
- Trusting an LLM-generated DSPy code sample without installing the actual
  package and checking -- exactly the mistake this lesson's own research
  process avoided.

## Key takeaways

- A DSPy `Signature` declares a task's inputs/outputs; DSPy manages the actual prompt text, keeping it available for optimization rather than hand-fixed.
- `dspy.BaseLM` is subclassable for a fully offline, scriptable LM -- no API key needed for testing, the same principle as `shared/llm/mock.py`.
- Configure `dspy.JSONAdapter()` explicitly for deterministic, single-call scripted tests -- the default adapter's fallback behavior otherwise doubles call counts.

## Lab

[`labs/01-dspy-prompt-optimization/`](../labs/01-dspy-prompt-optimization/README.md)
