from shared.llm.types import Message, Role, ToolCall

CORRECT_CODE = """
import csv

total = 0
with open("sales.csv") as f:
    for row in csv.DictReader(f):
        if row["product"] == "Widget A":
            total += int(row["revenue"])
print(total)
"""

BUGGY_CODE = "print(this_name_does_not_exist)"


def test_run_analysis_executes_real_code_against_the_dataset(data_agent, dataset_dir):
    output = data_agent.run_analysis(CORRECT_CODE, dataset_dir)

    assert output.strip() == "400"


def test_run_analysis_surfaces_python_errors_instead_of_raising(data_agent, dataset_dir):
    output = data_agent.run_analysis(BUGGY_CODE, dataset_dir)

    assert output.startswith("Error running code:")
    assert "NameError" in output


def test_dispatch_never_raises_on_unknown_tool(data_agent, dataset_dir):
    registry = data_agent.build_tool_registry(dataset_dir)
    call = ToolCall(id="1", name="not_a_tool", arguments={})

    result = data_agent.dispatch(call, registry)

    assert result.is_error


async def test_run_data_analysis_agent_self_corrects_after_an_error(
    data_agent, client, dataset_dir
):
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="Let me compute the total.",
            tool_calls=[ToolCall(id="1", name="run_analysis", arguments={"code": BUGGY_CODE})],
        )
    )
    client.provider.add_response(
        Message(
            role=Role.ASSISTANT,
            content="That failed -- let me fix it.",
            tool_calls=[ToolCall(id="2", name="run_analysis", arguments={"code": CORRECT_CODE})],
        )
    )
    client.provider.add_text("Widget A's total revenue is $400.")

    result = await data_agent.run_data_analysis_agent(
        client, dataset_dir, "What is the total revenue for Widget A?"
    )

    assert result == "Widget A's total revenue is $400."
    assert client.provider.call_count == 3


async def test_run_data_analysis_agent_stops_at_max_steps(data_agent, client, dataset_dir):
    for _ in range(10):
        client.provider.add_response(
            Message(
                role=Role.ASSISTANT,
                content="Still working on it.",
                tool_calls=[ToolCall(id="x", name="run_analysis", arguments={"code": BUGGY_CODE})],
            )
        )

    result = await data_agent.run_data_analysis_agent(
        client, dataset_dir, "What is the total revenue for Widget A?", max_steps=3
    )

    assert client.provider.call_count == 3
    assert "3" in result or "stopped" in result.lower()
