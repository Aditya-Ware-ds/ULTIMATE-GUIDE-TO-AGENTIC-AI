"""Lab 20.01: optimize a DSPy program with a real optimizer against a
scripted, offline LM. See ../README.md for the full spec.

Fill in the pieces below. Run the tests against your work with:
    LAB_TARGET=starter uv run --with dspy pytest \
        curriculum/20-optimizing-agents/labs/01-dspy-prompt-optimization/tests
"""

from __future__ import annotations

import types  # noqa: F401 -- used once you implement ScriptedLM.forward below

import dspy


class ScriptedLM(dspy.BaseLM):
    """A deterministic, fully offline LM: answers from `knowledge_base` by
    matching the question's text inside the messages DSPy sends.
    """

    forward_contract = "legacy"

    def __init__(self, knowledge_base: dict[str, str]) -> None:
        super().__init__(model="scripted-test-model", num_retries=0)
        self._knowledge_base = knowledge_base
        self.calls: list = []

    def forward(self, prompt=None, messages=None, **kwargs):
        """Record `messages or prompt` in self.calls. Find which question
        (a key of self._knowledge_base) appears in the joined content of
        `messages`, and build a response object DSPy's legacy contract
        expects: an object with `.choices[0].message.content` set to
        `'{"answer": "<the matched answer, or "unknown">"}'`, plus `.usage`
        (a dict) and `.model`.

        TODO: implement this.
        """
        raise NotImplementedError


def configure_scripted_lm(knowledge_base: dict[str, str]) -> ScriptedLM:
    """Create a ScriptedLM and call dspy.configure(lm=lm, adapter=dspy.JSONAdapter())
    (JSONAdapter avoids ChatAdapter's parse-failure fallback -- see
    lessons/01-dspy-signatures-and-modules.md). Return the LM.

    TODO: implement this.
    """
    raise NotImplementedError


def build_program() -> dspy.Predict:
    """Return dspy.Predict("question -> answer").

    TODO: implement this.
    """
    raise NotImplementedError


def exact_match_metric(example, prediction, trace=None) -> bool:
    """Return True if example.answer matches prediction.answer
    case-insensitively.

    TODO: implement this.
    """
    raise NotImplementedError


def build_trainset(knowledge_base: dict[str, str]) -> list[dspy.Example]:
    """Return one dspy.Example(question=..., answer=...).with_inputs("question")
    per entry in knowledge_base.

    TODO: implement this.
    """
    raise NotImplementedError


def optimize_program(program: dspy.Predict, trainset: list[dspy.Example]) -> dspy.Predict:
    """Compile `program` with dspy.BootstrapFewShot(metric=exact_match_metric,
    max_bootstrapped_demos=2, max_labeled_demos=2) against `trainset`, and
    return the optimized program.

    TODO: implement this.
    """
    raise NotImplementedError
