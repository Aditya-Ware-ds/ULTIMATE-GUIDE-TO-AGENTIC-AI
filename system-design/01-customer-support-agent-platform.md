# Case study: design a customer-support agent platform

**Difficulty:** ★★★★☆
**Draws on:** Module 06 (RAG), Module 09 (HITL), Module 12 (multi-agent), Module 16 (evaluation), Module 18 (security), Module 19 (deployment)

## The prompt

> Design an AI agent platform that handles customer-support conversations
> for a mid-size e-commerce company: answering FAQ-style questions, looking
> up order status, and issuing refunds within policy.

This mirrors [`projects/02-customer-support-agent/`](../projects/02-customer-support-agent/README.md)
at production scale -- read that project's actual implementation alongside
this case study; the reasoning below explains *why* it's shaped the way it is.

## Step 1: Clarify constraints first

Before proposing anything, the questions a senior engineer asks:

- **What's the failure cost?** A wrong FAQ answer is embarrassing; an
  incorrectly issued refund is a direct financial loss. These need
  different treatment, not a uniform one.
- **What's the expected volume?** Thousands of conversations a day changes
  the cost-optimization calculus (Module 19 lesson 03) meaningfully versus
  dozens.
- **What's the latency expectation?** A live chat window needs a response
  in seconds; an email-based support queue tolerates more.
- **Does a human ever need to be in the loop, and for what specifically?**
  This determines where Module 09's approval gates actually go, not
  whether to have them at all.

## Step 2: Topology

This does **not** need a multi-agent system by default (Module 12 lesson
03's decision process applies directly): a single agent with three tools
-- FAQ retrieval, order lookup, and refund issuance -- covers the described
scope. A supervisor-worker split (Module 12 lesson 01) would only be
justified if support volume grows to need genuinely distinct specialist
agents (e.g., a separate agent for a different product line with entirely
different policies) -- don't add that complexity until the constraints
actually call for it.

## Step 3: The architecture

- **Retrieval (Module 06)**: FAQ answers come from agentic RAG over the
  company's actual support knowledge base, not the model's general
  knowledge -- support answers need to be current and sourced.
- **Order lookup**: a straightforward tool call to the order-management
  system's API, no retrieval needed (it's structured data, not documents).
- **Refund issuance -- the consequential action**: gated behind Module 09's
  approval pattern, and behind Module 18's least-privilege framing at the
  tool layer -- refunds have a policy-bounded maximum amount and require
  human sign-off above a threshold, enforced by the tool itself, not by
  prompting the model to "be careful with refunds." This is the same
  allowlist-style boundary as Module 18's `send_email` example, applied to
  a refund amount ceiling instead of a recipient address.
- **Escalation**: if the agent can't resolve a request within a step
  budget (Module 04/09), it escalates to a human with a structured summary
  of what it already tried (Module 09 lesson 3's escalation pattern) --
  never silently drops the conversation.
- **State across a multi-message conversation**: Module 07's checkpointing
  handles a session that spans multiple user messages, so a
  interrupted/reconnected chat session resumes correctly.

## Step 4: Cross-cutting concerns (state these explicitly, unprompted)

- **Evaluation (Module 16)**: a golden dataset of real (anonymized)
  historical support conversations with known-correct resolutions, scored
  automatically before any prompt or model change ships -- this is what
  makes "did that change help or hurt" answerable with evidence, not a
  hunch.
- **Observability (Module 17)**: every conversation traced (`invoke_agent`
  spans containing `chat`/`execute_tool` children), so a specific bad
  outcome can be replayed and diagnosed, and aggregate cost/latency
  dashboards catch drift before it becomes a support-quality complaint.
- **Security (Module 18)**: retrieved FAQ content and order data are
  untrusted input the same way any tool result is -- an indirect-injection
  attempt embedded in, say, a customer's own message history should not be
  able to make the agent issue an unauthorized refund; the refund tool's
  own amount/recipient constraints are what actually prevent that,
  independent of whether the injection succeeds at the prompt level.
- **Deployment/cost (Module 19)**: route the FAQ-answering majority of
  traffic to a cheap, fast model with a cached, stable system prompt and
  tool definitions (Module 19 lesson 03); reserve a stronger model for
  requests a routing check flags as ambiguous or high-stakes.

## What to measure, and what changes at 10x scale

Track resolution rate without escalation, average handling cost per
conversation, and refund-policy-violation rate (should be zero, enforced
mechanically, not just monitored). At 10x volume, the cost-optimization
levers (caching, routing, Module 20's distillation for the FAQ-answering
slice specifically) stop being optional -- they become the difference
between a sustainable cost structure and one that scales linearly with an
increasingly expensive per-conversation cost.
