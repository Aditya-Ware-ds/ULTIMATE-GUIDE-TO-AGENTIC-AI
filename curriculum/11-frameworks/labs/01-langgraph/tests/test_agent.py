import pytest

pytest.importorskip("langgraph")
pytest.importorskip("langchain")

from langchain_core.language_models.chat_models import BaseChatModel  # noqa: E402
from langchain_core.messages import AIMessage  # noqa: E402
from langchain_core.outputs import ChatGeneration, ChatResult  # noqa: E402


class ScriptedChatModel(BaseChatModel):
    call_count: int = 0

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        self.call_count += 1
        if self.call_count == 1:
            message = AIMessage(
                content="",
                tool_calls=[
                    {"name": "calculate", "args": {"expression": "15 * 7 + 3"}, "id": "call_1"}
                ],
            )
        else:
            message = AIMessage(content="The answer is 108.")
        return ChatResult(generations=[ChatGeneration(message=message)])

    def bind_tools(self, tools, **kwargs):
        return self

    @property
    def _llm_type(self) -> str:
        return "scripted"


def test_calculate_basic_arithmetic(agent_module):
    assert agent_module.calculate.invoke({"expression": "2 + 2"}) == 4
    assert agent_module.calculate.invoke({"expression": "15 * 7 + 3"}) == 108


def test_calculate_rejects_non_arithmetic(agent_module):
    with pytest.raises(ValueError):
        agent_module.calculate.invoke({"expression": "__import__('os')"})


def test_run_agent_with_scripted_tool_call(agent_module):
    model = ScriptedChatModel()

    result = agent_module.run_agent("What is 15 times 7, plus 3?", model=model)

    assert result == "The answer is 108."
    assert model.call_count == 2
