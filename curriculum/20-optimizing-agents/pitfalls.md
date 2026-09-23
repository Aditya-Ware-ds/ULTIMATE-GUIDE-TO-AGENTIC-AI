# Module 20 pitfalls

## Trusting an LLM-generated DSPy code sample instead of checking the installed package

DSPy's API has changed meaningfully across versions (the `BaseLM` docstring
in the version this module was verified against, 3.3.1, explicitly
describes an in-progress migration from a "legacy" `forward()` contract to
a new typed one). A code sample that looks plausible from general knowledge
can easily target a different version's shape. This module's lessons and
lab were written only after installing `dspy` for real
(`uv run --with dspy python -c "..."`) and reading its actual installed
source with `inspect.getsource()` -- the same technique Module 10's and
Module 11's pitfalls both name as required for any fast-moving dependency,
now confirmed necessary for DSPy too.

## Returning a plain `dict` from a custom `BaseLM.forward()`

DSPy's legacy contract expects an OpenAI-response-shaped object accessed
via `.choices[0].message.content`, `.usage`, and `.model` -- not a dict
with those as keys. Returning a plain dict fails with an
`AttributeError: 'dict' object has no attribute 'choices'` deep inside
DSPy's internals, which can look like a DSPy bug rather than what it
actually is: a contract mismatch in your own `forward()`'s return value.
Use an object with real attribute access (this lab's solution uses
`types.SimpleNamespace`) for `.choices`/`.model`, but a genuine `dict` for
`.usage` specifically -- DSPy converts usage via `dict(...)`, which works on
a dict but not on a `SimpleNamespace`.

## Not configuring `dspy.JSONAdapter()` and being confused by doubled call counts

Without an explicit adapter, DSPy's default `ChatAdapter` tries to parse a
specific structured-text response format; a scripted LM returning plain
JSON fails that parse and DSPy silently falls back to a second call through
`JSONAdapter`. A test asserting `len(lm.calls) == 1` will fail with 2 --
easy to misdiagnose as "the scripted LM is being called twice for no
reason" when the actual cause is simply an unconfigured adapter.

## Treating a passing `test_optimize_program_bootstraps_real_demonstrations`-style test as proof the optimized program generalizes

This lab's training set has exactly two examples -- enough to prove the
optimization *mechanism* works correctly (real demos, selected via the real
metric), but far too small to demonstrate genuine generalization to
questions outside it. Don't extrapolate from a lab-scale demonstration like
this one to "DSPy optimization works well" for a real task without a
properly representative training set and a real held-out eval (Module 16),
the same caution lesson 02 and lesson 01's "when not to use this" both
raise.
