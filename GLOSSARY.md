# Glossary

Terms as used consistently throughout this repo. If a lesson uses a term
differently from this list, the lesson is wrong -- file an issue. This glossary
grows as modules are built; see `PROGRESS.md` for what's covered so far.

**Agent** -- A system where an LLM decides its own sequence of actions (which tools
to call, in what order, when to stop) to accomplish a goal, as opposed to a fixed
pipeline. See Module 04.

**Agent loop** -- The observe → think → act cycle an agent runs repeatedly until it
decides it's done or hits a stopping condition. See Module 04.

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

**Evaluator-optimizer** -- A pattern where one LLM call produces an output and a
second evaluates/critiques it, looping until the evaluator is satisfied or a budget
is exhausted. See Module 08.

**LLM-as-judge** -- Using an LLM call to score or compare outputs for evaluation
purposes, instead of (or alongside) exact-match or human grading. Carries known
biases (e.g. preferring longer or more confident-sounding answers) covered in
Module 16.

**Mock provider** -- `shared/llm/mock.py`'s `MockLLMProvider`: a scriptable fake LLM
that returns pre-programmed responses, used so every test in this repo runs offline
with no API keys.

**Multi-agent system** -- An architecture with more than one LLM-driven agent
collaborating (supervisor/worker, peer handoff, debate, etc.) rather than a single
agent with many tools. See Module 12.

**Prompt caching** -- A provider feature that reuses a previously-processed prefix
of a prompt (e.g. a long system prompt) across calls at reduced cost/latency. See
Module 19.

**ReAct** -- "Reasoning and Acting": a prompting pattern where the model
interleaves explicit reasoning text with tool calls in the same loop. See Module 04.

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
