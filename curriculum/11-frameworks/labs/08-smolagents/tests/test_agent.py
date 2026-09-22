import pytest

pytest.importorskip("smolagents")

from smolagents.models import (  # noqa: E402
    ChatMessage,
    ChatMessageToolCall,
    ChatMessageToolCallFunction,
    MessageRole,
    Model,
)


class ScriptedModel(Model):
    def __init__(self):
        super().__init__()
        self.call_count = 0

    def generate(
        self, messages, stop_sequences=None, response_format=None, tools_to_call_from=None, **kwargs
    ):
        self.call_count += 1
        if self.call_count == 1:
            return ChatMessage(
                role=MessageRole.ASSISTANT,
                content="",
                tool_calls=[
                    ChatMessageToolCall(
                        id="call_1",
                        type="function",
                        function=ChatMessageToolCallFunction(
                            name="calculate", arguments={"expression": "15 * 7 + 3"}
                        ),
                    )
                ],
            )
        return ChatMessage(
            role=MessageRole.ASSISTANT,
            content="",
            tool_calls=[
                ChatMessageToolCall(
                    id="call_2",
                    type="function",
                    function=ChatMessageToolCallFunction(
                        name="final_answer", arguments={"answer": "The answer is 108."}
                    ),
                )
            ],
        )


def test_calculate_basic_arithmetic(agent_module):
    assert agent_module.calculate("2 + 2") == 4
    assert agent_module.calculate("15 * 7 + 3") == 108


def test_calculate_rejects_non_arithmetic(agent_module):
    with pytest.raises(ValueError):
        agent_module.calculate("__import__('os')")


def test_run_agent_with_scripted_tool_call(agent_module):
    model = ScriptedModel()

    result = agent_module.run_agent("What is 15 times 7, plus 3?", model=model)

    assert result == "The answer is 108."
    assert model.call_count == 2
