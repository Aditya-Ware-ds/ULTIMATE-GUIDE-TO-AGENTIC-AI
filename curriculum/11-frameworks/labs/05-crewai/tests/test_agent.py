import pytest

pytest.importorskip("crewai")

from crewai.llms.base_llm import BaseLLM  # noqa: E402


class ScriptedLLM(BaseLLM):
    def __init__(self):
        super().__init__(model="scripted")
        self.call_count = 0

    def call(
        self,
        messages,
        tools=None,
        callbacks=None,
        available_functions=None,
        from_task=None,
        from_agent=None,
        response_model=None,
    ):
        self.call_count += 1
        if available_functions and "calculate" in available_functions:
            result = available_functions["calculate"](expression="15 * 7 + 3")
            return f"The answer is {result}."
        return "The answer is 108."

    def supports_function_calling(self):
        return True


def test_calculate_basic_arithmetic(agent_module):
    assert agent_module.calculate.func("2 + 2") == 4
    assert agent_module.calculate.func("15 * 7 + 3") == 108


def test_calculate_rejects_non_arithmetic(agent_module):
    with pytest.raises(ValueError):
        agent_module.calculate.func("__import__('os')")


def test_run_agent_with_scripted_tool_call(agent_module):
    llm = ScriptedLLM()

    result = agent_module.run_agent("What is 15 times 7, plus 3?", llm=llm)

    assert "108" in result
    assert llm.call_count >= 1
