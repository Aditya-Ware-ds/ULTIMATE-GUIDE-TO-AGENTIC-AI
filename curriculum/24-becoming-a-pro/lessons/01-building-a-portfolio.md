# Building a portfolio

**Last verified:** 2026-09-22
**Difficulty:** ★★★☆☆ · **Time:** ~30 minutes

## Learning objectives

- Turn this curriculum's own projects into specific, defensible portfolio pieces.
- Write a project description that demonstrates judgment, not just that code runs.
- Decide which of your projects/labs are worth showcasing versus which were purely for learning.

## Intuition

"I completed a course on AI agents" is not a portfolio -- it's a claim.
"I built a coding agent that fixes real bugs inside a sandboxed
subprocess, with a red-teamed permission boundary and a golden-dataset
eval harness" is specific, checkable, and demonstrates judgment a hiring
manager or collaborator can actually evaluate. The difference is entirely
in the specificity and the evidence of trade-off decisions, not the
underlying technology.

## The concept

### What actually makes a portfolio piece credible

- **A specific, real decision you made and can explain.** Not "I used
  DSPy" but "I chose `BootstrapFewShot` over manual prompt engineering
  because the task had a clear metric and a training set, and I could show
  the optimized program's bootstrapped demonstrations as evidence it
  actually improved" (Module 20).
- **Evidence of things going wrong and being fixed**, not just a finished
  result. Module 18's red-team lab -- "I found a real indirect-injection
  exploit, proved it with a failing test, and fixed it with a tool-level
  permission boundary" -- is more credible than "I built a secure agent"
  alone, because it shows the actual security reasoning, not just a claim
  of security.
- **A working, runnable artifact**, not a description. Every lab in this
  curriculum already has this property (a starter, a solution, a real test
  suite) -- the discipline of "all code must run" this whole curriculum
  practiced is exactly what makes a project a credible portfolio piece
  instead of a described one.

### Which projects to showcase

Not every lab needs to be a portfolio piece -- the five interleaved
projects (research assistant, customer-support agent, MCP server, content
pipeline, data-analysis agent) and the three capstones are built at
exactly the scale and integration-depth worth showcasing; individual
module labs are better referenced as "I understand X specifically" evidence
within a larger project's writeup than as standalone portfolio items.

### Writing the project description

Lead with the specific problem and the specific trade-off, not the
technology list. "Built an agent that fixes bugs inside `subprocess`-level
sandboxing after evaluating and rejecting a broader `exec()`-based
approach for security reasons" tells a reader more about your judgment
than "Built a coding agent using Python."

## Deeper: your capstones are supposed to be your strongest pieces

The three capstones (built after this module) are explicitly designed to
ship with the artifacts a real production team would expect -- a spec, an
architecture doc, an eval suite, a threat model, a deploy guide -- not just
code. That's not incidental scope creep; it's the format that makes a
capstone the strongest kind of portfolio piece this curriculum produces,
because it demonstrates the same judgment a real engineering role requires,
not just coding ability.

## When not to use this

Don't over-produce portfolio material for projects you built purely to
learn a specific technique and don't plan to maintain or discuss in depth
-- a portfolio's credibility comes from depth on a few pieces you can
actually defend under questioning, not breadth across everything you built.

## Common mistakes

- Listing technologies used ("LangGraph, DSPy, FastAPI") instead of
  decisions made and trade-offs considered.
- Showcasing a project you can't actually explain the internals of under
  follow-up questions -- depth you can defend beats breadth you can't.
- Treating every lab as equally portfolio-worthy, diluting the strongest
  pieces (the projects and capstones) among many smaller, less complete ones.

## Key takeaways

- A credible portfolio piece demonstrates a specific decision and trade-off, backed by a real, runnable artifact -- not a technology list or a vague completion claim.
- Evidence of a real problem found and fixed (Module 18's red-team pattern) is more credible than a claim of quality alone.
- This curriculum's projects and capstones are built at the right scale to showcase; individual module labs are better used as depth evidence within those larger writeups.
