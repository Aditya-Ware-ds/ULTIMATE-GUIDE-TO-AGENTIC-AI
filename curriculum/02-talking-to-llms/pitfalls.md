# Module 02 pitfalls

## Silently losing conversation history

If `chat_once` builds a fresh `messages` list from scratch each call instead of
including everything already in `history`, your tests may still pass if they
only check the *return value* of a single call -- the bug only shows up when you
specifically check (as `test_chat_once_second_call_sees_full_history` does) that
the *second* call's request actually included the first turn. This is worth
internalizing beyond the lab: "the function returned the right answer on this
one call" and "the function is managing state correctly across calls" are
different things to test, and agent bugs (Module 04 onward) are disproportionately
the second kind.

## Catching exceptions that the spec asked you to let propagate

`extract_structured`'s spec explicitly says let `json.JSONDecodeError` and
`jsonschema.ValidationError` propagate. A tempting "helpful" instinct is to catch
them and return `None` or an empty dict instead. Resist it here -- the tests
check for the specific exception types, and more importantly, silently returning
an empty result on a parse/validation failure hides a real problem from
whatever code calls this function next. Decide *where* a failure should be
handled deliberately (usually higher up, closer to where you can actually do
something about it -- retry, log, surface to a user) rather than swallowing it
at the first opportunity.

## Treating a passing mock test as proof a real provider will behave the same way

Every test in this lab runs against `MockLLMProvider`, which returns exactly
what you scripted -- it never fails to produce valid JSON, never returns an
unexpected tool call, never rate-limits you. Passing these tests proves your
*handling code* is correct; it does not prove a real provider will always
produce schema-conforming output or that your code handles a real provider's
actual failure modes (a 429, a malformed response, a timeout). That's exactly
what `live`-marked tests (Module 00's `LAB_TARGET`/`live` marker pattern,
extended in later modules) are for -- don't skip real-provider testing
altogether just because the mock suite is green.

## Forgetting `strict=True` in `zip()` when pairing history entries

Not directly exercised by this lab's own tests, but a closely related habit: when
you pair two lists that are supposed to be the same length (like `zip(a, b)` in
the embeddings lesson's cosine similarity), always use `zip(a, b, strict=True)`
in Python 3.10+. Without it, `zip` silently truncates to the shorter list instead
of raising an error -- a length mismatch becomes a quiet wrong answer instead of
a loud, debuggable exception.
