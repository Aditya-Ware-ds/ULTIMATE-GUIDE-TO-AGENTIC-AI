# Worked example: reading the GRPO paper critically

**Last verified:** 2026-09-22 (paper confirmed real via its arXiv abstract; see resources.md)
**Difficulty:** ★★★★☆ · **Time:** ~30 minutes

## Learning objectives

- Apply lessons 01-02's framework to a real, specific paper this curriculum already uses (Module 21).
- See concretely what "verified" vs. "not independently verified" looks like in practice, in a single worked example.
- Practice being honest about the limits of your own verification, not just critiquing someone else's.

## Intuition

Module 21 built a real, working implementation of GRPO's advantage
formula, using a paper (DeepSeekMath, which introduced GRPO) as the source.
This lesson goes back to that same paper and applies lessons 01-02's
critical-reading framework to it directly -- including being explicit about
which of the paper's claims this curriculum actually verified, and which it
did not.

## The concept

### The claim, separated from the framing

**Paper**: "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in
Open Language Models" (confirmed real via its arXiv abstract, 2402.03300).
Its introduced method, GRPO (Group Relative Policy Optimization), is
described in the abstract as "a variant of Proximal Policy Optimization
(PPO)" that "enhance[s] mathematical reasoning abilities while concurrently
optimizing the memory usage of PPO." The specific, falsifiable claim worth
separating from the paper's broader framing (about mathematical reasoning
generally) is narrower and more mechanical: **GRPO computes a policy
advantage from a group of sampled completions' rewards, without training a
separate critic/value network, reducing memory versus PPO.**

### What this curriculum actually verified, and how

- **Confirmed directly**: the paper's title, authorship, and the abstract's
  core framing (GRPO as a memory-efficient PPO variant) -- verified by
  fetching the paper's own arXiv abstract page.
- **Confirmed against a second, independent, current source**: the exact
  advantage formula (`(reward - group_mean) / group_std`) and the
  "no separate critic model" claim -- verified against Hugging Face TRL's
  current GRPO trainer documentation, an independent implementation of the
  method, not just a restatement of the paper's own description.
- **Not independently verified by this curriculum**: the paper's specific
  reported benchmark numbers (exact mathematical-reasoning accuracy
  figures, comparisons against specific baselines) -- Module 21's lab
  implements and tests the *formula*, which is a mechanical, checkable
  claim; it does not attempt to reproduce DeepSeekMath's own reported
  end-to-end training results, which would require real training
  infrastructure this curriculum's ground rules explicitly keep out of
  scope (see Module 21's README).

### Why this two-source verification mattered

Relying on the paper's abstract alone (which WebFetch's first attempts at
the raw PDF failed to extract usable text from -- a real, mundane
reproducibility obstacle lesson 02 warns about: not every source is easy to
actually check) would have left the exact formula unconfirmed. Checking a
second, independent, current implementation (Hugging Face TRL) against the
same claim is exactly lesson 02's "attempt a small reproduction" principle
in miniature -- not training a model, but confirming the specific
mechanical claim (the formula) against an independent source before
building and testing real code around it.

## Deeper: this lesson is itself an example of the discipline, not just a description of it

Notice this lesson doesn't claim to have verified DeepSeekMath's full
experimental results -- it explicitly separates what was checked (the
formula, the framing, via two independent sources) from what wasn't (the
paper's specific benchmark numbers). That explicit boundary is what lessons
01-02 are actually asking you to practice: not blanket trust, and not
blanket skepticism, but a precise account of what you actually confirmed.

## When not to use this

A two-source verification process is overkill for a claim you're not going
to build anything on top of -- reserve this level of scrutiny for claims
that will actually inform a real decision or a real piece of code, the way
Module 21's lab does here.

## Common mistakes

- Citing a paper's title and framing as if that alone verifies its specific
  technical claims -- confirming a paper exists and confirming its formula
  is correct are two different checks.
- Skipping the "what wasn't verified" step, leaving a reader unable to tell
  which parts of a summary are confirmed and which are simply repeated from
  the source.
- Assuming a paper introducing a method is the only source worth checking
  it against -- an independent, current implementation (like this lesson's
  use of Hugging Face TRL) is often a more directly checkable source for a
  specific mechanical claim than the original paper's prose.

## Key takeaways

- A paper's title/existence, its framing, and its specific technical claims are three separate things to verify -- confirming one doesn't confirm the others.
- Cross-checking a specific claim against an independent, current implementation (not just the original paper) is a concrete, practical form of lesson 02's "attempt a small reproduction."
- Always state explicitly what you did and didn't verify -- Module 21's lab implements and tests GRPO's formula specifically because that was the verifiable part; it never claims to reproduce the paper's full training results.
