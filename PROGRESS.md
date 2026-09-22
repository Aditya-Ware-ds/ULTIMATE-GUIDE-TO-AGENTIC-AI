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

- ✅ 07 Memory & state -- 3 lessons (memory types, memory stores, checkpointing
  & resumption), 3 runnable examples (verified), 1 lab (resumable agent:
  checkpoint messages+step to JSON, resume without repeating completed model
  calls -- the "kill and resume" test simulates a crash by calling
  `run_one_step` directly rather than letting a single call run to completion:
  starter/solution/tests, 11 tests passing against `solution/`, all failing
  correctly against `starter/`).
- ✅ 08 Planning & reasoning patterns -- 5 lessons (plan-and-execute, reflection
  & evaluator-optimizer, routing & parallelization, orchestrator-workers,
  workflow vs. agent), 3 runnable examples (verified, including a real
  measured sequential-vs-parallel timing difference), 1 lab (both
  plan-and-execute AND evaluator-optimizer implemented for the same task, with
  a written comparison in the solution's docstring: starter/solution/tests, 9
  tests passing against `solution/`, all failing correctly against `starter/`).
- ✅ 09 Human-in-the-loop -- 3 lessons (approval gates, interrupt & resume,
  escalation & UX), 3 runnable examples (verified), 1 lab (agent that pauses
  before a gated `send_email` tool call, persisting the pending call to a
  Module-07-style checkpoint, and resumes correctly on approval or rejection
  -- rejection modeled as a normal `ToolResult(is_error=True)`, reusing
  Module 03's recoverable-failure mechanism: starter/solution/tests, 6 tests
  passing against `solution/`, all failing correctly against `starter/`).
  **Level 2 (Modules 07-09) is now fully complete** except the interleaved
  project below.
- ✅ Project: customer-support agent with escalation -- integration project
  reusing Module 09's approval-gate/checkpoint pattern (gated `issue_refund`
  tool) and escalation pattern (hitting `max_steps` now returns
  `status="escalated"` with a full step-by-step summary instead of a generic
  stop message). FAQ lookup uses a simple in-memory keyword-overlap match
  rather than Module 06's full hybrid-search machinery, by design (this
  project's point is approval+escalation integration, not retrieval).
  starter/solution/tests split, 8 tests passing against `solution/`, all
  failing correctly against `starter/`.

## Level 3 -- The ecosystem

- ✅ 10 Protocols -- 3 lessons (MCP overview & architecture, building an MCP
  server+client, A2A & Agent Skills), 5 runnable examples (verified, including
  a real subprocess-spawning stdio MCP client-server connection), 3 labs:
  (1) real MCP server (wraps Module 03's calculator/weather tools) + real
  client, tested via in-process `Client(mcp_server_instance)` connection --
  5 tests passing; (2) A2A-style task lifecycle state machine (simplified,
  not the full SDK) -- 12 tests passing; (3) packaging a tool as a validated
  `SKILL.md` (a real hand-written skill file, not just Python) -- 9 tests
  passing. All labs' starter/ correctly fail. Added `mcp` and `pyyaml` as
  dependencies. **Verification note**: web search/fetch results for the `mcp`
  Python package described a stale pre-rework API
  (`mcp.server.fastmcp.FastMCP`); installed the actual package (2.2.0) and
  used `dir()`/`inspect.signature()` to get ground-truth current API
  (`mcp.server.MCPServer`, `mcp.Client`, etc.) before writing any lesson/lab
  code, then executed every code sample directly to confirm it runs -- see
  Module 10's pitfalls.md for this as a general lesson about fast-moving
  specs. Links checked (47 unique, all OK).
- ✅ 11 Frameworks -- **all 9 built and tested**, per the user's explicit "all 9,
  full builds" decision: LangGraph, OpenAI Agents SDK, Claude Agent SDK,
  Google ADK, CrewAI, Microsoft Agent Framework, Pydantic AI, smolagents,
  LlamaIndex Workflows. Same reference agent (a calculator tool answering
  "what is 15*7+3") implemented once per framework, each with its own
  starter/solution/tests. Every framework's actual current API was verified
  by installing it and using `dir()`/`inspect.signature()` directly (several
  search results / tutorials described stale, pre-rework APIs -- see the
  module's pitfalls.md). 2 lessons (why frameworks exist; a comparison matrix
  written *after* all 9 were actually built, not from marketing pages), plus
  per-module quiz/pitfalls/resources. Frameworks live outside the default
  dependency set (`uv run --with <package>`, not persistent groups --
  Microsoft's `agent-framework` needs `mcp<2`, this project needs `mcp>=2`,
  which broke `uv sync` outright when tried as a group); each lab's tests use
  `pytest.importorskip` so `make test` stays green without any framework
  installed (178 passed, 9 skipped). **Claude Agent SDK is a documented
  exception**: it wraps the real Claude Code agent loop with no model-
  injection point, so only its tool-definition/arithmetic logic is offline-
  testable; its full agent-loop test is `@pytest.mark.live` (needs a real key,
  not run in this session). Links checked (61 unique, all OK).
- ✅ 12 Multi-agent systems -- 3 lessons (topologies: supervisor-worker,
  hierarchical, handoff, swarm, debate; concrete failure modes: infinite
  handoff loops, duplicated work, ambiguous worker-success signals, cascading
  cost; when multi-agent is a mistake, with a decision process), 2 runnable
  examples (`supervisor_worker_demo.py`, `handoff_budget_demo.py`, both
  verified), 1 lab: hand-rolled supervisor-worker with 3 specialized workers
  (researcher/writer/critic), **no framework** -- built directly on Module
  08's orchestrator-workers signature. The supervisor requires an explicit
  `"status"` field from workers and escalates (without calling synthesis)
  rather than inferring success from mere output, per lesson 02's core
  lesson; 6 tests passing, starter's gaps correctly raise
  `NotImplementedError`. Full quiz/pitfalls/resources written. 184 passed, 9
  skipped repo-wide; links checked (65 unique, all OK).
- ✅ Project: MCP server for a real public API -- a real
  `mcp.server.MCPServer` wrapping [Open-Meteo](https://open-meteo.com/en/docs)
  (verified 2026-09-22: no API key needed for non-commercial use) with one
  tool, `get_current_weather(latitude, longitude)`. Default offline tests hit
  a tiny local HTTP server shaped like Open-Meteo's real response (same
  technique as Module 00's async-fetch-cli lab), not the real internet; one
  `@pytest.mark.live` test hits the real API for real and passes. **Note**:
  a tool returning a bare `-> dict` annotation gets no MCP `structured_content`
  (verified empirically -- `output_schema` stays `None`); annotating the
  return type concretely as `dict[str, float | str]` fixes it. 3 offline
  tests + 1 live test passing; starter's gaps correctly raise
  `NotImplementedError`. Links checked (66 unique, all OK).
- ✅ Project: multi-agent content pipeline -- 3 specialized stages
  (researcher, writer, critic) reusing Module 12's "explicit status, not
  inferred success" discipline (a failed research stage escalates
  immediately, no draft/critique calls) plus Module 08's evaluator-optimizer
  loop shape for the writer/critic revision cycle (bounded by
  `max_revisions`, escalates -- doesn't silently claim success -- if never
  approved). 7 tests passing covering first-try success, one revision,
  research failure, and exhausted revisions with exact model-call-count
  assertions; starter's gaps correctly raise `NotImplementedError`. 194
  passed, 9 skipped repo-wide; links checked (66 unique, all OK). **Level 3
  and its interleaved projects are now fully complete.**

## Level 4 -- Specialized agents

- ✅ 13 Coding agents -- 4 lessons (sandboxed code execution, using
  `shared/sandbox/` for real for the first time since Phase 0; repo
  navigation/editing with path-traversal-safe file tools; the test-driven
  agent loop, Module 04's ReAct loop plus a mechanical pytest-based stop
  signal instead of a model judgment call; how terminal coding agents work,
  verified 2026-09-22 against Claude Code's current best-practices docs --
  explore/plan/code/commit, "give it a way to verify," context-window
  management as the primary constraint). 1 runnable example
  (`sandboxed_tools_demo.py`, verified). 1 lab: an agent that fixes a real
  bug in a small bundled sample repo (`sample_repo/`, a read-only template
  copied into a temp dir outside the git tree per test run, both to avoid
  polluting tracked files and because a nested-in-repo `pytest` subprocess
  would otherwise pick up this project's own `pyproject.toml` config) using
  `read_file`/`write_file`/`run_tests` tools, entirely inside
  `shared/sandbox/shell_sandbox.py`. The agent's final status is an
  independent re-run of the tests, never the model's own claim -- proven by
  a test where the model falsely claims success and the loop still reports
  `"failed"`. 10 tests passing; starter's gaps correctly raise
  `NotImplementedError`. Added `norecursedirs = ["sample_repo"]` to
  `pyproject.toml`'s pytest config so the repo's own `make test` never
  collects the sample repo's deliberately-failing fixture test. 204 passed,
  9 skipped repo-wide; links checked (70 unique, all OK).
- ✅ 14 Browser & computer-use agents -- 3 lessons: browser automation
  (Playwright, verified current on 2026-09-22, DOM/selector-based, a small
  typed `goto`/`click`/`get_text` action vocabulary plus a URL allowlist
  mirroring Module 13's path-scoping); screenshots vs. the DOM (**corrected
  a stale working assumption while writing this**: Claude's, OpenAI's, and
  Gemini's computer-use tools were checked directly against each vendor's
  current docs on 2026-09-22 and all three currently use screenshot +
  pixel-coordinate perception only, *not* an accessibility tree, contrary to
  the original PLAN.md's landscape note -- corrected here per Ground Rule 1);
  reliability tricks (explicit wait conditions over fixed sleeps,
  retry-only-on-transient-failures, narrow action vocabulary as a
  reliability technique, not just a security one). 1 runnable example
  (`browser_tools_demo.py`, verified, uses a fake session -- no real browser
  needed). 1 lab: a browser-automation agent (Module 04's ReAct loop) against
  a bundled local `sample_site/index.html` whose "View details" button
  creates a real DOM element on click (so the task genuinely requires a
  click before a read, not just one page-read). Offline tests use a
  hand-written `FakeBrowserSession` that mirrors the real page's actual
  click-then-reveal behavior exactly; 8 offline tests passing; starter's
  gaps correctly raise `NotImplementedError`. **One `@pytest.mark.live` test
  drives a real Playwright browser and was written but not run this
  session** -- `uv run --with "playwright>=1.47" python -c "from
  playwright.sync_api import ..."` did not finish downloading within 120s in
  this environment; run it manually per the lab README before trusting the
  live path. 212 passed, 9 skipped, 2 deselected repo-wide; links checked
  (74 unique, all OK).
- ✅ 15 Voice & multimodal agents -- **extended `shared/llm/` for the first
  time since Phase 0**: added `ImageContent` (`media_type` + `data_base64`)
  and `Message.images: list[ImageContent]`, wired into `AnthropicProvider`
  only (verified against
  https://platform.claude.com/docs/en/build-with-claude/vision on
  2026-09-22: base64 image content blocks, images-before-text ordering,
  supported formats/token-cost table) -- OpenAI/Gemini/Ollama adapters
  deliberately and documentedly still ignore `Message.images` (a new,
  explicit entry below in Open Issues). 2 lessons (vision inputs; realtime
  voice architecture, verified against OpenAI's current Realtime API docs
  -- direct audio processing, WebRTC/WebSocket transport, VAD-based
  turn-taking/barge-in -- conceptual only, no required runnable lab per the
  approved plan, to avoid a live metered audio dependency). 1 runnable
  example (`image_encoding_demo.py`, verified, includes a from-scratch
  minimal PNG encoder). 1 lab: `load_image`/`ask_about_image` against a
  64x64 synthetic PNG generated with pure Python (`zlib`/`struct`, no
  Pillow dependency, no licensing ambiguity) baked into
  `images/red_square_on_blue.png`. 3 offline tests passing (base64
  round-trip, unsupported-extension rejection, mock-provider message
  construction); starter's gaps correctly raise `NotImplementedError`.
  **One `@pytest.mark.live` test against the real Anthropic API was written
  but not run this session** -- no `ANTHROPIC_API_KEY` was available in
  this environment; run it manually per the lab README before trusting the
  live path. 215 passed, 9 skipped, 3 deselected repo-wide; links checked
  (78 unique, all OK). **Level 4 is now fully complete.**
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

- **`Message.images` only wired into `AnthropicProvider`**: Module 15 added
  `ImageContent`/`Message.images` to `shared/llm/types.py` but only
  `AnthropicProvider` converts it into a real API request; OpenAI, Gemini,
  and Ollama adapters silently ignore it. Wire in the others once their
  current image-block shapes are verified the same way (each vendor's
  format differs and each has changed shape before -- don't guess from this
  session's Anthropic verification).
- **Module 15's live vision test not run**: no `ANTHROPIC_API_KEY` was
  available in this session's environment; run
  `uv run pytest -m live curriculum/15-voice-and-multimodal-agents/labs/01-vision-qa-agent/tests`
  manually before trusting the real-API path.
- **Module 14's live Playwright test not run**: `uv run --with
  "playwright>=1.47" python -c "from playwright.sync_api import ..."` did
  not finish downloading within a 120s timeout in this session's
  environment. Run
  `uv run --with "playwright>=1.47" playwright install chromium` then the
  live test manually per that lab's README when network access allows.
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

Level 4 is complete. Build the **"data-analysis agent with a code sandbox"**
project next, under `projects/05-data-analysis-agent/` (confirm exact
naming against the `projects/0N-name/` convention already established).
Reuse `shared/sandbox/code_sandbox.py` directly (already built and tested in
Phase 0, exercised for real in Module 13): an agent that writes and runs
Python to analyze a small bundled dataset (e.g. a CSV with a handful of
columns/rows, bundled in the project directory, not fetched live) inside the
sandbox, following Module 13's exact discipline -- never `exec()` generated
code directly, only through `run_python`, with the same reasoning
(untrusted, model-generated code needs process isolation, a timeout, and a
restricted environment). The agent's loop should be Module 04's ReAct shape
again, with a `run_python_analysis(code: str) -> str` tool (or similarly
named) that returns the sandboxed stdout, and the task should be answerable
by writing a short pandas/csv-module script and reading its printed output
-- keep the dataset and task small enough that the whole thing stays
offline-testable via the mock provider's scripted tool-call sequence, the
same pattern used in every ReAct-loop lab so far. After this project, start
**Level 5, Module 16 (Evaluation)** under `curriculum/16-evaluation/`: eval-
driven development, golden datasets, LLM-as-judge (and its known biases),
trajectory/tool-call evals, regression suites, and current public benchmarks
(SWE-bench, GAIA, tau-bench, BrowseComp, WebArena, OSWorld, Terminal-Bench --
re-verify each is still current and accurately described before citing it,
per Ground Rule 1, the same discipline that caught the stale computer-use
claim in Module 14). Lab: a small golden-dataset eval harness plus an
LLM-as-judge for one earlier agent (e.g. Module 04's ReAct agent or Module
13's coding agent), runnable offline against the mock provider. Two
follow-ups noted in Open Issues above are worth revisiting when this
environment has reliable network access: Module 14's live Playwright test
and Module 15's live Anthropic vision test were both written but not
executed this session. Run each solution's tests before marking done, then
update this file and commit after each project/module.
