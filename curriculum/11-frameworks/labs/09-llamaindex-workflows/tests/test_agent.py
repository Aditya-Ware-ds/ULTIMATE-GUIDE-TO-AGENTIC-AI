import pytest

pytest.importorskip("llama_index.core")

from llama_index.core.base.llms.types import (  # noqa: E402
    ChatMessage,
    MessageRole,
    TextBlock,
    ToolCallBlock,
)
from llama_index.core.llms import MockFunctionCallingLLM  # noqa: E402


def make_scripted_llm():
    call_count = {"n": 0}

    def response_generator(*args, **kwargs):
        call_count["n"] += 1
        if call_count["n"] == 1:
            return ChatMessage(
                role=MessageRole.ASSISTANT,
                blocks=[
                    ToolCallBlock(
                        tool_call_id="1",
                        tool_name="calculate",
                        tool_kwargs={"expression": "15 * 7 + 3"},
                    )
                ],
            )
        return ChatMessage(
            role=MessageRole.ASSISTANT, blocks=[TextBlock(text="The answer is 108.")]
        )

    llm = MockFunctionCallingLLM(is_chat_model=True, response_generator=response_generator)
    return llm, call_count


def test_calculate_basic_arithmetic(agent_module):
    assert agent_module.calculate("2 + 2") == 4
    assert agent_module.calculate("15 * 7 + 3") == 108


def test_calculate_rejects_non_arithmetic(agent_module):
    with pytest.raises(ValueError):
        agent_module.calculate("__import__('os')")


async def test_run_agent_with_scripted_tool_call(agent_module):
    llm, call_count = make_scripted_llm()

    result = await agent_module.run_agent("What is 15 times 7, plus 3?", llm=llm)

    assert result == "The answer is 108."
    assert call_count["n"] == 2
