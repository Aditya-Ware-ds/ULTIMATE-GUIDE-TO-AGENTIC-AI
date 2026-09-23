# Cheatsheet: evaluation metrics and methods

From Module 16 (Evaluation). Use the cheapest method that actually answers
the question -- prefer a mechanical check over an LLM judge whenever one
exists.

| Method | What it measures | Cost/reliability | Use when |
|---|---|---|---|
| **Exact/mechanical check** | Does the output match a deterministic ground truth (a number, a passing test suite, valid JSON)? | Cheapest, most reliable | A ground-truth check exists at all (Module 13's "run the tests" principle). |
| **Golden-dataset accuracy** | Fraction of a representative, curated dataset the agent gets right. | Cheap per-item, needs upkeep | You need a single trusted number to track over time / across changes. |
| **LLM-as-judge** | A model call grades a free-form answer against a reference or rubric. | More expensive, has known biases | No mechanical check exists and correctness is genuinely open-ended. |
| **Trajectory eval** | Did the agent use the right tools, in a sensible order, without redundant/contradictory calls? | Needs instrumentation (traces) | Two agents can reach the same answer via very different (and differently risky) paths. |
| **Public benchmark** (SWE-bench, GAIA, tau-bench, BrowseComp, WebArena, OSWorld, Terminal-Bench) | Standardized comparison against the broader field. | Free to run others' numbers, expensive to run yourself | Comparing against the field, not validating your specific task. |

## LLM-as-judge biases (mitigate each explicitly)

- **Position bias** -- favors whichever candidate is shown first/second. Mitigate: swap order, run twice, trust only an agreeing verdict.
- **Verbosity bias** -- favors longer answers regardless of quality. Mitigate: score conciseness as its own explicit criterion.
- **Self-preference bias** -- a model rates its own outputs more favorably. Mitigate: use a different model (or fully independent call) as judge.

## The regression-suite discipline

Run the golden dataset + trajectory checks automatically on every change
(the same idea as `make test`, applied to agent *behavior*). Add a new
example to the dataset every time a real failure mode is found, so it can
never silently regress again.

See: `curriculum/16-evaluation/README.md`.
