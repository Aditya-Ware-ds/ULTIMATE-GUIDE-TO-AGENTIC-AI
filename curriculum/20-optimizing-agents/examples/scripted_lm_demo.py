"""Run: uv run --with dspy python curriculum/20-optimizing-agents/examples/scripted_lm_demo.py

Shows a DSPy Signature answering a question via a fully scripted, offline
LM -- no API key, no network. See lessons/01-dspy-signatures-and-modules.md.

Requires `dspy` (not a default dependency of this repo -- see this
module's README for why).
"""

from __future__ import annotations

import types

import dspy


class ScriptedLM(dspy.BaseLM):
    """A minimal, fully offline stand-in for a real LM -- the same idea as
    shared/llm/mock.py's MockLLMProvider, applied to DSPy's own LM
    abstraction (verified against dspy 3.3.1's dspy.BaseLM docstring).
    """

    forward_contract = "legacy"

    def __init__(self, script: list[str]) -> None:
        super().__init__(model="scripted-demo-model", num_retries=0)
        self._script = list(script)
        self.calls: list = []

    def forward(self, prompt=None, messages=None, **kwargs):
        self.calls.append(messages or prompt)
        text = self._script.pop(0)
        message = types.SimpleNamespace(content=text)
        choice = types.SimpleNamespace(message=message, finish_reason="stop")
        usage = {"prompt_tokens": 5, "completion_tokens": 5, "total_tokens": 10}
        return types.SimpleNamespace(choices=[choice], usage=usage, model=self.model)


def main() -> None:
    lm = ScriptedLM(['{"answer": "Paris"}'])
    dspy.configure(lm=lm, adapter=dspy.JSONAdapter())

    predictor = dspy.Predict("question -> answer")
    result = predictor(question="What is the capital of France?")

    print(f"Answer: {result.answer}")
    print(f"Real model calls made: {len(lm.calls)}")


if __name__ == "__main__":
    main()
