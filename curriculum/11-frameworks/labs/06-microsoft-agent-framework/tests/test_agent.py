import pytest

pytest.importorskip("agent_framework")

import agent_framework as af  # noqa: E402
from agent_framework._tools import FunctionInvocationLayer  # noqa: E402


class ScriptedChatClient(FunctionInvocationLayer, af.BaseChatClient):
    call_count: int = 0

    async def _inner_get_response(self, *, messages, stream=False, options=None, **kwargs):
        self.call_count += 1
        if self.call_count == 1:
            content = af.Content.from_function_call(
                "call_1", "calculate", arguments={"expression": "15 * 7 + 3"}
            )
        else:
            content = af.Content.from_text("The answer is 108.")
        return af.ChatResponse(messages=af.Message(role="assistant", contents=[content]))

    async def _inner_get_streaming_response(self, *args, **kwargs):
        raise NotImplementedError


def test_calculate_basic_arithmetic(agent_module):
    assert agent_module.calculate("2 + 2") == 4
    assert agent_module.calculate("15 * 7 + 3") == 108


def test_calculate_rejects_non_arithmetic(agent_module):
    with pytest.raises(ValueError):
        agent_module.calculate("__import__('os')")


async def test_run_agent_with_scripted_tool_call(agent_module):
    client = ScriptedChatClient()

    result = await agent_module.run_agent("What is 15 times 7, plus 3?", client=client)

    assert result == "The answer is 108."
    assert client.call_count == 2
