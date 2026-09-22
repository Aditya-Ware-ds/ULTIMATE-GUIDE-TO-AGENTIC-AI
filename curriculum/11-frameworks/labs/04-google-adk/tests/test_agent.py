import pytest

pytest.importorskip("google.adk")

from google.adk.models import BaseLlm, LlmResponse  # noqa: E402
from google.genai import types  # noqa: E402


class ScriptedLlm(BaseLlm):
    model: str = "scripted"
    call_count: int = 0

    async def generate_content_async(self, llm_request, stream=False):
        self.call_count += 1
        if self.call_count == 1:
            part = types.Part(
                function_call=types.FunctionCall(
                    name="calculate", args={"expression": "15 * 7 + 3"}
                )
            )
        else:
            part = types.Part(text="The answer is 108.")
        yield LlmResponse(content=types.Content(role="model", parts=[part]))


def test_calculate_basic_arithmetic(agent_module):
    assert agent_module.calculate("2 + 2") == 4
    assert agent_module.calculate("15 * 7 + 3") == 108


def test_calculate_rejects_non_arithmetic(agent_module):
    with pytest.raises(ValueError):
        agent_module.calculate("__import__('os')")


async def test_run_agent_with_scripted_tool_call(agent_module):
    model = ScriptedLlm()

    result = await agent_module.run_agent("What is 15 times 7, plus 3?", model=model)

    assert result == "The answer is 108."
    assert model.call_count == 2
