# Assessing reproducibility

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~30 minutes

## Learning objectives

- Judge whether a paper's method is actually reproducible from what it publishes, not from what it claims.
- Identify the specific details (prompts, hyperparameters, exact dataset splits) that determine real reproducibility for LLM/agent research specifically.
- Attempt a small, honest reproduction of a paper's simplest claim before trusting it fully.

## Intuition

"We release our code" doesn't automatically mean a result is reproducible
-- for LLM and agent research specifically, reproducibility depends on
details that are easy to omit and hard to reconstruct after the fact: exact
prompts, exact model versions and dates (since hosted models change),
sampling parameters, and the precise evaluation harness.

## The concept

### What actually needs to be specified for an agent paper to be reproducible

- **The exact prompts used**, not a paraphrased description of them --
  Module 02's lesson on prompt sensitivity applies directly: a
  differently-worded prompt can produce meaningfully different results,
  so "we used a system prompt instructing the model to reason step by
  step" is not enough to reproduce the actual number reported.
- **The exact model identifier and date**, since hosted models can be
  updated silently -- a result from "GPT-4" without a specific dated
  snapshot identifier may not be reproducible even with access to an
  API, because the model behind that name may have changed.
- **Sampling parameters** (temperature, top-p) -- Module 01's sampling
  lesson covered why these change output distribution meaningfully; a
  paper reporting results without specifying them leaves a real gap.
- **The exact evaluation harness and dataset split** -- code released
  without the specific eval script and data split used to produce the
  headline numbers is only partially reproducible.

### Attempting a small reproduction

Before trusting a paper's central claim, attempt the smallest possible
version of it yourself: one example from their dataset, their described
method, and see if you get a broadly similar result. This doesn't need to
match their exact number -- it needs to reveal whether the method as
*described* actually behaves the way the paper claims, at all. A method
that fails even this minimal sanity check is a strong signal something
important was omitted or misdescribed.

### Verified vs. unverifiable claims -- name the difference explicitly

When you can't reproduce a claim (no released code, no released prompts,
no accessible model version), say so explicitly rather than reporting the
paper's number as if you'd confirmed it -- the same "mark UNVERIFIED if
unsure" discipline this entire curriculum's Ground Rule 2 has followed
throughout its own construction.

## Deeper: this curriculum's own labs are a model of what reproducibility looks like

Every lab in this repository specifies its exact scripted inputs (the mock
provider's exact responses), its exact expected outputs, and a runnable
test that confirms the claimed behavior -- nothing is asserted without a
way to check it. This is the standard research reproducibility should be
held to, made concrete: if you can't hand someone the exact inputs and a
way to check the exact outputs, the claim isn't yet reproducible, no matter
how confidently it's stated.

## When not to use this

A blog post or a vendor's own documented feature (verified directly against
official docs and, where possible, the installed package -- this
curriculum's standard practice since Module 10) doesn't need this same
reproducibility audit; it needs the verification discipline from Module 01
lesson-equivalent (check the primary source, date it), which is a related
but distinct check.

## Common mistakes

- Treating "code is available on GitHub" as sufficient for reproducibility
  without checking whether the exact prompts/hyperparameters used for the
  headline results are actually included.
- Reporting a paper's number in your own work as if verified, when you
  haven't actually attempted any reproduction of it.
- Assuming a result reproduces on a newer model version just because it's
  "the same model family" -- Module 01's point about models changing over
  time applies to reproduction attempts specifically.

## Key takeaways

- Real reproducibility for LLM/agent research requires exact prompts, dated model versions, sampling parameters, and the specific eval harness -- not just "code is released."
- Attempt the smallest possible reproduction before trusting a paper's central claim; a method that fails even a minimal sanity check signals something important was omitted.
- Explicitly mark a claim as unverified when you can't reproduce it, rather than reporting it as confirmed.
