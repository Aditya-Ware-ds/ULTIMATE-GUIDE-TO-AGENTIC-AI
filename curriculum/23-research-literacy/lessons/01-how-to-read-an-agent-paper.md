# How to read an agent paper

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~40 minutes

## Learning objectives

- Separate a paper's actual claimed contribution from its framing and marketing.
- Identify what a paper's evaluation methodology does and doesn't demonstrate.
- Read a paper's limitations section as seriously as its results section.

## Intuition

A paper's abstract and introduction are written to be persuasive -- that's
not dishonest, it's the genre. Reading critically means extracting the
actual, falsifiable claim underneath the framing, and checking whether the
paper's own evidence actually supports it, independent of how confidently
it's stated.

## The concept

### Separate the claim from the framing

Every agent paper makes some version of "we improve X." The critical
questions: improve X *compared to what specific baseline*, *on what
specific task distribution*, *by how much*, and *is that improvement the
paper's actual novel contribution or an incidental side effect of a
different change* (a bigger model, more compute, a different eval set) the
paper doesn't isolate for. A paper claiming a "new agent architecture"
that also happens to use a stronger base model than its baselines has
conflated two variables -- the architecture might contribute nothing.

### Read the evaluation methodology like an audit

- **What benchmark(s), and are they the right fit for the claim?** (Module
  16 lesson 03's benchmark table is exactly this kind of fit-check applied
  to this curriculum's own claims.)
- **What's the baseline comparison?** A weak or outdated baseline makes any
  improvement look larger than it would against a current, competitive one.
- **Is the eval set the same one the method was tuned against?** Module
  16 lesson 01's "golden dataset must be representative, and untouched by
  what it's evaluating" caution applies identically to a paper's claimed
  results -- a method evaluated only on the data it was developed against
  tells you much less than one evaluated on a genuinely held-out set.
- **Are results reported with variance/multiple runs, or a single number?**
  LLM outputs are stochastic; a single run's result can be noise dressed up
  as a finding.

### Take the limitations section seriously

A paper's limitations section is often the most informative part for
deciding whether a result applies to *your* problem -- it's where authors
state, in their own words, what their method doesn't handle. Skipping
straight from the abstract to "how do I use this" skips exactly the part
that tells you when not to.

## Deeper: this is the same discipline Ground Rule 1 has required all along

This curriculum's own ground rules (never fabricate, verify claims against
current sources, date-stamp) are research literacy applied to building a
curriculum instead of reading a paper. Modules 14 and 18 both demonstrate
this concretely: an earlier working assumption ("computer-use tools use
accessibility trees") and an earlier plan claim ("OWASP Agentic Top 10,
ASI01-10, ranked #3") were both caught as stale or unverifiable *by
applying exactly this lesson's discipline* -- checking the primary source
rather than trusting a plausible-sounding prior summary.

## When not to use this

Not every piece of agent-AI writing needs this level of scrutiny -- a
vendor's own API documentation (which this curriculum verifies directly
via installed packages and official docs throughout) is a different kind
of source than a research paper's claims about a novel method's
performance, and doesn't need the same "what's the baseline, what's the
eval set" audit.

## Common mistakes

- Trusting an abstract's stated improvement number without checking what
  baseline and eval set it was measured against.
- Treating a paper's limitations section as boilerplate to skip, rather
  than the part most likely to tell you whether the method applies to your
  actual problem.
- Confusing "the paper is prestigious/from a well-known lab" with "the
  specific claim I care about is well-supported by its actual evidence" --
  read the argument, not the byline.

## Key takeaways

- Extract the actual, falsifiable claim from a paper's framing, and check whether its own evidence isolates that claim from confounding variables.
- Audit the evaluation methodology: baseline, eval-set independence, and whether results account for run-to-run variance.
- Read the limitations section as seriously as the results -- it's often the most useful part for deciding whether a method applies to your problem.
