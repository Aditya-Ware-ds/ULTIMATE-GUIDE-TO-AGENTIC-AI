# Module 20 quiz

**1. What does a DSPy `Signature` declare, and what does DSPy do with it?**

<details><summary>Answer</summary>

A signature declares a task's input and output fields (e.g.
`"question -> answer"`). DSPy generates and manages the actual prompt text
needed to get a model to fill those fields, and parses the response back
into structured fields -- you never write or parse that prompt yourself.

</details>

**2. Why does `dspy.BaseLM` matter for testing DSPy code without an API key?**

<details><summary>Answer</summary>

It's subclassable to build a fully offline, scriptable LM (this module's
`ScriptedLM`) -- the same "swap the real provider for a scriptable fake"
principle `shared/llm/mock.py` provides for every other module, applied to
DSPy's own LM abstraction.

</details>

**3. Why does this module's lab configure `dspy.JSONAdapter()` explicitly instead of using DSPy's default adapter?**

<details><summary>Answer</summary>

The default `ChatAdapter` expects a specific structured text format and
falls back to a second call through `JSONAdapter` on a parse failure --
configuring `JSONAdapter` directly avoids that extra, wasted call when
scripting plain JSON responses, keeping call counts deterministic for tests.

</details>

**4. What shape does a DSPy metric function have, and how does that compare to Module 16's LLM-as-judge?**

<details><summary>Answer</summary>

`(example, prediction, trace) -> bool | float` -- structurally identical to
Module 16's judge function, just simpler in this lab's case (an exact
check instead of an LLM call). DSPy accepts either a mechanical check or an
LLM-as-judge as a valid metric.

</details>

**5. What does `dspy.BootstrapFewShot.compile()` actually do?**

<details><summary>Answer</summary>

It runs the unoptimized program against a training set, keeps only the
examples where the metric returned true as "bootstrapped demonstrations,"
and returns a program with those demonstrations attached -- concrete,
inspectable few-shot examples selected because they empirically passed the
metric, not a vague notion of "improved."

</details>

**6. Why should you inspect `optimized_program.demos` after compiling, rather than just trusting that `.compile()` ran without error?**

<details><summary>Answer</summary>

A successful return doesn't prove optimization actually selected anything
useful -- the same "don't infer success from the absence of an error"
discipline as Module 13's independent test re-run and Module 12's explicit
worker status. `demos` being a real, non-empty, correct list is the actual
evidence optimization happened.

</details>

**7. How does distillation differ from simply routing easy requests to a smaller off-the-shelf model (Module 19)?**

<details><summary>Answer</summary>

Routing sends easy requests to a small model that may or may not handle
them well as-is. Distillation trains a small model specifically to
imitate a larger model's outputs on your task's actual input distribution
-- a targeted training process, not just a routing decision.

</details>

**8. Why should fine-tuning generally be tried after prompt optimization and model routing, not before?**

<details><summary>Answer</summary>

Fine-tuning requires real training infrastructure and a sizable,
high-quality dataset -- a heavier, more expensive commitment than
prompt-level optimization or routing, which are cheaper and faster to
iterate on and often sufficient on their own.

</details>

**9. Why must a distilled or fine-tuned model still be evaluated with Module 16's eval harness before deployment?**

<details><summary>Answer</summary>

Distillation and fine-tuning quality are empirical questions, not
guarantees of the process itself -- a smaller model trained to imitate a
larger one can still fail to generalize well; only a real eval against
representative data confirms it's actually good enough to deploy.

</details>

**10. Why is an open-weight/local model (Module 01's `OllamaProvider`) sometimes the cheapest available option, and when is it not the right choice?**

<details><summary>Answer</summary>

For a task where a smaller open-weight model already clears the accuracy
bar (verified via Module 16's eval harness), running it locally avoids
per-token hosted-API costs entirely. It's the wrong choice when the task
genuinely needs capability only a larger hosted model currently provides,
or when local infrastructure/ops overhead outweighs the savings.

</details>
