# Module 23 quiz

**1. Why should you separate a paper's claimed contribution from its framing before evaluating it?**

<details><summary>Answer</summary>

A paper might improve results through a confounded variable (a stronger
base model, more compute) rather than through the specific novel
contribution it's framed around -- separating the two lets you assess
whether the actual claimed mechanism is what produced the improvement, not
just whether the numbers went up.

</details>

**2. What three things should you check about a paper's evaluation methodology before trusting its reported improvement?**

<details><summary>Answer</summary>

The baseline it's compared against (weak/outdated baselines inflate
apparent improvement), whether the eval set is independent of what the
method was tuned against, and whether results account for run-to-run
variance rather than reporting a single stochastic run as a finding.

</details>

**3. Why is a paper's limitations section often more useful than its results section for deciding whether to use a method?**

<details><summary>Answer</summary>

It's where authors state, in their own words, what the method doesn't
handle -- exactly the information needed to judge whether a result applies
to your specific problem, which the results section (framed to highlight
success) typically doesn't emphasize.

</details>

**4. Why doesn't "the authors released their code" guarantee a result is reproducible?**

<details><summary>Answer</summary>

For LLM/agent research specifically, reproducibility also depends on exact
prompts, dated model versions (hosted models change), sampling parameters,
and the exact eval harness/data split -- all of which can be omitted even
when code is released.

</details>

**5. What should you do before fully trusting a paper's central claim, per lesson 02?**

<details><summary>Answer</summary>

Attempt the smallest possible reproduction yourself -- one example, their
described method -- to see if the method as described behaves the way
claimed at all, before trusting the full-scale reported result.

</details>

**6. In the worked example (lesson 03), what specifically was verified against a source independent of the DeepSeekMath paper itself?**

<details><summary>Answer</summary>

GRPO's exact advantage formula and its "no separate critic model" property
were verified against Hugging Face TRL's current, independent
implementation documentation -- not just restated from the paper's own
description.

</details>

**7. What did the worked example explicitly NOT claim to have verified?**

<details><summary>Answer</summary>

DeepSeekMath's own specific reported benchmark/accuracy numbers and
end-to-end training results -- Module 21's lab implements and tests only
the mechanical advantage formula, which doesn't require real training
infrastructure, and the lesson is explicit that this is a narrower claim
than the paper's full experimental results.

</details>

**8. Why does this module connect its own discipline back to Modules 14 and 18's corrections?**

<details><summary>Answer</summary>

Both modules caught a stale or unverifiable claim (Module 14's
"accessibility tree" computer-use assumption; Module 18's "OWASP Agentic
Top 10, ASI01-10, ranked #3" claim) by checking primary sources instead of
trusting a prior summary -- the exact discipline this module names and
teaches explicitly, already practiced concretely earlier in this same
curriculum.

</details>

**9. Why is "the paper is from a well-known lab" not sufficient reason to trust a specific claim within it?**

<details><summary>Answer</summary>

Reputation reflects the source's general track record, not whether the
*specific* claim's evidence (baseline, eval set, methodology) actually
supports it -- read the argument itself, since even reputable sources can
have a specific claim that doesn't hold up to the same scrutiny lesson 01
describes.

</details>

**10. What should you do when you can't reproduce or independently verify a paper's claim?**

<details><summary>Answer</summary>

State explicitly that it's unverified rather than reporting it as
confirmed -- the same "mark UNVERIFIED if unsure" discipline this
curriculum's own ground rules have followed throughout its construction.

</details>
