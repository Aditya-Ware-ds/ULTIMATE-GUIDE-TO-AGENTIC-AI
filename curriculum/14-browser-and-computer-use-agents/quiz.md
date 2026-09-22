# Module 14 quiz

**1. Why does DOM/selector-based browser automation tend to be more reliable than pixel-coordinate control?**

<details><summary>Answer</summary>

Selectors reference the page's actual structure (an element's id, class, or
attributes), which survives most layout changes. Pixel coordinates describe
a specific point on the rendered screen, which shifts whenever the layout
changes even slightly -- the same visual click target can move without any
change to the underlying element.

</details>

**2. Why does `goto` need a URL allowlist rather than accepting any URL the model requests?**

<details><summary>Answer</summary>

Without one, a model that decides mid-task to "look something up" could
navigate anywhere, including a page designed to feed it malicious
instructions (an indirect prompt-injection vector, previewed here and
covered fully in Module 18). This is the browser equivalent of Module 13's
path-scoping for file tools -- least privilege applied to navigation.

</details>

**3. As of 2026-09-22, how do Claude's, OpenAI's, and Gemini's computer-use tools currently perceive the screen?**

<details><summary>Answer</summary>

All three use screenshots and pixel coordinates -- none currently uses or
relies on an OS accessibility tree for general computer use. This was
verified directly against each vendor's current docs while writing this
module, correcting an earlier "accessibility tree + screenshot" assumption
that turned out to be stale.

</details>

**4. When should you reach for screenshot-based computer use instead of DOM-based browser automation?**

<details><summary>Answer</summary>

Only when the task needs to operate outside a browser's DOM entirely -- a
native desktop application, a PDF viewer, or anything without a structured
interface to select against. For a task confined to a browser, DOM-based
automation is more reliable and cheaper.

</details>

**5. Why is a fixed `time.sleep()` an unreliable way to wait for a page to finish loading?**

<details><summary>Answer</summary>

It's a guess about timing, not a check of actual state -- either too short
(flaky, the page genuinely needed longer) or wasteful (too long for a page
that was ready sooner). An explicit wait condition (e.g. `wait_for_selector`)
checks the actual thing that matters and proceeds as soon as it's true.

</details>

**6. Why should retries be applied only to transient failures, not every failure?**

<details><summary>Answer</summary>

A transient failure (an element not yet rendered) can genuinely resolve on
retry. A failure caused by a wrong premise (the button was renamed, or
never existed) will fail identically every time -- retrying it just delays
surfacing a real problem, the same distinction Module 03 draws for tool
error handling generally.

</details>

**7. In this module's lab, why does `get_text("#details")` raise an error before `#details-btn` is clicked?**

<details><summary>Answer</summary>

The sample page's button creates the `#details` element via JavaScript only
when clicked -- it genuinely doesn't exist in the DOM beforehand. The fake
browser session mirrors this real behavior deliberately, so the lab's task
genuinely requires a `click` step, not just a single `get_text` call.

</details>

**8. Why is `BrowserSession` defined as a `Protocol` rather than a concrete base class?**

<details><summary>Answer</summary>

Structural typing lets any object with the right three methods (`goto`,
`click`, `get_text`) work as a `BrowserSession` -- including a real
`PlaywrightBrowserSession` and a hand-written fake used in offline tests --
without either one needing to inherit from a shared base class. This is
what makes the lab's core logic testable without a real browser.

</details>

**9. Why does this module's lab keep the real Playwright test behind `@pytest.mark.live` instead of running it by default?**

<details><summary>Answer</summary>

Real Playwright browser automation needs the `playwright` package plus
downloaded browser binaries (`playwright install`) -- a real external
dependency this repo's default test suite shouldn't require. Gating it
behind `live` keeps `make test` fast, deterministic, and installable with
zero extra setup, the same pattern used for every other framework/live
dependency in this curriculum (Module 11's frameworks, Module 03's
`live`-marked API-key tests).

</details>

**10. A task needs to read a web page's content exactly once, with no interaction required. Should you reach for this module's browser-automation agent?**

<details><summary>Answer</summary>

No -- a plain HTTP GET (Module 00's async-fetch-cli, or Module 06's
retrieval tools) is cheaper and more reliable than launching a browser for
something that doesn't require rendering or interaction. Browser automation
earns its cost only when a task genuinely needs to interact with a
rendered, stateful page.

</details>
