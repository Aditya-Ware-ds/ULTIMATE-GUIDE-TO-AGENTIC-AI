# Screenshots vs. the DOM: two different computer-use approaches

**Last verified:** 2026-09-22 (against Anthropic's, OpenAI's, and Google's current computer-use docs -- see resources.md)
**Difficulty:** ★★★☆☆ · **Time:** ~30 minutes

## Learning objectives

- Correctly describe how Claude's, OpenAI's, and Gemini's computer-use tools currently perceive a screen.
- Explain why general computer-use tools use screenshots and pixel coordinates rather than the DOM/accessibility tree, and what that trades away.
- Choose between DOM-based browser automation and screenshot-based computer use for a given task.

## Intuition

This module's lab uses lesson 01's DOM-based approach because its task stays
entirely inside a browser. Not every task does -- a desktop spreadsheet, a
native settings dialog, or an arbitrary unfamiliar application has no DOM to
select against at all. General "computer use" tools solve a harder, more
general problem, and as of 2026-09-22, all three major vendors solve it the
same way: **screenshots and pixel coordinates, not an accessibility tree.**

## The concept

### What Claude's, OpenAI's, and Gemini's computer-use tools actually do

Verified directly against each vendor's current documentation on
2026-09-22:

- **Claude's computer-use tool** (GA on the Claude API) perceives the
  screen through **screenshots only** -- base64-encoded images of the
  virtual display, with a zoom capability for inspecting small regions at
  full resolution. All actions (`left_click`, `type`, `scroll`, `wait`, and
  others) use pixel coordinates in screenshot space, not element references.
- **OpenAI's computer-use tool** is documented the same way: "Give the model
  a current screenshot when the UI state is unknown. After a short group of
  actions, return another screenshot so it can check the result" -- an
  explicit screenshot-observe-act loop, again with pixel-coordinate actions
  (`click`, `drag`, `scroll`, `keypress`, `type`).
- **Gemini's Computer Use** (currently Preview) is described identically:
  "Using screenshots, the model can 'see' a computer screen," with a
  browser-environment action set (click, type, scroll, navigate) driven the
  same way.

None of the three currently expose or rely on an OS accessibility tree for
general computer use -- this module's earlier working assumption that the
field had converged on "accessibility tree + screenshot" was checked against
each vendor's current docs while writing this lesson and turned out to be
stale; screenshot-plus-pixel-coordinates is the actual current pattern
across all three.

### Why screenshots, not the DOM, for general computer use

A screenshot-based approach works on *anything renderable* -- a browser, a
native app, a terminal, a PDF viewer -- because it doesn't depend on the
target exposing any particular structured interface. The cost is real:
pixel coordinates are more brittle than selectors (a layout shift of a few
pixels can misdirect a click), screenshots are token-expensive (roughly
1,000-1,800 tokens each per Claude's current docs, compounding over a long
session), and the model has to *infer* what's clickable from pixels rather
than being told directly.

### The actual choice this creates

| | DOM/selector-based (lesson 01) | Screenshot-based (this lesson) |
|---|---|---|
| Scope | Browser tasks only | Anything renderable on screen |
| Reliability | High -- selectors survive most layout changes | Lower -- pixel coordinates are layout-sensitive |
| Cost | Cheap (text-based) | Expensive (image tokens per step) |
| When to use | The task stays inside a browser you control | The task spans native apps, or the page has no usable DOM structure |

Real coding-agent products increasingly offer both, and let the model or the
integrator choose per task -- OpenAI's own current guidance explicitly
recommends Playwright/PyAutoGUI-driven code execution as an alternative path
to the structured screenshot-based computer tool for exactly this reason.

## Deeper: this module's lab deliberately stays in the DOM-based lane

Given the choice above, this module's lab uses Playwright/DOM-based
automation specifically because its task (navigate a page, read text,
click a button) never leaves the browser -- there's no reason to pay
screenshot-based automation's reliability and cost tax for a task
selector-based automation handles cleanly. Recognizing which lane a real
task falls into is the actual skill this lesson teaches; implementing a full
screenshot-based computer-use loop is out of scope for this module's lab.

## When not to use this

Don't build a screenshot-based computer-use loop for a task confined to a
browser -- that's lesson 01's job, more reliably and more cheaply. Reach for
screenshot-based computer use only when the task genuinely needs to operate
outside a DOM you can select against.

## Common mistakes

- Assuming a specific vendor's computer-use approach from general
  intuition or older material rather than checking current docs -- as this
  lesson's own writing process demonstrated, this is exactly the kind of
  claim that goes stale fast (Ground Rule 1).
- Using screenshot-based computer use for an in-browser task "because it's
  more general," paying unnecessary cost and reliability tax for no benefit.
- Not budgeting for screenshot token cost in a long screenshot-based loop --
  it compounds quickly compared to text-based tool results.

## Key takeaways

- As of 2026-09-22, Claude, OpenAI, and Gemini's computer-use tools all perceive the screen via screenshots and pixel coordinates, not an accessibility tree.
- Screenshot-based control generalizes to anything renderable but costs more and is less reliable than DOM-based selectors for in-browser tasks.
- Choose DOM-based automation when a task stays inside a browser; reach for screenshot-based computer use only when it genuinely needs to leave one.

## Lab

[`labs/01-browser-task-agent/`](../labs/01-browser-task-agent/README.md)
