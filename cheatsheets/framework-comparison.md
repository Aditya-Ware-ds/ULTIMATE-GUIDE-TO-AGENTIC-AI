# Cheatsheet: agent framework comparison

Condensed from `curriculum/11-frameworks/lessons/02-comparison-matrix-and-how-to-choose.md`
-- built from actually implementing the same reference agent in all 9,
not from marketing pages. **Last verified:** 2026-09-22.

| Framework | Core abstraction | Offline test mechanism | Watch out for |
|---|---|---|---|
| **LangGraph** | Explicit state graph; `create_agent` | Custom `BaseChatModel` subclass | No built-in fake model scripts tool calls cleanly |
| **OpenAI Agents SDK** | Minimal `Agent` + `Runner` | Implement the `Model` protocol directly | Keep tool logic separate from the `@function_tool` wrapper |
| **Claude Agent SDK** | Wraps the real Claude Code agent loop | **None -- can't be tested offline** | Not a "bring your own model" framework at all |
| **Google ADK** | Session-oriented `LlmAgent` + `Runner` | Official `InMemoryRunner.run_debug(...)` | Most ceremony for a one-shot question |
| **CrewAI** | Role-based `Agent`/`Task`/`Crew` | Custom `BaseLLM` (invokes tools itself) | Structurally different tool-invocation path from the others |
| **Microsoft Agent Framework** | `BaseChatClient` + `Agent` | Custom client + `FunctionInvocationLayer` mixin | Missing that mixin fails **silently** -- empty answer, no error |
| **Pydantic AI** | Typed `Agent` + Pydantic validation | Official `TestModel`/`FunctionModel` | Best testing story of the 9 |
| **smolagents** | Minimal `ToolCallingAgent`/`CodeAgent` | Custom `Model` subclass | Requires a strict Google-style `Args:` docstring |
| **LlamaIndex Workflows** | Event-driven `FunctionAgent` | Official `MockFunctionCallingLLM` | Clean, purpose-built testing support |

## How to choose

1. **Long-running, stateful, multi-turn sessions as a first-class concept?** → Google ADK.
2. **Explicit, inspectable control flow (a graph you can read)?** → LangGraph.
3. **Thinnest wrapper in the OpenAI/Anthropic ecosystem specifically?** → OpenAI Agents SDK / Claude Agent SDK (only if you want Claude Code's actual loop, not a general framework).
4. **Typed, validated I/O as a core guarantee, best offline testing?** → Pydantic AI.
5. **Team thinks in "roles" (researcher, writer, reviewer)?** → CrewAI.
6. **Retrieval as a first-class citizen alongside agents?** → LlamaIndex Workflows.
7. **Smallest dependency footprint for a code-execution-style agent?** → smolagents.
8. **Deep in the Microsoft/.NET ecosystem?** → Microsoft Agent Framework.

**None of these are permanent commitments** -- if you built the underlying
loop by hand first (Modules 03-09), migrating later means re-learning
syntax, not concepts.

See: `curriculum/11-frameworks/README.md`.
