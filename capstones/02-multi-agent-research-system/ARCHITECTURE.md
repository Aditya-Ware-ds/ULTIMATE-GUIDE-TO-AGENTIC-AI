# Architecture -- Multi-agent research system

## Overview

```
                        invoke_agent research-pipeline
                                    │
        ┌───────────────────┬──────┴──────┬──────────────────┐
        ▼                   ▼             ▼                  ▼
  invoke_agent          invoke_agent  invoke_agent      invoke_agent
   researcher              writer       critic         writer (revision)
        │                   │             │                  │
     chat span           chat span    chat span          chat span
```

Structurally identical to `projects/04-multi-agent-content-pipeline/`'s
supervisor-worker topology (Module 12 lesson 01) -- a top-level flow
dispatching to researcher, writer, and critic workers, with a bounded
revision loop between writer and critic. This capstone's contribution is
making that structure **observable** (Module 17) and **measurable**
(Module 16), not redesigning the topology itself.

## Design rationale

### Why each worker gets its own `invoke_agent` span, not just a `chat_span`

A flat trace (three `chat` spans with no grouping) tells you three model
calls happened, but not which one was "the researcher" vs. "the critic" --
exactly the visibility gap Module 17 lesson 02 names as the reason
multi-agent debugging needs the whole graph, not a flat event list.
Wrapping each worker's call in its own `invoke_agent_span` makes the
exported trace directly answer "which agent did what, and in what order,"
which is what actually makes a bad output diagnosable after the fact.

### Why citations are numbered references to `research`'s own facts, not free-text sourcing

Verifying "is this citation accurate" against arbitrary free-text sourcing
would require another LLM call (an LLM-as-judge, Module 16 lesson 02) --
genuinely more expensive and less reliable than a mechanical check.
Numbering the facts `research` already returns and asking `draft` to cite
them by number makes citation-accuracy verification a pure, deterministic
string-parsing operation (`extract_citations`/`verify_citations`), the
same "prefer a mechanical check over a judgment call" principle Module 13
and Module 16 both apply elsewhere in this curriculum.

### Why the eval suite takes the pipeline function and client factory as parameters

Identical reasoning to Capstone 1's `eval_harness.py`: an eval suite tied
to one specific pipeline implementation is weaker infrastructure than one
that can score any pipeline with a compatible signature (Module 16's
`evaluate_dataset` shape). This also makes it trivial to compare two
pipeline variants (e.g. with and without a critic stage) against the same
eval suite.

### Why the mean citation accuracy excludes escalated topics

A topic that never reached a citable article shouldn't be scored `0.0` for
citation accuracy -- that would conflate "the pipeline correctly refused an
unresearchable topic" (a success of the escalation mechanism, Module 12
lesson 02) with "the pipeline produced inaccurate citations" (an actual
quality failure). Averaging only over `"success"` results keeps these two
distinct failure modes from being conflated into one misleading number.

## What this capstone does not attempt

The citation-accuracy check only verifies that cited numbers are
*in-range* references to real facts -- it does not verify that the cited
sentence's actual content matches what that fact says (which would require
an LLM-as-judge, a real cost/reliability tradeoff per Module 16 lesson 02).
A production system would likely want both: the cheap mechanical check
this capstone implements as a fast first-pass filter, and an LLM-as-judge
spot-check on a sample of outputs for deeper accuracy verification.
