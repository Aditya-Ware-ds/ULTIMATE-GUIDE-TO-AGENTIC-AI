import pytest

pytest.importorskip("agents")

from agents.items import (  # noqa: E402
    ModelResponse,
    ResponseFunctionToolCall,
    ResponseOutputMessage,
    ResponseOutputText,
)
from agents.models.interface import Model  # noqa: E402
from agents.usage import Usage  # noqa: E402


class ScriptedModel(Model):
    def __init__(self):
        self.call_count = 0

    async def get_response(
        self,
        system_instructions,
        input,
        model_settings,
        tools,
        output_schema,
        handoffs,
        tracing,
        *,
        previous_response_id,
        conversation_id,
        prompt,
    ):
        self.call_count += 1
        if self.call_count == 1:
            output = [
                ResponseFunctionToolCall(
                    call_id="call_1",
                    name="calculate",
                    arguments='{"expression": "15 * 7 + 3"}',
                    type="function_call",
                )
            ]
        else:
            output = [
                ResponseOutputMessage(
                    id="msg_1",
                    role="assistant",
                    status="completed",
                    type="message",
                    content=[
                        ResponseOutputText(
                            text="The answer is 108.", type="output_text", annotations=[]
                        )
                    ],
                )
            ]
        return ModelResponse(output=output, usage=Usage(), response_id="resp_1")

    async def stream_response(self, *args, **kwargs):
        raise NotImplementedError


def test_evaluate_basic_arithmetic(agent_module):
    assert agent_module._evaluate("2 + 2") == 4
    assert agent_module._evaluate("15 * 7 + 3") == 108


def test_evaluate_rejects_non_arithmetic(agent_module):
    with pytest.raises(ValueError):
        agent_module._evaluate("__import__('os')")


def test_calculate_tool_is_registered(agent_module):
    assert agent_module.calculate.name == "calculate"


async def test_run_agent_with_scripted_tool_call(agent_module):
    model = ScriptedModel()

    result = await agent_module.run_agent("What is 15 times 7, plus 3?", model=model)

    assert result == "The answer is 108."
    assert model.call_count == 2
