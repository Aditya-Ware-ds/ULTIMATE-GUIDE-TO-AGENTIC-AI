"""Project 02: customer-support agent with escalation -- reference solution.
See ../README.md.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path

from shared.llm import LLMClient, Message, Role
from shared.llm.types import ToolCall, ToolDefinition, ToolResult

FAQ: dict[str, str] = {
    "shipping": "Standard shipping takes 3-5 business days; international orders take 2-3 weeks.",
    "returns": "Items may be returned within 30 days of purchase with a valid receipt.",
    "account": "Reset your password from the login page's 'Forgot password' link.",
}


def search_faq(query: str) -> str:
    query_words = set(query.lower().split())
    best_score = 0
    best_entry = None
    for entry in FAQ.values():
        entry_words = set(entry.lower().split())
        score = len(query_words & entry_words)
        if score > best_score:
            best_score = score
            best_entry = entry
    if best_entry is None:
        raise ValueError(f"No FAQ entry found for: {query!r}")
    return best_entry


_ISSUED_REFUNDS: list[dict] = []


def issue_refund(order_id: str, amount: float) -> str:
    _ISSUED_REFUNDS.append({"order_id": order_id, "amount": amount})
    return f"Refund of ${amount:.2f} issued for order {order_id}"


SEARCH_FAQ_TOOL = ToolDefinition(
    name="search_faq",
    description="Search the FAQ knowledge base for an answer to a support question.",
    parameters={
        "type": "object",
        "properties": {"query": {"type": "string"}},
        "required": ["query"],
    },
)

ISSUE_REFUND_TOOL = ToolDefinition(
    name="issue_refund",
    description="Issue a refund for an order. Requires human approval.",
    parameters={
        "type": "object",
        "properties": {
            "order_id": {"type": "string"},
            "amount": {"type": "number"},
        },
        "required": ["order_id", "amount"],
    },
)

TOOL_REGISTRY: dict[str, Callable] = {"search_faq": search_faq, "issue_refund": issue_refund}
REQUIRES_APPROVAL: set[str] = {"issue_refund"}


def dispatch(tool_call: ToolCall, registry: dict[str, Callable]) -> ToolResult:
    if tool_call.name not in registry:
        return ToolResult(
            tool_call_id=tool_call.id,
            content=f"Unknown tool: {tool_call.name}",
            is_error=True,
        )
    function = registry[tool_call.name]
    try:
        result = function(**tool_call.arguments)
        return ToolResult(tool_call_id=tool_call.id, content=str(result))
    except Exception as exc:
        return ToolResult(
            tool_call_id=tool_call.id, content=f"Tool execution failed: {exc}", is_error=True
        )


def message_to_dict(message: Message) -> dict:
    return {
        "role": message.role.value,
        "content": message.content,
        "tool_calls": [asdict(tc) for tc in message.tool_calls],
        "tool_result": asdict(message.tool_result) if message.tool_result else None,
    }


def message_from_dict(data: dict) -> Message:
    return Message(
        role=Role(data["role"]),
        content=data["content"],
        tool_calls=[ToolCall(**tc) for tc in data["tool_calls"]],
        tool_result=ToolResult(**data["tool_result"]) if data["tool_result"] else None,
    )


def save_checkpoint(
    path: Path,
    messages: list[Message],
    step: int,
    pending_tool_call: ToolCall | None = None,
) -> None:
    data = {
        "step": step,
        "messages": [message_to_dict(m) for m in messages],
        "pending_tool_call": asdict(pending_tool_call) if pending_tool_call else None,
    }
    path.write_text(json.dumps(data))


def load_checkpoint(path: Path) -> tuple[list[Message], int, ToolCall | None] | None:
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    messages = [message_from_dict(m) for m in data["messages"]]
    pending_tool_call = ToolCall(**data["pending_tool_call"]) if data["pending_tool_call"] else None
    return messages, data["step"], pending_tool_call


def build_escalation_summary(messages: list[Message], reason: str) -> str:
    steps = []
    for message in messages:
        for tool_call in message.tool_calls:
            steps.append(f"Called {tool_call.name}({tool_call.arguments})")
        if message.tool_result is not None:
            status = "ERROR" if message.tool_result.is_error else "OK"
            steps.append(f"  -> [{status}] {message.tool_result.content}")
    steps_text = "\n".join(f"  {i + 1}. {step}" for i, step in enumerate(steps))
    return f"Escalating to a human. Reason: {reason}\nSteps already attempted:\n{steps_text}"


@dataclass
class AgentResult:
    status: str
    text: str | None = None
    pending_tool_call: ToolCall | None = None


_TOOLS = [SEARCH_FAQ_TOOL, ISSUE_REFUND_TOOL]


async def _continue_loop(
    client: LLMClient,
    checkpoint_path: Path,
    messages: list[Message],
    step: int,
    max_steps: int,
) -> AgentResult:
    while step < max_steps:
        response = await client.complete(messages, tools=_TOOLS)
        if not response.message.tool_calls:
            if checkpoint_path.exists():
                checkpoint_path.unlink()
            return AgentResult(status="done", text=response.message.content or "")

        tool_call = response.message.tool_calls[0]
        messages.append(response.message)

        if tool_call.name in REQUIRES_APPROVAL:
            save_checkpoint(checkpoint_path, messages, step, pending_tool_call=tool_call)
            return AgentResult(status="paused", pending_tool_call=tool_call)

        result = dispatch(tool_call, TOOL_REGISTRY)
        messages.append(Message(role=Role.TOOL, tool_result=result))
        step += 1
        save_checkpoint(checkpoint_path, messages, step)

    summary = build_escalation_summary(messages, "hit the step limit without resolving the request")
    return AgentResult(status="escalated", text=summary)


async def run_support_agent(
    client: LLMClient,
    checkpoint_path: Path,
    user_input: str,
    max_steps: int = 5,
) -> AgentResult:
    messages: list[Message] = [
        Message(
            role=Role.SYSTEM,
            content="You are a customer support agent. Use search_faq to answer questions.",
        ),
        Message(role=Role.USER, content=user_input),
    ]
    return await _continue_loop(client, checkpoint_path, messages, step=0, max_steps=max_steps)


async def resume_after_approval(
    client: LLMClient,
    checkpoint_path: Path,
    approved: bool,
    max_steps: int = 5,
) -> AgentResult:
    checkpoint = load_checkpoint(checkpoint_path)
    if checkpoint is None:
        raise FileNotFoundError(f"No checkpoint found at {checkpoint_path}")
    messages, step, pending_tool_call = checkpoint
    if pending_tool_call is None:
        raise ValueError("Checkpoint has no pending tool call to resume")

    if approved:
        result = dispatch(pending_tool_call, TOOL_REGISTRY)
    else:
        result = ToolResult(
            tool_call_id=pending_tool_call.id,
            content="The user did not approve this action.",
            is_error=True,
        )
    messages.append(Message(role=Role.TOOL, tool_result=result))
    step += 1
    return await _continue_loop(client, checkpoint_path, messages, step, max_steps)
