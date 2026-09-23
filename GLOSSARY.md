# Glossary

Terms as used consistently throughout this repo. If a lesson uses a term
differently from this list, the lesson is wrong -- file an issue. This glossary
grows as modules are built; see `PROGRESS.md` for what's covered so far.

**Agent** -- A system where an LLM decides its own sequence of actions (which tools
to call, in what order, when to stop) to accomplish a goal, as opposed to a fixed
pipeline. See Module 04.

**Agent loop** -- The observe → think → act cycle an agent runs repeatedly until it
decides it's done or hits a stopping condition. See Module 04.

**Checkpoint / resume** -- Persisting an agent's in-progress state (conversation
history, step count) to durable storage so a killed or interrupted run can pick up
where it left off instead of restarting. See Module 07. Distinct from a **progress
file** (below), which tracks status across many largely-independent tasks rather
than one continuous conversation.

**Compaction** -- Shrinking conversation history (via summarization, truncation, or
selective removal) to stay within the context window as an agent runs long. See
Module 05.

**Context rot** -- The degradation of an LLM's effective attention/accuracy as
irrelevant or stale content accumulates in its context window, even before the
window is technically full. See Module 05.

**Context window** -- The maximum number of tokens (input + output combined, for
most current APIs) a model can attend to in a single call. See Module 01.

**Context engineering** -- Deliberately deciding what goes into an agent's context
window (system prompt, tool descriptions, history, retrieved documents) and how
it's structured, as a first-class design activity rather than an afterthought. See
Module 05.

**Distillation** -- Training a smaller, cheaper model to imitate a larger model's
outputs on a specific task's actual input distribution, rather than switching to an
off-the-shelf small model directly. See Module 20.

**Evaluator-optimizer** -- A pattern where one LLM call produces an output and a
second evaluates/critiques it, looping until the evaluator is satisfied or a budget
is exhausted. See Module 08.

**Human-in-the-loop (HITL) / approval gate** -- Pausing an agent before a
consequential action so a human can approve or reject it, with the ability to
resume afterward. Distinct from -- and best combined with -- an allowlist enforced
inside the tool itself: approval alone should never be the only safeguard for a
genuinely high-stakes action. See Module 09 and Module 18.

**Idempotency key** -- A unique value a client generates once per logical request
and reuses on every retry, so a repeated request returns the already-computed
result instead of re-running (and re-triggering any consequential side effects of)
the underlying work. See Module 19.

**Indirect prompt injection** -- Prompt injection where the malicious instruction
comes not from the user's own message but from content the agent reads while doing
its job (a retrieved document, a tool result, a web page) -- see **Prompt
injection**, below. See Module 18.

**LLM-as-judge** -- Using an LLM call to score or compare outputs for evaluation
purposes, instead of (or alongside) exact-match or human grading. Carries known
biases (e.g. preferring longer or more confident-sounding answers) covered in
Module 16.

**Least privilege / tool permissions** -- Constraining what a tool is capable of
doing (an allowlist of files, URLs, recipients, or channels) independent of the
model's intent, so a tool stays safe even if the model calling it is manipulated or
simply wrong. See Module 13, Module 14, and Module 18.

**MCP (Model Context Protocol)** -- An open protocol for exposing tools to an LLM
client in a standardized way, independent of the framework or provider on either
side. See Module 10.

**Mock provider** -- `shared/llm/mock.py`'s `MockLLMProvider`: a scriptable fake LLM
that returns pre-programmed responses, used so every test in this repo runs offline
with no API keys.

**Multi-agent system** -- An architecture with more than one LLM-driven agent
collaborating (supervisor/worker, peer handoff, debate, etc.) rather than a single
agent with many tools. See Module 12.

**Observability / tracing** -- Instrumenting an agent's model and tool calls as
structured, nested spans (an `invoke_agent` span containing `chat`/`execute_tool`
children) so a run can be replayed and debugged after the fact. See Module 17.

**Progress file** -- A durable, external record of task-level status (pending/done,
plus each task's result) for a multi-task plan, checked and updated after every
task completes so a killed/restarted run resumes from the first incomplete task.
See Module 22. This repository's own `PROGRESS.md` is a real, working instance of
this exact pattern.

**Prompt caching** -- A provider feature that reuses a previously-processed prefix
of a prompt (e.g. a long system prompt) across calls at reduced cost/latency. See
Module 19.

**Prompt injection** -- Getting a model to treat untrusted text as if it were a
legitimate instruction. **Direct** injection comes from the user's own message;
**indirect** injection comes from content the agent reads while doing its job (see
above). See Module 18.

**ReAct** -- "Reasoning and Acting": a prompting pattern where the model
interleaves explicit reasoning text with tool calls in the same loop. See Module 04.

**Reward hacking** -- Optimization pressure finding and exploiting the gap between
a reward function's letter and its actual intent, maximizing the measured proxy
without solving the intended task. See Module 21.

**RLVR (Reinforcement Learning with Verifiable Rewards)** -- RL where a
deterministic checker (not a learned reward model) scores correctness, used
heavily for training agents on math/code/tool-use tasks. See Module 21.

**Sandbox** -- An isolated execution environment (subprocess, container, or
restricted shell) an agent's code or shell actions run inside, so a mistake or
injected instruction can't affect the host system. See `shared/sandbox/` and
Module 13.

**Structured output** -- Constraining an LLM's response to conform to a schema
(typically JSON Schema) so it can be parsed reliably by code. See Module 02.

**Tool use / function calling** -- Giving an LLM a set of callable functions
(described via schema) it can invoke mid-response instead of only producing text.
See Module 03.

**Trajectory eval** -- Evaluating not just an agent's final answer but the sequence
of tool calls and intermediate steps it took to get there. See Module 16.
