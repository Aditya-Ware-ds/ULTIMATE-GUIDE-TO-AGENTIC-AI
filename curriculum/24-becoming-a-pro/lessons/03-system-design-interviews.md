# Agent system-design interviews

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~40 minutes

## Learning objectives

- Work through an agent system-design question the way a senior engineer would: clarify constraints, then reason about trade-offs, not jump to an architecture diagram.
- Draw on this curriculum's specific modules as concrete design vocabulary during a design discussion.
- Read [`system-design/`](../../../system-design/README.md)'s worked case studies as models for structuring your own answer.

## Intuition

An agent system-design interview isn't testing whether you can name every
technique this curriculum covered -- it's testing whether you can reason
about which ones a *specific* set of constraints actually calls for, the
same "match the pattern to the problem" discipline Modules 08 and 12 both
taught for topology choice, generalized to the whole system.

## The concept

### The structure of a strong answer

1. **Clarify constraints before proposing anything.** What's the actual
   task? What's the failure cost (Module 09's HITL material -- does a
   mistake need a human approval gate)? What's the expected volume (Module
   19's cost/scale material)? A senior-level answer asks these before
   sketching any architecture, the same way Module 08 lesson 05's
   workflow-vs-agent decision starts with "can the steps be enumerated,"
   not with "should I use an agent."
2. **Reason about topology (Module 12) before jumping to implementation
   details.** Does this need one agent with tools, or genuinely distinct
   specialists? Module 12 lesson 03's "when multi-agent is a mistake"
   decision process is directly the vocabulary for this step.
3. **Name the cross-cutting concerns explicitly, don't let them be an
   afterthought.** Evaluation (Module 16), observability (Module 17),
   security/permissions (Module 18), and deployment/cost (Module 19) --
   naming these unprompted, and explaining how your specific design
   addresses each, is what separates a senior-level answer from one that
   only describes the happy path.
4. **State what you'd measure to know if it's working**, and what you'd
   do differently at 10x the scale -- both signal you're thinking about the
   system as something that has to keep working, not just something that
   works once in the interview.

### Using this curriculum's modules as your vocabulary

A strong answer to "design a customer-support agent" might explicitly
invoke: Module 06's retrieval for the knowledge base, Module 09's approval
gate for refunds specifically (a consequential action, per Module 18's
least-privilege framing), Module 07's checkpointing for handling a session
that spans multiple user messages, and Module 16's eval harness for
knowing whether a prompt change actually helped. Naming these specifically
-- not "I'd use RAG" but "I'd use retrieval scoped to the specific
knowledge base, the same agentic-RAG pattern from Module 06, because the
support questions need current, sourced answers, not the model's general
knowledge" -- is what makes an answer sound like real experience rather
than recited terminology.

## Deeper: [`system-design/`](../../../system-design/README.md) has worked examples of exactly this structure

Read the case studies there before attempting your own answer to a similar
question cold -- they're built to demonstrate the four-step structure above
concretely, drawing on the same modules this lesson names, for two
realistic prompts ("design a customer-support agent platform" and "design
a multi-agent research system"). They're not meant to be memorized answers
-- the actual constraints in a real interview question will differ -- but
the *reasoning structure* transfers directly.

## When not to use this

Not every technical conversation about agents is a system-design interview
-- a debugging conversation or a code review calls for different framing
(closer to Module 13's or Module 17's material) than the constraints-first,
trade-off-driven structure this lesson describes for a genuinely open-ended
design question.

## Common mistakes

- Jumping straight to a specific framework or architecture diagram before
  clarifying the actual constraints (failure cost, volume, latency
  requirements).
- Describing only the happy path and never mentioning evaluation,
  observability, security, or cost until explicitly asked.
- Naming techniques without the reasoning for why they fit *this*
  question's specific constraints -- reciting Module 12's topology names
  without explaining which one this particular problem's structure calls
  for.

## Key takeaways

- Clarify constraints (failure cost, volume, latency) before proposing an architecture -- the same discipline Module 08's workflow-vs-agent decision and Module 12's topology choice both require.
- Name cross-cutting concerns (eval, observability, security, cost) explicitly and unprompted -- this is what a senior-level answer includes that a junior one omits.
- Use this curriculum's specific modules as concrete vocabulary, explaining *why* a pattern fits the specific constraints, not just naming it.
