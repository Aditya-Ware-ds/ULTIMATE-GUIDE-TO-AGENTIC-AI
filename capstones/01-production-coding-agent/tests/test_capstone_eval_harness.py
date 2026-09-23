from shared.llm import get_client
from shared.llm.types import Message, Role, ToolCall

CALCULATOR_FIX = (
    "def add(a: float, b: float) -> float:\n"
    "    return a + b\n\n\n"
    "def subtract(a: float, b: float) -> float:\n"
    "    return a - b\n"
)
STRINGS_FIX = (
    "def shout(text: str) -> str:\n"
    "    return text.upper()\n\n\n"
    "def reverse(text: str) -> str:\n"
    "    return text[::-1]\n"
)
NUMBERS_FIX = (
    "def find_min(values: list[float]) -> float:\n"
    "    return min(values)\n\n\n"
    "def find_max(values: list[float]) -> float:\n"
    "    return max(values)\n"
)


def _scripted_client_factory(fix_content: str, target_file: str):
    def factory():
        client = get_client("mock")
        client.provider.add_response(
            Message(
                role=Role.ASSISTANT,
                content="Reading the source.",
                tool_calls=[
                    ToolCall(id="1", name="read_file", arguments={"relative_path": target_file})
                ],
            )
        )
        client.provider.add_response(
            Message(
                role=Role.ASSISTANT,
                content="Fixing the bug.",
                tool_calls=[
                    ToolCall(
                        id="2",
                        name="write_file",
                        arguments={"relative_path": target_file, "content": fix_content},
                    )
                ],
            )
        )
        client.provider.add_response(
            Message(
                role=Role.ASSISTANT,
                content="Verifying.",
                tool_calls=[ToolCall(id="3", name="run_tests", arguments={})],
            )
        )
        client.provider.add_text("Done.")
        return client

    return factory


async def test_run_eval_reports_a_perfect_pass_rate_across_all_sample_repos(
    coding_agent, eval_harness, sample_repo_root
):
    fixes = {
        "calculator": (CALCULATOR_FIX, "calculator.py"),
        "strings": (STRINGS_FIX, "stringutils.py"),
        "numbers": (NUMBERS_FIX, "numberutils.py"),
    }
    factories = iter(
        _scripted_client_factory(*fixes[task["repo"]])() for task in eval_harness.SAMPLE_TASKS
    )

    result = await eval_harness.run_eval(
        coding_agent.run_coding_agent, lambda: next(factories), sample_repo_root
    )

    assert result["total"] == 3
    assert result["passed"] == 3
    assert result["pass_rate"] == 1.0
    assert {r["repo"] for r in result["results"]} == {"calculator", "strings", "numbers"}


async def test_run_eval_reports_partial_pass_rate_when_a_repo_is_not_fixed(
    coding_agent, eval_harness, sample_repo_root
):
    def bad_client_factory():
        client = get_client("mock")
        client.provider.add_text("I believe this is already correct.")
        return client

    fixes = {
        "calculator": (CALCULATOR_FIX, "calculator.py"),
        "numbers": (NUMBERS_FIX, "numberutils.py"),
    }
    call_order = iter(eval_harness.SAMPLE_TASKS)

    def factory():
        task = next(call_order)
        if task["repo"] == "strings":
            return bad_client_factory()
        return _scripted_client_factory(*fixes[task["repo"]])()

    result = await eval_harness.run_eval(coding_agent.run_coding_agent, factory, sample_repo_root)

    assert result["total"] == 3
    assert result["passed"] == 2
    assert result["pass_rate"] == 2 / 3
    failed = next(r for r in result["results"] if r["repo"] == "strings")
    assert failed["status"] == "failed"
