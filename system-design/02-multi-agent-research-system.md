# Case study: design a multi-agent research system

**Difficulty:** ★★★★★
**Draws on:** Module 06 (RAG), Module 12 (multi-agent), Module 16 (evaluation), Module 17 (observability), Module 19 (deployment)

## The prompt

> Design a system that takes a research question, investigates it across
> multiple sources, and produces a cited report -- similar in spirit to
> [`projects/01-research-assistant/`](../projects/01-research-assistant/README.md)
> and the "multi-agent content pipeline"
> ([`projects/04-multi-agent-content-pipeline/`](../projects/04-multi-agent-content-pipeline/README.md)),
> but at a scale where a single agent's context window becomes the limiting
> factor.

## Step 1: Clarify constraints first

- **How deep does the research need to go?** A single-source lookup is a
  different system than one requiring synthesis across dozens of documents
  -- this determines whether multi-agent (Module 12) is even justified
  (lesson 03's decision process: does this genuinely need distinct
  specialist skills or real parallelism, or would one well-tooled agent
  suffice?).
- **What's the acceptable latency?** Multi-agent systems add real latency
  (Module 12 lesson 03) -- a report needed in seconds rules out a deep,
  multi-stage pipeline regardless of quality benefits.
- **How is correctness verified?** Citations that don't actually support
  their claims are worse than no citations -- this determines the
  evaluation approach (Module 16) from the start, not as an afterthought.

## Step 2: Topology -- here, multi-agent earns its cost

Unlike the customer-support case study, this problem genuinely has
distinct specialist sub-skills and real parallelism opportunity: a
**researcher** (retrieves and summarizes per-source), a **writer**
(synthesizes retrieved material into a coherent report), and a **critic**
(checks the draft's citations actually support its claims) -- exactly
`projects/04-multi-agent-content-pipeline/`'s topology (Module 12 lesson
01's supervisor-worker pattern, specialized). Multiple researcher instances
can run in parallel across independent sources (Module 08's
parallelization, feeding into Module 12's orchestrator-workers shape).

## Step 3: The architecture

- **Retrieval per source (Module 06)**: each researcher worker gets a
  narrow, focused context -- its own source, not the whole investigation's
  accumulated history (Module 12 lesson 01's context-budget point,
  inherited from Module 08 lesson 04).
- **Citation tracking**: extract and verify citations mechanically
  (`projects/01-research-assistant/`'s `extract_citations`/
  `verify_citations` pattern) rather than trusting the writer's claim that
  a citation is accurate -- Module 12 lesson 02's "explicit status, not
  inferred success" applied to citation correctness specifically.
- **The critic stage is not optional**: per Module 12's core lesson, the
  pipeline should escalate (not silently publish) if the critic finds
  unsupported claims, the same discipline as
  `projects/04-multi-agent-content-pipeline/`'s escalation-on-research-
  failure behavior.
- **Failure modes to design against explicitly (Module 12 lesson 02)**:
  duplicated research (two researcher workers investigating the same
  source redundantly -- mitigate with shared, visible claimed/in-progress
  state) and a system-wide step/cost budget across the *entire* pipeline,
  not just per-agent, to prevent an infinite research-revise loop.

## Step 4: Cross-cutting concerns (state these explicitly, unprompted)

- **Evaluation (Module 16)**: an LLM-as-judge specifically for "does this
  citation actually support this claim" (a genuinely open-ended judgment,
  appropriate for Module 16 lesson 02's LLM-as-judge rather than a
  mechanical check), evaluated against a golden set of question/report
  pairs with known citation-accuracy issues planted in the source material.
- **Observability (Module 17)**: this is exactly the scenario Module 17
  lesson 02 names directly -- multi-agent debugging needs the whole
  conversation/handoff graph (each worker's spans nested under the
  supervisor's `invoke_agent` span), not any single agent's log in
  isolation, to diagnose why a specific report came out wrong.
- **Cost (Module 19)**: multi-agent multiplies token spend across every
  agent involved (Module 08's parallelization cost point, restated for
  multi-agent) -- track cost per completed, citation-verified report, not
  just cost per research pipeline invocation, since a report that fails
  the critic stage and needs revision costs more than one that passes
  cleanly the first time.

## What to measure, and what changes at 10x scale

Track citation-accuracy rate (from the critic/eval, not self-reported),
end-to-end latency, and cost per verified report. At 10x scale, the
research-worker parallelism (Module 08) becomes the primary lever for
latency, while the critic stage's own cost (an extra full pass per report)
becomes worth optimizing specifically -- a cheaper, distilled model
(Module 20) trained specifically on the citation-verification task is a
natural next step once there's enough real critic-stage traffic to
distill from.
