# Comparison matrix and how to choose

**Last verified:** 2026-09-22, based on hands-on builds of all 9 labs in this module.
**Difficulty:** ★★★★☆ · **Time:** ~45 minutes

## Learning objectives

- Compare all 9 frameworks along dimensions that actually matter for choosing one.
- Explain, from direct experience, what "easy to test offline" looks like across very different designs.
- Apply a decision process to pick a framework for a real project.

## The matrix

Built from actually implementing the same tiny reference agent in each --
not from marketing pages.

| Framework | Core abstraction | Offline test mechanism | Notable finding while building it |
|---|---|---|---|
| **LangGraph** | Explicit state graph; `create_agent` (from `langchain`, not the now-deprecated `langgraph.prebuilt.create_react_agent`) | Custom `BaseChatModel` subclass (override `_generate` **and** `bind_tools`) | No built-in fake model scripts tool calls cleanly -- `GenericFakeChatModel` isn't built for this |
| **OpenAI Agents SDK** | Minimal `Agent` + `Runner` | Implement the `Model` protocol directly (`get_response` returning typed Responses-API items) | Keep tool logic in a plain function separate from the `@function_tool` wrapper -- the wrapper's invocation path needs a real `ToolContext` |
| **Claude Agent SDK** | Wraps the real Claude Code CLI/agent loop | **None -- cannot be tested offline** | The only framework with no model-injection point; it's not a "bring your own model" framework at all, by design |
| **Google ADK** | Session-oriented `LlmAgent` + `Runner` | `InMemoryRunner.run_debug(...)`, an **officially documented** debug/testing helper, + custom `BaseLlm` | Most ceremony for a one-shot question (session/user IDs), reflecting its multi-turn-first design |
| **CrewAI** | Role-based `Agent`/`Task`/`Crew` | Custom `BaseLLM` subclass | Structurally different: `BaseLLM.call()` receives `available_functions` directly and is expected to invoke them itself -- no separate tool-call object for an external executor |
| **Microsoft Agent Framework** | `BaseChatClient` + `Agent` | Custom client, **must also inherit `FunctionInvocationLayer`** | Missing that mixin fails *silently* (empty answer, not an error) -- the single easiest mistake to make in this whole module |
| **Pydantic AI** | Typed `Agent` + Pydantic validation | Official `TestModel` (auto-calls tools) and `FunctionModel` (fully scripted) | Best testing story of the 9 -- built for this exact purpose |
| **smolagents** | Minimal `ToolCallingAgent`/`CodeAgent` | Custom `Model` subclass | Requires a strict Google-style `Args:` docstring block or schema generation fails at construction time |
| **LlamaIndex Workflows** | Event-driven `FunctionAgent` | Official `MockFunctionCallingLLM` with a `response_generator` callable | Clean, purpose-built testing support, similar in spirit to Pydantic AI's |

## How to choose, as a process

1. **Does your task need long-running, stateful, multi-turn sessions as a
   first-class concept?** Google ADK's session model is built for this
   directly; most others treat it as something you add.
2. **Do you need explicit, inspectable control flow** (Module 08's
   plan-and-execute/orchestrator-workers made concrete as a graph you can
   read)? LangGraph's state-graph model is the most explicit of the 9.
3. **Are you already in the OpenAI or Anthropic ecosystem specifically, and
   want the thinnest possible wrapper?** OpenAI Agents SDK for the former;
   the Claude Agent SDK for the latter *if and only if* you want Claude
   Code's actual agent loop (file access, permissions, subagents) rather
   than a generic framework -- it is not a general-purpose choice.
4. **Do you need typed, validated inputs/outputs as a core guarantee**, and
   value the best offline-testing experience of this group? Pydantic AI.
5. **Is your team already thinking in "roles" (a researcher, a writer, a
   reviewer)** rather than a graph or a loop? CrewAI's abstraction matches
   that mental model directly (Module 12 revisits this multi-agent framing).
6. **Do you need retrieval (Module 06) as a first-class citizen alongside
   agents**, not bolted on? LlamaIndex Workflows, given LlamaIndex's RAG
   heritage.
7. **Do you want the smallest possible dependency footprint** for a
   code-execution-style agent? smolagents.
8. **Are you already deep in the Microsoft/.NET ecosystem**, or need one SDK
   spanning Python and .NET? Microsoft Agent Framework.

None of these are permanent commitments -- because you built the underlying
loop by hand (Modules 03-09), migrating between frameworks later means
re-learning syntax, not re-learning concepts.

## Deeper: testing ergonomics predicted real friction, not just annoyance

Across all 9 builds, the frameworks with an official, documented,
purpose-built testing mechanism (Pydantic AI's `TestModel`/`FunctionModel`,
LlamaIndex's `MockFunctionCallingLLM`, Google ADK's `run_debug`) took
noticeably less time and produced fewer surprises than the ones requiring a
hand-rolled fake client (LangGraph, OpenAI Agents SDK, CrewAI, Microsoft
Agent Framework, smolagents) -- and the Microsoft Agent Framework's missing
`FunctionInvocationLayer` mixin produced a *silent* wrong answer, the worst
kind of framework surprise (Module 04 lesson 1's "what does it do silently
that surprises you" question, answered concretely). If a framework's testing
story is this module's biggest signal of anything, it's that "how does this
framework want you to test it" is a legitimate, load-bearing evaluation
criterion for choosing one, not an afterthought.

## When not to use this

Don't let this matrix substitute for evaluating a framework against your
*actual* project's requirements -- it reflects one tiny reference task,
deliberately. A framework that felt heaviest here (CrewAI, Microsoft Agent
Framework) may be exactly right for a task that needs what it's built for
(role-based teams; .NET interop) that this trivial calculator agent never
exercised.

## Key takeaways

- All 9 frameworks converge on the same underlying loop (Module 04); they differ in abstraction level, control-flow explicitness, and testing ergonomics.
- Testing ergonomics varied enormously and predicted real development friction -- treat "how do I test this offline" as a first-class evaluation criterion.
- The Claude Agent SDK is a structurally different tool (drives the real Claude Code loop) from the other 8 general-purpose frameworks -- know this before reaching for it.

## Labs

`labs/01-langgraph/` through `labs/09-llamaindex-workflows/`
