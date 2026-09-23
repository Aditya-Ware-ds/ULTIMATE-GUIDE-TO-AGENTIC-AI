"""Lab 20.01: optimize a DSPy program with a real optimizer against a
scripted, offline LM. Reference solution. See ../README.md.
"""

from __future__ import annotations

import types

import dspy


class ScriptedLM(dspy.BaseLM):
    """A deterministic, fully offline LM: answers from `knowledge_base` by
    matching the question's text inside the messages DSPy sends. Verified
    against dspy 3.3.1's dspy.BaseLM legacy contract.
    """

    forward_contract = "legacy"

    def __init__(self, knowledge_base: dict[str, str]) -> None:
        super().__init__(model="scripted-test-model", num_retries=0)
        self._knowledge_base = knowledge_base
        self.calls: list = []

    def forward(self, prompt=None, messages=None, **kwargs):
        self.calls.append(messages or prompt)
        text = " ".join(m.get("content", "") for m in (messages or []) if isinstance(m, dict))
        answer = next((a for q, a in self._knowledge_base.items() if q in text), "unknown")
        message = types.SimpleNamespace(content=f'{{"answer": "{answer}"}}')
        choice = types.SimpleNamespace(message=message, finish_reason="stop")
        usage = {"prompt_tokens": 5, "completion_tokens": 5, "total_tokens": 10}
        return types.SimpleNamespace(choices=[choice], usage=usage, model=self.model)


def configure_scripted_lm(knowledge_base: dict[str, str]) -> ScriptedLM:
    lm = ScriptedLM(knowledge_base)
    dspy.configure(lm=lm, adapter=dspy.JSONAdapter())
    return lm


def build_program() -> dspy.Predict:
    return dspy.Predict("question -> answer")


def exact_match_metric(example, prediction, trace=None) -> bool:
    return example.answer.lower() == prediction.answer.lower()


def build_trainset(knowledge_base: dict[str, str]) -> list[dspy.Example]:
    return [
        dspy.Example(question=question, answer=answer).with_inputs("question")
        for question, answer in knowledge_base.items()
    ]


def optimize_program(program: dspy.Predict, trainset: list[dspy.Example]) -> dspy.Predict:
    optimizer = dspy.BootstrapFewShot(
        metric=exact_match_metric, max_bootstrapped_demos=2, max_labeled_demos=2
    )
    return optimizer.compile(program, trainset=trainset)
