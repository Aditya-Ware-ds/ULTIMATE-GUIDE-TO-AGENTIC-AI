# Module 16 pitfalls

## Building a golden dataset that's really just "the easy cases"

It's tempting to populate a golden dataset with clean, unambiguous questions
that any reasonable agent gets right on the first try -- the eval then
reports a reassuringly high accuracy that tells you almost nothing about
how the agent handles the genuinely hard or edge-case inputs that cause
real production failures. A useful golden dataset deliberately includes the
inputs that have actually caused problems before (or are likely to), not
just ones that are easy to write.

## Trusting a judge's verdict as ground truth without spot-checking it

`judge()` is itself an LLM call, and it can be wrong -- confidently. If you
never compare a sample of its verdicts against your own read of the
question and answer, a systematically biased or miscalibrated judge can
silently produce a misleading accuracy number for a long time before anyone
notices the eval harness itself is the thing that's broken, not the agent
it's grading.

## Letting `evaluate_dataset` call the judge even when the agent's answer is obviously well-formed and correct

For a task with a genuinely mechanical check available (Module 13's exact
principle -- run the tests, or in this case, parse and compare a number),
routing every single item through an LLM judge anyway is unnecessary cost
and adds judge-bias risk for cases that never needed it. Use the mechanical
check first, and reserve the judge for genuinely open-ended grading, per
lesson 02's "when a judge isn't the right tool at all" section.

## Reading only the aggregate accuracy after a change, not the per-item results

An aggregate score staying flat after a change can hide real movement
underneath it -- three previously-passing items newly failing, offset by
three previously-failing items newly passing. `evaluate_dataset`'s
`results` list exists specifically so a regression is debuggable ("which
specific items changed and why"), not just detectable as a number moving.
Always diff the per-item results against the previous run, not just the
top-line accuracy.
