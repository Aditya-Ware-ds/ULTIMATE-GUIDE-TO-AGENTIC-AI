# Module 14 pitfalls

## Assuming a vendor's computer-use approach without checking current docs

It's tempting to describe "how computer-use agents work" from general
impression or older material. While building this module, an earlier
working assumption ("the field converged on accessibility tree +
screenshot") turned out to be stale the moment it was checked against
Claude's, OpenAI's, and Gemini's current docs on 2026-09-22 -- all three
currently use screenshots and pixel coordinates only. This is exactly
Ground Rule 1's warning in practice: verify against current sources before
writing a claim into a lesson, especially for anything framed as "the
current state of X," since this field moves fast enough that a
several-month-old mental model can already be wrong.

## Letting the fake browser session drift from the real page's actual behavior

The lab's `FakeBrowserSession` deliberately mirrors `sample_site/index.html`'s
real behavior exactly (`#details` doesn't exist until `#details-btn` is
clicked) so that tests passing against the fake actually predict tests
passing against a real Playwright browser. If you change the sample page
without updating the fake session (or vice versa), your offline tests can
pass while the real, live-gated test fails -- always keep the fake and the
real page in sync, the same discipline Module 00's local-server fixture
uses to stay faithful to the real API it stands in for.

## Treating a URL allowlist as decoration instead of the actual boundary

It's easy to write `goto`'s allowlist check and then, elsewhere in the same
codebase, call `session.goto(url)` directly for convenience -- bypassing the
check entirely. The allowlist only does anything if *every* navigation path
goes through it; a coding-agent-style shortcut ("just this once, call the
session directly") reopens exactly the unrestricted-navigation risk lesson
01 exists to close.

## Forgetting that a `Protocol` gives no runtime guarantee

`BrowserSession` being a `Protocol` means type checkers can verify a class
implements it, but nothing stops you from passing an object missing one of
the three methods at runtime -- you'd only find out when that specific
method is called and raises `AttributeError`. This is a normal tradeoff of
structural typing, not a bug, but it means test coverage of all three
methods (not just the ones a happy-path test happens to exercise) matters
more than it would with a strictly-enforced abstract base class.
