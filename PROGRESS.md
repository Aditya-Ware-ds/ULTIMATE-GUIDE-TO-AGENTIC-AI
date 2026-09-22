# Progress

Written so a new session can resume from this file alone. Update this after every
module/project/capstone. See `/home/aditya/.claude/plans/pasted-content-id-51ca-mission-kind-scone.md`
(or the copy of `PLAN.md` content in git history/PR description) for the full
approved plan, verified landscape notes, and build order this follows.

Legend: ✅ done and tested · 🚧 in progress · ⬜ not started

## Phase 0 -- Scaffold

- ✅ Repo skeleton (`shared/`, `curriculum/`, `projects/`, `capstones/`, `cheatsheets/`, `papers/`, `system-design/`)
- ✅ `pyproject.toml` (uv-managed, Python 3.11+, ruff config, pytest config with `live` marker)
- ✅ `shared/llm/` -- provider-agnostic client (`get_client()`), types, mock provider, pricing table
- ✅ `shared/llm/providers/` -- Anthropic, OpenAI (Responses API), Gemini (Interactions API), Ollama adapters
- ✅ `shared/tracing/` -- real OpenTelemetry tracer, GenAI semantic-convention spans (`invoke_agent`/`chat`/`execute_tool`), in-memory exporter
- ✅ `shared/sandbox/` -- `run_python` (subprocess-isolated) and `run_shell` (allowlisted, no `shell=True`)
- ✅ Tests for all of the above: 26 tests, all offline, no API keys (`make test` green)
- ✅ `make lint` green (ruff check + format)
- ✅ `Makefile` (setup/test/test-live/lint/format/docs/docs-serve/check-links)
- ✅ `.env.example`, `.gitignore`, `.gitattributes`
- ✅ `.github/workflows/ci.yml` (lint + offline tests + docs build on push/PR; link check as a non-blocking job)
- ✅ `mkdocs.yml` + `docs/*.md` (thin pages using `mkdocs-include-markdown-plugin` to include the real root `.md` files, so there's one source of truth for prose, not two)
- ✅ Root docs: `README.md`, `ROADMAP.md`, `SETUP.md`, `HOW_TO_USE.md`, `GLOSSARY.md` (seeded, grows with each module), this file
- ✅ `scripts/check_links.py`
- ✅ `make docs` (`mkdocs build`) verified working. Note: built **without** `--strict`
  -- cross-links between root docs (e.g. `README.md` → `[ROADMAP.md](ROADMAP.md)`)
  resolve correctly on GitHub but MkDocs warns because the included copies live at
  different site URLs (`/roadmap/` not `ROADMAP.md`). Non-fatal; tracked below.

## Level 0 -- Foundations

- ⬜ 00 Programming prerequisites
- ⬜ 01 How LLMs work
- ⬜ 02 Talking to LLMs

## Level 1 -- First agent, no frameworks

- ⬜ 03 Tool use / function calling
- ⬜ 04 The agent loop from scratch
- ⬜ 05 Context engineering
- ⬜ 06 Retrieval & agentic RAG
- ⬜ Project: research assistant with citations

## Level 2 -- Capable agents

- ⬜ 07 Memory & state
- ⬜ 08 Planning & reasoning patterns
- ⬜ 09 Human-in-the-loop
- ⬜ Project: customer-support agent with escalation

## Level 3 -- The ecosystem

- ⬜ 10 Protocols (MCP server + client, A2A, Agent Skills)
- ⬜ 11 Frameworks (all 9: LangGraph, OpenAI Agents SDK, Claude Agent SDK, Google ADK, CrewAI, Microsoft Agent Framework, Pydantic AI, smolagents, LlamaIndex Workflows)
- ⬜ 12 Multi-agent systems
- ⬜ Project: MCP server for a real public API
- ⬜ Project: multi-agent content pipeline

## Level 4 -- Specialized agents

- ⬜ 13 Coding agents
- ⬜ 14 Browser & computer-use agents
- ⬜ 15 Voice & multimodal agents
- ⬜ Project: data-analysis agent with a code sandbox

## Level 5 -- Production engineering

- ⬜ 16 Evaluation
- ⬜ 17 Observability & debugging
- ⬜ 18 Security & safety
- ⬜ 19 Deployment & scale

## Level 6 -- Expert / frontier

- ⬜ 20 Optimizing agents
- ⬜ 21 RL and training for agents
- ⬜ 22 Long-horizon & autonomous agents
- ⬜ 23 Research literacy
- ⬜ 24 Becoming a pro

## Capstones

- ⬜ 1. Production coding agent
- ⬜ 2. Multi-agent research system
- ⬜ 3. Secure enterprise agent

## Final pass (do last)

- ⬜ Full offline test suite
- ⬜ `test-live` smoke run (requires real keys)
- ⬜ Link check
- ⬜ `mkdocs build --strict`
- ⬜ Terminology-vs-`GLOSSARY.md` consistency pass
- ⬜ Prerequisite-ordering check

## Open issues / UNVERIFIED items

- **Gemini streaming**: `shared/llm/providers/gemini_provider.py`'s `stream()` is a
  non-native fallback (calls `complete()` once, re-chunks the text client-side)
  because the Interactions API's native streaming shape wasn't clearly documented
  when verified on 2026-09-22. Fix once confirmed against
  https://ai.google.dev/gemini-api/docs -- likely before or during Module 02/03 live labs.
- **Provider adapter live-path correctness**: `shared/llm/providers/*.py` were
  written against each vendor's *current documented* request/response shape
  (Anthropic Messages API, OpenAI Responses API, Gemini Interactions API, Ollama
  chat API) as of 2026-09-22, but only exercised by offline unit tests so far --
  none has been run against a real API key yet. Run each once for real (small,
  cheap call) before relying on it in a `live`-marked lab test, per Ground Rule 3
  ("all code must run").
- **Model IDs in `shared/llm/client.py`'s `_DEFAULT_MODELS`** (`claude-haiku-4-5`,
  `gpt-5-nano`, `gemini-3-flash`, `qwen3:8b`) and **pricing in
  `shared/llm/pricing.py`** were verified via web search on 2026-09-22 (sources
  inline in `pricing.py`). Re-verify before Level 0/Level 2 lessons that quote
  specific prices, since this is exactly the kind of claim that goes stale fastest.
- **Docs-site cross-links show MkDocs warnings**: root docs use GitHub-relative
  links (`[ROADMAP.md](ROADMAP.md)`) which are correct on GitHub but don't resolve
  to the right site URL when rendered through `docs/*.md`'s include-markdown
  wrappers (see Phase 0 note above). `make docs` succeeds; `mkdocs build --strict`
  does not. Low priority -- would need either a link-rewriting plugin or
  per-context link syntax to fully fix.
- **GitHub repo URL**: `.github/workflows/ci.yml` doesn't need one (checkout is
  automatic), but `mkdocs.yml` has no `repo_url` set since this repo hasn't been
  pushed anywhere yet. Add one once it has a remote.

## Exact next step

Build **Level 0, Module 00 (Programming prerequisites)**: lessons on Python
essentials for this repo, JSON, HTTP/REST, async/await, git, venvs/uv, terminal,
under `curriculum/00-programming-prerequisites/`, following the per-module
structure in the approved plan (`README.md`, `lessons/`, `examples/`, `labs/`,
`quiz.md`, `pitfalls.md`, `resources.md`). Lab: a small async HTTP + JSON CLI tool
(no LLM) with starter/solution/tests. Run the solution's tests before marking done,
then update this file and commit.
