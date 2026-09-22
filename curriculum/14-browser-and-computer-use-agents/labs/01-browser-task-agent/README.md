# Lab 14.01 -- Browser task agent

**Difficulty:** ★★★★☆ · **Time:** ~2-3 hours

## Task

Build a browser-automation agent (Module 04's ReAct loop, plus `goto`,
`click`, and `get_text` tools) that answers a question about a small,
bundled local page by navigating and clicking through it. No API key or real
browser needed for the default tests -- tested against
`shared.llm.get_client("mock")` and a minimal fake browser session. One
`@pytest.mark.live` test drives a real Playwright browser against the
bundled page.

`sample_site/index.html` is a tiny product page: a title, a price, and a
"View details" button that reveals battery/color info only once clicked --
so answering the lab's question genuinely requires a `click` before a
`get_text`, not just reading the page once.

## Files

- `starter/browser_agent.py` -- skeleton with the pieces to implement
- `solution/browser_agent.py` -- complete reference implementation
- `sample_site/index.html` -- the bundled test page
- `tests/` -- offline tests (a fake browser session) + one live-gated Playwright test

## Requirements

Implement these in `starter/browser_agent.py` (`BrowserSession` and
`PlaywrightBrowserSession` are already given):

- `def goto(session, url: str, allowed_prefixes: tuple[str, ...]) -> str` --
  raise `ValueError` if `url` doesn't start with any of `allowed_prefixes`
  (see lessons/01); otherwise call `session.goto(url)` and return a
  confirmation string.
- `def click(session, selector: str) -> str` / `def get_text(session, selector: str) -> str`
  -- thin wrappers around the session's own methods.
- `def build_tool_registry(session, allowed_prefixes) -> dict[str, Callable]`
  -- a registry of the three tools as callables taking only the
  model-supplied arguments (bind `session`/`allowed_prefixes` via closure).
- `def dispatch(tool_call, registry) -> ToolResult` -- same contract as
  prior modules.
- `async def run_browser_agent(client, session, task: str, allowed_prefixes: tuple[str, ...], max_steps: int = 6) -> str`
  -- the ReAct loop (Module 04) using these tools.

## Acceptance criteria

- All tests in `tests/` pass against your `starter/browser_agent.py`.
- `goto` raises `ValueError` for a URL not on the allowlist, and never calls
  `session.goto` in that case.
- `get_text("#details")` raises before `#details-btn` has been clicked (the
  fake session mirrors the real page's actual behavior).
- `run_browser_agent` correctly chains `goto` -> `click` -> `get_text` ->
  final answer for the lab's scripted scenario, making exactly 4 model
  calls.
- Hitting `max_steps` returns a message that says so, not a bare answer.

## Running the tests

```bash
uv run pytest curriculum/14-browser-and-computer-use-agents/labs/01-browser-task-agent/tests
```

Against your own work in progress:

```bash
LAB_TARGET=starter uv run pytest curriculum/14-browser-and-computer-use-agents/labs/01-browser-task-agent/tests
```

Live, against a real Playwright browser (one-time setup, then run):

```bash
uv run --with "playwright>=1.47" playwright install chromium
uv run --with "playwright>=1.47" pytest -m live curriculum/14-browser-and-computer-use-agents/labs/01-browser-task-agent/tests
```

## Next

[`quiz.md`](../../quiz.md) · [`pitfalls.md`](../../pitfalls.md) · then
[Module 15 -- Voice & multimodal agents](../../../15-voice-and-multimodal-agents/README.md)
