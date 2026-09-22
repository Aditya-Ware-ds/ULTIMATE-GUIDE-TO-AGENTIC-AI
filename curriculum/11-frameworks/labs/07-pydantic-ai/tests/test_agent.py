import pytest

pytest.importorskip("pydantic_ai")

from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart, ToolCallPart  # noqa: E402
from pydantic_ai.models.function import AgentInfo, FunctionModel  # noqa: E402


def test_calculate_basic_arithmetic(agent_module):
    assert agent_module.calculate("2 + 2") == 4
    assert agent_module.calculate("15 * 7 + 3") == 108


def test_calculate_rejects_non_arithmetic(agent_module):
    with pytest.raises(ValueError):
        agent_module.calculate("__import__('os')")


def test_run_agent_with_scripted_tool_call(agent_module):
    call_count = {"n": 0}

    def scripted(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        call_count["n"] += 1
        if call_count["n"] == 1:
            return ModelResponse(
                parts=[ToolCallPart(tool_name="calculate", args={"expression": "15 * 7 + 3"})]
            )
        return ModelResponse(parts=[TextPart(content="The answer is 108.")])

    result = agent_module.run_agent("What is 15 times 7, plus 3?", model=FunctionModel(scripted))

    assert result == "The answer is 108."
    assert call_count["n"] == 2
