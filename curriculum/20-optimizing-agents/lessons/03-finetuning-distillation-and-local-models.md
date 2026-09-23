# Fine-tuning, distillation, and local models

**Last verified:** 2026-09-22
**Difficulty:** ★★★★☆ · **Time:** ~40 minutes

## Learning objectives

- Distinguish prompt optimization (lesson 02), fine-tuning, and distillation as three different levers with different costs and payoffs.
- Explain what distillation actually trains a smaller model to do, and why that's different from just using a smaller model directly.
- Decide when an open-weight/local model (Module 01's `OllamaProvider`) is the right choice instead of a hosted API.

## Intuition

Lesson 02 optimized *what gets sent to* a fixed model (few-shot
demonstrations, selected prompt content). Fine-tuning and distillation
instead change *the model itself* -- its weights -- which is a heavier,
more expensive lever than prompt optimization, and one that pays off under
different conditions.

## The concept

### Fine-tuning for tool use

Fine-tuning adjusts a model's weights on a dataset of examples specific to
your task -- for an agent, that dataset is typically real (or
realistic) tool-calling traces: the exact tool-call sequences and arguments
you want the model to produce for given inputs. This can improve
reliability and reduce prompt length (less needs to be re-explained in
context every call) for a narrow, well-defined, high-volume task, but
requires real training infrastructure and a genuinely sizable, high-quality
dataset -- it's a heavier commitment than lesson 02's few-shot optimization,
appropriate once prompt-level optimization has been tried and a specific,
recurring failure pattern remains.

### Distillation

Distillation trains a smaller, cheaper model to imitate a larger, more
capable one's outputs on your specific task -- not to be generally as good
as the larger model, but to match it closely enough *on the distribution of
inputs your task actually produces*. This is different from simply
switching to a smaller model directly (Module 19's model-routing lesson):
routing sends easy requests to an off-the-shelf small model that may or may
not handle them well; distillation trains a small model specifically to
handle *your* requests well, using the larger model's outputs as the
training signal.

```python
# Conceptual shape, not a runnable pipeline:
# 1. Run the large, expensive model on a representative sample of real inputs.
# 2. Collect (input, large_model_output) pairs as a training set.
# 3. Fine-tune a smaller model on that training set to imitate the outputs.
# 4. Evaluate the distilled model with Module 16's eval harness before
#    trusting it in production -- distillation quality is an empirical
#    question, not a given.
```

### Open-weight and local models

`shared/llm/`'s `OllamaProvider` (Module 01 onward) is this curriculum's
open-weight/local option -- running a model on your own infrastructure
instead of calling a hosted API. The tradeoff is real: local models trade
some raw capability for cost control, data privacy (nothing leaves your
infrastructure), and the ability to fine-tune or distill into a model you
fully control the weights of, which most hosted APIs don't expose directly.
For a task where a smaller open-weight model (Module 01's tool-calling-
capable model classes) already clears your accuracy bar via Module 16's
eval harness, it's frequently the cheapest available option by a wide
margin.

## Deeper: these three levers compose, in a natural order

A sensible optimization sequence, cheapest and least risky first: (1)
prompt/few-shot optimization (lesson 02) using the model you already have,
(2) model routing (Module 19) to send easy traffic to a cheaper off-the-
shelf model, (3) distillation once you have a large enough volume of real
traffic to make training a task-specific smaller model worthwhile, (4)
fine-tuning for a narrow, high-volume, well-understood failure pattern that
survives all of the above. Skipping straight to fine-tuning without trying
the cheaper levers first is a common, avoidable waste of effort and cost.

## When not to use this

Don't fine-tune or distill for a low-volume task, or one whose requirements
are still actively changing -- both require real upfront investment
(data collection, training infrastructure, evaluation) that only pays off
against enough volume and stability to amortize it. Lesson 02's prompt
optimization is cheaper to iterate on and better suited to a task still in
flux.

## Common mistakes

- Reaching for fine-tuning before trying prompt optimization (lesson 02)
  and model routing (Module 19), both of which are cheaper, faster to
  iterate on, and often sufficient on their own.
- Distilling into a smaller model without evaluating it against Module 16's
  eval harness before deployment -- distillation quality is empirical, not
  guaranteed by the process itself.
- Assuming a local/open-weight model is "worse" across the board rather
  than checking its actual eval score on your specific task -- for many
  narrower tasks, a well-chosen small open-weight model clears the bar
  fine, at a fraction of the cost.

## Key takeaways

- Fine-tuning and distillation change model weights, a heavier lever than lesson 02's prompt optimization -- appropriate once cheaper levers have been tried and a specific pattern remains.
- Distillation trains a smaller model specifically to imitate a larger one's outputs on your task's actual input distribution, which differs from simply routing to an off-the-shelf small model.
- Try optimization levers roughly cheapest-first: prompt optimization, then routing, then distillation, then fine-tuning -- validated at each step with Module 16's eval harness.

## Lab

[`labs/01-dspy-prompt-optimization/`](../labs/01-dspy-prompt-optimization/README.md)
