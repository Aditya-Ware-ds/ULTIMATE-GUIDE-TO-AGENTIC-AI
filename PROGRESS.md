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
- ✅ Project: data-analysis agent with a code sandbox -- a `run_analysis`
  tool executing model-written Python for real via
  `shared.sandbox.code_sandbox.run_python` (never `exec()`, per Module 13's
  discipline reused directly) against a bundled `dataset/sales.csv` (copied
  into a temp dir per test, same reasoning as Module 13's `repo_copy`).
  Errors from the sandboxed code (verified with a real `NameError`) are
  surfaced as a string, not raised, so the Module 04 ReAct loop can
  self-correct on the next step -- proven by a test where the model's first
  tool call has a real bug and the second one fixes it. 5 tests passing
  (real sandboxed execution with a correct-code assertion on real computed
  output, real error surfacing, dispatch, self-correction, max_steps);
  starter's gaps correctly raise `NotImplementedError`. **Level 4 and its
  interleaved projects are now fully complete.** 220 passed, 9 skipped, 3
  deselected repo-wide; links checked (78 unique, all OK).

## Level 5 -- Production engineering

- ✅ 16 Evaluation -- Level 5 begins. 3 lessons: eval-driven development and
  golden datasets; LLM-as-judge (structured-output verdicts, and the three
  documented judge biases -- position, verbosity, self-preference -- with
  mitigations, citing Zheng et al. 2023 and Liu et al. 2023, both verified
  real via arXiv abstracts on 2026-09-22); trajectory evals and current
  public benchmarks (SWE-bench, GAIA, tau-bench, BrowseComp, WebArena,
  OSWorld, Terminal-Bench -- SWE-bench and GAIA's current-active status
  verified directly; the lesson explicitly tells readers to re-verify
  leaderboard numbers rather than quoting any, since that's the part that
  goes stale). 1 runnable example (`judge_bias_demo.py`, verified --
  demonstrates position bias and the swap-and-check mitigation with a
  deliberately biased mock judge). 1 lab: a golden-dataset eval harness
  (`evaluate_dataset`) with an LLM-as-judge, generic over any
  `agent_fn(client, question) -> str` signature so it could grade any
  earlier module's agent. 4 tests passing (structured verdict, call
  ordering, accuracy computation, perfect score); starter's gaps correctly
  raise `NotImplementedError`. 224 passed, 9 skipped, 3 deselected
  repo-wide; links checked (82 unique, all OK).
- ✅ 17 Observability & debugging -- **`shared/tracing/tracer.py` (built in
  Phase 0, unit-tested there but never wired around a real agent loop) is
  finally exercised by a lab.** 3 lessons: tracing agent loops (wrapping
  Module 04's exact ReAct loop in `invoke_agent_span`/`chat_span`/
  `execute_tool_span`, recording token usage via `span.set_attribute(...)`
  once the response is known, never as opening kwargs); replaying failed
  runs (`replay_trace`: sort by `start_time`, indent by walking each span's
  `parent` chain -- explicitly connected back to Module 12 lesson 02's
  "multi-agent debugging needs the whole graph" point); cost/latency
  dashboards (`summarize_usage` rolling up `gen_ai.usage.*` attributes,
  feeding into Module 02's `estimate_cost`, plus why a single run isn't a
  dashboard -- trends need aggregation across many runs, the same principle
  as Module 16's eval accuracy). 1 runnable example
  (`trace_replay_demo.py`, verified, produces a real nested 4-span trace
  and replays it correctly indented). 1 lab: a traced ReAct agent
  (calculate tool) plus `replay_trace`/`summarize_usage`; 5 tests passing,
  including one that walks the actual parent chain to prove an
  `execute_tool` span nests under `invoke_agent` (not a hardcoded depth
  assumption); starter's gaps correctly raise `NotImplementedError`. 229
  passed, 9 skipped, 3 deselected repo-wide; links checked (84 unique, all
  OK).
- ✅ 18 Security & safety -- **corrected a fabrication-risk landscape claim
  from the original PLAN.md before writing anything**: verified against
  OWASP's current site (2026-09-22) that the LLM Top 10 is the **2025**
  list (not "2026"), Excessive Agency ranks **#6** (not "#3"), and there is
  **no verified numbered "OWASP Top 10 for Agentic Applications
  (ASI01-ASI10)"** -- only a separate, non-numbered "Agentic AI: Threats
  and Mitigations" guide (published 2025-02-17) from OWASP's Agentic
  Security Initiative. resources.md documents this correction explicitly.
  3 lessons: prompt injection (direct vs. indirect, why indirect is the
  harder problem for every tool-using agent built since Module 04); tool
  permissions and least privilege (names Module 13's `resolve_within_repo`/
  `DEFAULT_ALLOWED_COMMANDS` and Module 14's URL allowlist explicitly as
  this same pattern, applied to a new consequential tool); OWASP + a
  4-step red-team process (pick a scenario, prove the exploit with a
  failing test, patch, prove the fix). 1 runnable example
  (`injection_defense_demo.py`, verified -- vulnerable vs. patched
  `send_email` side by side against the identical poisoned-document
  scenario). 1 lab: a `read_document`/`send_email` agent with a real
  embedded prompt-injection document; the core red-team test scripts a
  simulated "successfully manipulated" model attempting to email an
  attacker and asserts `_SENT_EMAILS` stays empty -- proving the tool-level
  allowlist blocks the exploit regardless of the model's decision, not by
  hoping the model resists the injection. 4 tests passing; starter's gaps
  correctly raise `NotImplementedError`. 233 passed, 9 skipped, 3 deselected
  repo-wide; links checked (88 unique, all OK).
- ✅ 19 Deployment & scale -- Level 5 closes. **Added `fastapi>=0.115.0` as a
  real, persistent dependency** (verified current/actively maintained
  2026-09-22, first new base dependency since Phase 0; installs cleanly, no
  resolution conflicts) -- also added `[tool.ruff.lint.flake8-bugbear]
  extend-immutable-calls` for FastAPI's `Depends()`-in-defaults idiom
  (ruff's B008 otherwise flags it as a false-positive mutable-default bug).
  3 lessons: streaming services and durable jobs (FastAPI `StreamingResponse`
  + `TestClient`, tested fully in-process with zero network; durable jobs
  named explicitly as Module 07's checkpoint/resume triggered by
  infrastructure instead of a simulated crash); retries, idempotency, and
  rate limits (an idempotency-key pattern verified against Stripe's real,
  current production docs, including the ~24-hour key-expiry window);
  prompt caching and cost optimization (Anthropic's current `cache_control`
  mechanics and cache-hit cost reductions, verified 2026-09-22; model
  routing tied back to Module 08's routing pattern and Module 12's
  explicit-status escalation). 1 runnable example
  (`idempotent_service_demo.py`, verified -- a real FastAPI app tested via
  `TestClient`, proving a retried request doesn't re-call the agent). 1 lab:
  a FastAPI service (`/jobs`, `/jobs/{key}`, `/jobs/stream`) with idempotent
  job handling, using dependency-injection overrides to swap in the mock
  provider for offline testing. 7 tests passing; starter's gaps correctly
  raise `NotImplementedError` (surfaces through `TestClient` as expected).
  240 passed, 9 skipped, 3 deselected repo-wide; links checked (91 unique,
  all OK).

## Level 6 -- Expert / frontier

- ✅ 20 Optimizing agents -- Level 6 begins. **Verified DSPy for real**
  (installed `dspy` 3.3.1 via `uv run --with dspy`, read `dspy.BaseLM`'s
  actual installed source with `inspect.getsource()`, and iteratively
  smoke-tested a scripted offline LM end-to-end -- including discovering
  and working around two real, undocumented-in-summary-form gotchas: the
  legacy LM contract needs an object with `.choices[0].message.content`
  attribute access, not a dict, and DSPy's default `ChatAdapter` silently
  double-calls via a `JSONAdapter` fallback unless `JSONAdapter` is
  configured explicitly). 3 lessons: DSPy signatures and modules
  (`dspy.Predict`, a fully offline `dspy.BaseLM` subclass); optimizing with
  a metric (a real, verified `dspy.BootstrapFewShot.compile()` run,
  producing real inspectable `optimized.demos`); fine-tuning, distillation,
  and local models (conceptual, ties to `shared/llm/`'s `OllamaProvider`
  and Module 19's cost-optimization material, with an explicit
  cheapest-first lever ordering: prompt optimization -> routing ->
  distillation -> fine-tuning). 1 runnable example
  (`scripted_lm_demo.py`, verified, requires `uv run --with dspy`). 1 lab:
  a DSPy program optimized with `BootstrapFewShot` against a scripted,
  deterministic offline LM -- 5 tests passing, including one that asserts
  `len(optimized.demos) >= 1` as concrete proof optimization actually
  happened, not just that `.compile()` ran without error; starter's gaps
  correctly raise `NotImplementedError`. `dspy` is NOT a persistent
  dependency (Module 11's `uv run --with` pattern, since it's a heavy,
  fast-moving framework) -- `pytest.importorskip("dspy")` makes this lab's
  tests show as **skipped** (not failed) in the default `make test`. 240
  passed, 10 skipped, 3 deselected repo-wide; links checked (93 unique, all
  OK -- one transient timeout on a pre-existing SETUP.md link resolved on
  retry, unrelated to this module).
- ✅ 21 RL and training for agents -- 3 lessons: verifiable rewards (RLVR,
  reusing Module 13's exact sandboxing discipline for the reward function
  itself; explicitly complementary to RLHF, not a replacement); reward
  hacking (a model exploiting a reward function's letter without its
  intent; explicitly tied back to Module 18's "the tool/boundary is the
  actual constraint, not the model's intentions" framing); GRPO and
  group-relative advantages (the exact formula `(r - mean) / std`, **verified
  directly against Hugging Face TRL's current GRPO trainer docs** on
  2026-09-22 -- confirmed GRPO eliminates PPO's separate critic model
  entirely). 1 runnable example (`grpo_advantage_demo.py`, verified). 1
  lab: a verifiable reward function (real sandboxed code execution via
  `shared.sandbox.code_sandbox.run_python`) plus a real, exact
  implementation of GRPO's advantage formula -- explicitly and repeatedly
  labeled throughout (README, lessons, pitfalls) as illustrating the
  reward/advantage **math** only, not a real policy-gradient training step,
  to avoid any impression this curriculum implements actual RL training.
  9 tests passing, including an exact-value check against the verified
  formula and a zero-std edge case; starter's gaps correctly raise
  `NotImplementedError`. 249 passed, 10 skipped, 3 deselected repo-wide;
  links checked (95 unique, all OK).
- ✅ 22 Long-horizon & autonomous agents -- 3 lessons: context and
  verification at scale (which earlier modules' patterns scale unmodified
  to a long horizon -- Module 13's sandboxing, Module 18's tool
  permissions -- and which need rethinking -- Module 04's single-loop
  `max_steps`, Module 07's single-conversation checkpoint); reliability
  math (naive chain success = `p**n`; a worked, arithmetic-checked example:
  95% per-step reliability degrades to ~7.7% over 50 dependent steps);
  progress files and resumability (extends Module 07's checkpoint to a
  multi-task shape, **explicitly and directly identified as the same
  pattern this repository's own `PROGRESS.md` has used across this entire
  multi-session build** -- not a hypothetical analogy). 1 runnable example
  (`reliability_math_demo.py`, verified, arithmetic double-checked by
  hand). 1 lab: a multi-task progress-file agent proven via a real
  kill-and-resume test (call the single-task function directly to simulate
  a crash, then call the full resumable function again and verify the
  completed task is never re-run) -- the identical test-pattern discipline
  from Module 07's lab, now at task-list granularity. 5 tests passing;
  starter's gaps correctly raise `NotImplementedError`. 254 passed, 10
  skipped, 3 deselected repo-wide; links checked (95 unique, all OK).
- ✅ 23 Research literacy -- **no code lab, per the approved plan** (a
  reading/judgment skill, not something a test suite verifies). 3 lessons:
  how to read an agent paper (separating claim from framing, auditing
  baseline/eval-set/variance, taking limitations sections seriously); 
  assessing reproducibility (exact prompts/dated model versions/sampling
  params/eval harness -- what "code is released" doesn't automatically
  cover); a worked example applying both lessons to the real GRPO/
  DeepSeekMath paper (arXiv 2402.03300, confirmed real) already used in
  Module 21 -- explicitly separates what was verified (title, framing, and
  the exact formula, the latter cross-checked against an independent
  source, Hugging Face TRL) from what was NOT independently verified
  (DeepSeekMath's own reported benchmark numbers), modeling the "mark
  UNVERIFIED" discipline concretely rather than just describing it. Ties
  this module's whole framing explicitly back to two corrections this
  session already made for real (Module 14's computer-use claim, Module
  18's OWASP claim) as worked proof the discipline isn't hypothetical.
  254 passed, 10 skipped, 3 deselected repo-wide (unchanged -- no code this
  module); links checked (97 unique, all OK).
- ✅ 24 Becoming a pro -- **no code lab, per the approved plan.** 3 lessons:
  building a portfolio (specificity/evidence over technology lists;
  projects+capstones as the right showcase scale, individual labs as depth
  evidence within those); open-source contribution (genuine gaps found
  through real use -- citing Module 11's and Module 20's own pitfalls.md
  entries as real examples of exactly this discovery process -- small/
  precise beats large/ambitious for a first PR); agent system-design
  interviews (constraints-first, cross-cutting-concerns-named-explicitly
  structure). **Populated `system-design/` with its first real content**
  (previously an empty stub): two full worked case studies --
  `01-customer-support-agent-platform.md` (a single-agent-is-correct case)
  and `02-multi-agent-research-system.md` (a multi-agent-earns-its-cost
  case) -- each explicitly citing the specific curriculum modules and
  actual `projects/` implementations the design draws on, per the
  approved plan's cross-cutting-materials guidance. **Level 6 is now fully
  complete.** 254 passed, 10 skipped, 3 deselected repo-wide (unchanged --
  no code this module); links checked (98 unique, all OK).

## Capstones

- ✅ 1. Production coding agent -- ships with README (spec), ARCHITECTURE.md,
  THREAT_MODEL.md (5 named threats, each mapped to a specific passing
  test, following Module 18's exact red-team framing), and DEPLOY.md
  (sketches Module 19's service/idempotency/routing patterns applied to
  this agent, no new runnable code -- reuses Module 19's already-tested
  mechanics by reference rather than reimplementing them). Reuses Module
  13's exact agent-loop/sandboxing implementation unmodified (deliberate --
  see ARCHITECTURE.md's rationale) against **3 sample repos**
  (`sample_repo/{calculator,strings,numbers}/`, each with one distinct
  real bug), plus a generic `eval_harness.py` (`run_eval`, Module 16's
  `evaluate_dataset` shape -- the agent function and client factory are
  injected, never imported) reporting an aggregate pass rate across all
  three, standing in for the plan's "scored on a held-out test set"
  requirement. **Hit and fixed a real pytest gotcha**: two of this
  capstone's test files (`test_coding_agent.py`, `test_eval_harness.py`)
  collided by basename with same-named test files already in
  `curriculum/13-.../tests/` and `curriculum/16-.../tests/` --
  pytest's default import mode requires globally-unique test file
  basenames across the whole repo when no `__init__.py` files are present;
  renamed to `test_capstone_coding_agent.py`/`test_capstone_eval_harness.py`
  to fix (a real, reproducible collision, not a hypothetical one -- worth
  remembering when naming any future test file: check it's unique
  repo-wide, not just within its own directory). 11 tests passing;
  starter's gaps correctly raise `NotImplementedError`. 265 passed, 10
  skipped, 3 deselected repo-wide; links checked (98 unique, all OK).
- ✅ 2. Multi-agent research system -- ships with README (spec),
  ARCHITECTURE.md, THREAT_MODEL.md (4 named threats, each mapped to a
  specific passing test, drawing on both Module 18's red-team framing and
  Module 12 lesson 02's named multi-agent failure modes), and DEPLOY.md.
  Extends `projects/04-multi-agent-content-pipeline/`'s researcher/writer/
  critic topology **unmodified in its core control flow** with: real
  nested tracing (Module 17 -- each worker wrapped in its own
  `invoke_agent_span`, verified via actual parent/child `span_id` checks,
  not just span-name presence, directly proving Module 17 lesson 02's
  "multi-agent debugging needs the whole graph" point) and a numbered-fact
  citation mechanism (`extract_citations`/`verify_citations`, a mechanical
  check rather than an LLM-as-judge, deliberately) plus a generic
  `eval_suite.py` (`evaluate_citation_accuracy`, Module 16's
  `evaluate_dataset` shape) that excludes escalated topics from the mean
  score. Named test files with the `test_capstone_*` prefix proactively
  (per the lesson learned in Capstone 1) -- no collisions this time. 13
  tests passing; starter's gaps correctly raise `NotImplementedError`. 278
  passed, 10 skipped, 3 deselected repo-wide; links checked (98 unique,
  all OK).
- ✅ 3. Secure enterprise agent -- ships with README (spec), ARCHITECTURE.md,
  THREAT_MODEL.md (a full red-team report following Module 18's exact
  four-step process, 4 threats each mapped to a specific passing test),
  and DEPLOY.md. A real `mcp.server.MCPServer`/`mcp.Client` (Module 10)
  exposing `lookup_record`/`send_announcement`, composed with Module 09's
  approval-gate pattern (`message_to_dict`/`from_dict`,
  `save_checkpoint`/`load_checkpoint`, `AgentResult`, all unchanged in
  shape) -- `dispatch` bridges the two by calling the real MCP client
  instead of a local function registry. **Discovered and verified a real,
  non-obvious `mcp` package behavior**: raising a plain exception inside an
  `@mcp.tool()` function is caught and replaced with a generic "Error
  executing tool X" message -- the specific message only propagates if the
  tool raises `mcp.server.mcpserver.exceptions.ToolError` instead (found
  by installing the real package and testing both paths directly before
  writing any lesson/capstone content, documented in ARCHITECTURE.md).
  **Core red-team proof**: `send_announcement`'s channel allowlist lives
  inside the MCP tool itself, so a request to a non-allowlisted channel is
  blocked even when a human approves it (`resume_after_approval(...,
  approved=True)`) -- proven by
  `test_redteam_approved_but_non_allowlisted_channel_is_still_blocked`.
  Kill-and-resume is tested against **freshly loaded module instances and
  a freshly started MCP server** (not the same objects used to create the
  checkpoint), a stronger proof than reusing live objects would be. 7
  tests passing; starter's gaps correctly raise `NotImplementedError`.
  285 passed, 10 skipped, 3 deselected repo-wide; links checked (98
  unique, all OK). **This is the last capstone -- all 25 curriculum
  modules, 5 projects, and 3 capstones are now complete.**

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

**Every module, project, and capstone in the approved plan is now built
(25 curriculum modules, 5 projects, 3 capstones).** What remains is the
**final pass** described in the approved plan:

1. **Full offline test suite** -- last confirmed green: 285 passed, 10
   skipped (framework/DSPy/live tests correctly skipped without those
   extras installed), 3 deselected (`live`-marked), 0 failed. Re-run
   `uv run pytest -q` fresh before considering this final pass complete,
   since files may have changed since this note was written.
2. **`test-live` smoke run** -- **not run this session** (no real provider
   API keys in this environment). Known live-gated tests still needing a
   real run when keys are available: Module 03's live provider tests,
   Module 11's Claude Agent SDK live test, Module 14's live Playwright
   test (also needs `playwright install chromium`, which timed out this
   session), Module 15's live Anthropic vision test, Module 20's DSPy live
   path if one exists. Grep for `@pytest.mark.live` repo-wide to get the
   current complete list before running.
3. **Full link check** -- last confirmed green: `uv run python
   scripts/check_links.py` reports "All links OK" (98 unique links across
   269 files as of Capstone 3). Re-run fresh; note one transient timeout
   was observed once earlier (Module 20, a SETUP.md link) that resolved on
   retry -- treat a single failure as possibly transient and retry before
   concluding a link is actually broken.
4. **`mkdocs build`** -- last known state (from Phase 0): succeeds without
   `--strict` (cross-link warnings are a known, documented, non-fatal
   limitation -- see Open Issues below). Re-run `make docs` and confirm
   this is still true after 25 modules' worth of new content; check
   whether `docs/`'s `nav:` should now include module entries (noted as
   low-priority in Open Issues since Phase 0, revisit given how much
   content now exists).
5. **Terminology-vs-`GLOSSARY.md` consistency check** -- **not yet done
   this session.** `GLOSSARY.md` was written in Phase 0, before any of
   Modules 00-24 existed; it needs a fresh pass checking that terms
   introduced across all 25 modules (RLVR, GRPO, indirect prompt
   injection, idempotency key, progress file, etc.) are actually defined
   there, and that terminology is used consistently across modules (e.g.
   "tool call" vs "function call," "checkpoint" vs "progress file" used
   for genuinely different things per Module 07 vs Module 22, not
   conflated).
6. **Prerequisite-ordering check across all 25 modules** -- **not yet done
   this session.** Verify each module's stated "Prerequisites" link and
   each lesson's cross-references to earlier modules actually only ever
   point backward (never forward to a module not yet introduced) --
   spot-check is easy given every module's README explicitly named its
   prerequisite; a full pass would grep every lesson file for "Module NN"
   references and confirm NN is always ≤ the current module's own number.
7. **Summary of what shipped and any known gaps** -- write this last, once
   1-6 above are actually done, not before. Pull the known-gaps list
   directly from the "Open issues / UNVERIFIED items" section below rather
   than re-deriving it.

Do not mark the curriculum "done" until this final pass actually runs (not
just until every module's individual PROGRESS.md entry says ✅) -- the
final pass is explicitly a separate, later verification step in the
approved plan, distinct from each module's own build-time checks.
