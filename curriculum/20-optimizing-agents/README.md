# Module 20 -- Optimizing agents

**Difficulty:** ★★★★★ · **Time estimate:** 6-8 hours

## Objectives

By the end of this module you can:

- Express a task as a DSPy `Signature` and run it with `dspy.Predict`, instead of hand-writing a prompt string.
- Optimize a DSPy program against a metric and a small training set, using a real optimizer (`BootstrapFewShot`).
- Explain fine-tuning for tool use, distillation, and open-weight/local models as complementary optimization levers, and when each applies.

## Prerequisites

[Module 19 -- Deployment & scale](../19-deployment-and-scale/README.md)

## Why this module exists

Level 6 opens by asking a different question than every earlier module:
not "how do I build this agent pattern," but "how do I make an existing
one better, automatically, using data instead of manual trial and error."
Module 16's eval harness is the direct prerequisite this module builds on
-- DSPy's optimizers need exactly the kind of metric function that module
taught you to write, and this module is where that metric earns its keep
by actually driving an optimization process, not just reporting a score.

**A note on dependencies**: `dspy` is not part of this repo's default
dependencies (same reasoning as Module 11's 9 frameworks -- see this
module's lab README for why). Use `uv run --with dspy` to run its examples
and tests; `make test` skips this module's DSPy-dependent tests
automatically via `pytest.importorskip("dspy")` when it isn't installed.

## Contents

- [`lessons/01-dspy-signatures-and-modules.md`](lessons/01-dspy-signatures-and-modules.md)
- [`lessons/02-optimizing-with-a-metric.md`](lessons/02-optimizing-with-a-metric.md)
- [`lessons/03-finetuning-distillation-and-local-models.md`](lessons/03-finetuning-distillation-and-local-models.md)
- [`examples/`](examples/) -- small runnable demos (no API key needed, requires `dspy`)
- [`labs/01-dspy-prompt-optimization/`](labs/01-dspy-prompt-optimization/) -- optimize a DSPy program with a real optimizer against a scripted, offline LM
- [`quiz.md`](quiz.md)
- [`pitfalls.md`](pitfalls.md)
- [`resources.md`](resources.md)

## Next

[Module 21 -- RL and training for agents](../21-rl-and-training-for-agents/README.md)
