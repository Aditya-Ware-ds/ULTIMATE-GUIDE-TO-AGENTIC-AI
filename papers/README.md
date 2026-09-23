# Papers

An annotated reading list of foundational and current agent-related papers. Every
entry here is a real, verifiable paper -- no invented citations. Each entry
includes what the paper actually showed, why it matters for building agents, and
its verified link (arXiv, ACL Anthology, or the venue's own site).

Every entry below was cited in this curriculum's own lessons and verified there
(either directly via its arXiv abstract, or as an established, real paper already
cross-referenced by multiple independent current sources) before being added here
-- see the linked module's `resources.md` for the original verification context.
Module 23 (Research literacy) covers how to read a paper like this critically.

## ReAct: Synergizing Reasoning and Acting in Language Models

**Yao et al., 2022.** [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)

Showed that interleaving explicit reasoning traces with tool-calling actions
in a single loop ("think, then act, observe, repeat") outperforms
reasoning-only or acting-only prompting on multi-hop QA and decision-making
tasks. This is the pattern this curriculum's Module 04 agent loop is named
after and built directly on.

## Lost in the Middle: How Language Models Use Long Contexts

**Liu et al., 2023.** [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)

Established the U-shaped positional-degradation effect: models are
reliably better at using information at the very start or very end of a
long context than in the middle. Directly motivates Module 05's
context-engineering discipline -- where you place information in an
agent's context is not a neutral choice.

## Reflexion: Language Agents with Verbal Reinforcement Learning

**Shinn et al., 2023.** [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)

Introduced verbal self-reflection as a substitute for gradient-based
reinforcement learning: an agent that fails a task generates a natural-
language critique of its own attempt and uses it as context for the next
try. Foundational paper behind Module 08's reflection/evaluator-optimizer
pattern.

## Improving Factuality and Reasoning in Language Models through Multiagent Debate

**Du et al., 2023.** [arXiv:2305.14325](https://arxiv.org/abs/2305.14325)

Showed that having multiple model instances debate and critique each
other's answers over several rounds improves factual accuracy and
reasoning compared to a single model's self-reflection alone. Source paper
behind Module 12's debate topology.

## AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation

**Wu et al., 2023.** [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)

A foundational multi-agent-conversation framework, structuring agent
collaboration as customizable conversable agents exchanging messages.
AutoGen's ideas were subsequently merged into Microsoft Agent Framework
(covered in Module 11) -- this paper is the conceptual origin of that
framework's conversation-centric design.

## G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment

**Liu et al., 2023.** [arXiv:2303.16634](https://arxiv.org/abs/2303.16634)

Showed that a chain-of-thought-prompted GPT-4 evaluator, using a
form-filling paradigm, aligns with human judgment substantially better
than prior automatic metrics (BLEU, ROUGE) for open-ended generation
quality. Foundational paper behind Module 16's LLM-as-judge pattern.

## Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

**Zheng et al., 2023.** [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)

Documented the specific, reproducible biases LLM judges exhibit --
position bias, verbosity bias, and self-enhancement bias -- and proposed
mitigations for each. Directly cited in Module 16 lesson 02 as the source
for the three judge-bias mitigations this curriculum teaches.

## DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models

**Shao et al., 2024.** [arXiv:2402.03300](https://arxiv.org/abs/2402.03300)

Introduced GRPO (Group Relative Policy Optimization), a memory-efficient
PPO variant that computes a policy advantage from a group of sampled
completions' rewards without training a separate critic/value network.
This curriculum's Module 21 lab implements and tests GRPO's exact
advantage formula; Module 23 uses this same paper as its worked example
for reading a paper critically, including being explicit about which of
its claims were and weren't independently verified.
