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

- ✅ 00 Programming prerequisites -- 5 lessons, 4 runnable examples (all executed
  and verified), 1 lab (async fetch + JSON CLI: starter/solution/tests, 10 tests
  passing against `solution/`, correctly failing against unimplemented
  `starter/`), quiz, pitfalls, resources (verified 2026-09-22). Also added
  `shared/testing/lab_loader.py` (+ its own 4 tests) as the reusable
  starter-vs-solution test-loading pattern every future lab will use.
- ✅ 01 How LLMs work -- 5 lessons (tokens/tokenizers, context windows,
  sampling/decoding, embeddings, reasoning models & hallucination), 3 runnable
  examples (verified), 1 lab (token counting with real `tiktoken` + a
  temperature/softmax sampling simulator: starter/solution/tests, 10 tests
  passing against `solution/`). Links checked (`scripts/check_links.py`: all
  17 unique links OK).
- ✅ 02 Talking to LLMs -- 5 lessons (messages/roles, streaming, structured
  outputs, prompt engineering fundamentals, cost & latency), 4 runnable examples
  (verified), 1 lab (chat loop + structured extraction + cost estimation built on
  `shared.llm`: starter/solution/tests, 9 tests passing against `solution/`).
  While verifying structured-output API shapes for lesson 3, found and fixed two
  real gaps in the Phase-0 provider adapters: `AnthropicProvider.complete()` and
  `GeminiProvider.complete()` both accepted `response_schema` but silently
  ignored it. Now wired to Anthropic's GA `output_config.format` and Gemini's
  current (post-May-2026-migration) `response_format`. Added `jsonschema` as a
  dependency. Links checked (24 unique, all OK).

## Level 1 -- First agent, no frameworks

- ✅ 03 Tool use / function calling -- 3 lessons (tool schemas, dispatch &
  execution, error handling & retries), 3 runnable examples (verified), 1 lab
  (hand-written calculator + weather tool-calling loop: `ast`-based safe
  arithmetic, no `eval()`; starter/solution/tests, 14 tests passing against
  `solution/`, 13/14 correctly failing against `starter/` -- the one that
  trivially passes is an intentionally lenient `pytest.raises(Exception)`
  check, noted but not worth over-engineering). Links checked (27 unique, all OK).
- ✅ 04 The agent loop from scratch -- 3 lessons (the agent loop, stopping
  conditions, ReAct pattern), 3 runnable examples (verified), 1 lab (ReAct agent
  answering 2-hop questions with search + calculate tools: starter/solution/tests,
  9 tests passing against `solution/`, all 9 correctly failing against
  `starter/`). Links checked (29 unique, all OK).
- ✅ 05 Context engineering -- 3 lessons (what goes in context, compaction &
  summarization, context rot), 3 runnable examples (verified; the context-rot
  demo uses explicitly-labeled made-up numbers for shape illustration, not real
  measurements -- resources.md links to the real Chroma study for actual
  figures), 1 lab (agent loop with compaction, keeping a real `tiktoken`-based
  token count under budget across an 18+ step scripted run: starter/solution/
  tests, 8 tests passing against `solution/`, all 8 correctly failing against
  `starter/`). Links checked (33 unique, all OK).
- ✅ 06 Retrieval & agentic RAG -- 3 lessons (chunking & embeddings, hybrid
  search & reranking, agentic RAG), 3 runnable examples (verified; hybrid search
  demo uses a deterministic `hashlib`-based toy embedding, clearly labeled as
  not a real model), 1 lab (agentic RAG over 4 bundled support-doc `.txt` files
  with a `search_documents` tool the model can call multiple times:
  starter/solution/tests, 16 tests passing against `solution/`, all failing
  correctly against `starter/`). Fixed a link-checker false-positive along the
  way: `scripts/check_links.py` now sends a normal User-Agent header (some
  sites, Wikipedia included, 403 the default httpx UA). Links checked (37
  unique, all OK). **Levels 0-1 (Modules 00-06) are now fully complete** except
  the interleaved project below.
- ✅ Project: research assistant with citations -- integration project reusing
  Module 06's retrieval patterns and Modules 03-05's agent loop, adding
  citation extraction/verification (`extract_citations`/`verify_citations`)
  that flags a fabricated source name even though it "looks" like a real
  citation -- a concrete, testable instance of Module 01 lesson 5's
  hallucination point. 5 bundled spaceflight-history documents,
  starter/solution/tests split (same pattern as labs), 12 tests passing
  against `solution/`, all failing/erroring correctly against `starter/`.

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
- **Docs-site cross-links show MkDocs warnings**: root *and curriculum* docs use
  GitHub-relative links (e.g. `[ROADMAP.md](ROADMAP.md)`,
  `[lessons/01-...](lessons/01-python-essentials.md)`) which are correct on
  GitHub but don't resolve to the right site URL when mirrored through
  `docs/**/*.md`'s `scripts/sync_docs.py`-generated include-markdown wrappers.
  `make docs` succeeds (non-fatal warnings); `mkdocs build --strict` does not.
  Low priority -- content and navigation both work, just not every in-page link
  on the built site; would need a link-rewriting plugin to fully fix. `docs/`
  also currently has no explicit `nav:` entries for curriculum/projects/etc.
  pages (only the 6 root pages are in `nav:`) -- they're still built and
  searchable, just not in the top nav. Add nav entries (or an
  automatic-nav plugin) once there's enough curriculum content to be worth it.
- **GitHub repo URL**: `.github/workflows/ci.yml` doesn't need one (checkout is
  automatic), but `mkdocs.yml` has no `repo_url` set since this repo hasn't been
  pushed anywhere yet. Add one once it has a remote.

## Exact next step

Build **Level 2, Module 07 (Memory & state)**: lessons on short-term vs.
long-term memory, episodic vs. semantic memory, memory stores, and
checkpointing/resumption, under `curriculum/07-memory-and-state/`, following
the same per-module structure used so far. Per the approved plan, the lab
should add checkpointed, resumable state to the running agent pattern (a
"kill-and-resume" test: serialize agent state mid-run, reload it in a fresh
process/object, and prove it continues correctly) -- this is meaningfully new
territory versus Modules 03-06 (which never needed to persist state across
process boundaries), so budget real design time for the serialization format
(plain JSON of the `Message` list plus any loop-specific state, e.g. step
count, is likely sufficient and keeps this offline-testable with no new
dependencies). Distinguish this clearly from Module 05's compaction (shrinking
context *within* a run) and Module 06's retrieval (finding *documents*) --
memory here means deliberately persisting an agent's *own state* across
separate runs. Run the solution's tests before marking done, then update this
file and commit.
