"""Run: uv run python curriculum/14-browser-and-computer-use-agents/examples/browser_tools_demo.py

Shows the goto/click/get_text action vocabulary and URL allowlisting against
a tiny fake browser session -- no real browser, no API key needed. See
lessons/01-browser-automation.md.
"""

from __future__ import annotations


class FakeBrowserSession:
    """A minimal stand-in for a real browser page (see lessons/01)."""

    def __init__(self) -> None:
        self.current_url: str | None = None
        self.clicked: set[str] = set()

    def goto(self, url: str) -> None:
        self.current_url = url

    def click(self, selector: str) -> None:
        self.clicked.add(selector)

    def get_text(self, selector: str) -> str:
        if selector == "#title":
            return "Wireless Mouse"
        if selector == "#details":
            if "#details-btn" not in self.clicked:
                raise ValueError(f"No element matching {selector!r} yet")
            return "Battery life: 6 months."
        raise ValueError(f"No element matching {selector!r}")


def goto(session, url: str, allowed_prefixes: tuple[str, ...]) -> str:
    if not any(url.startswith(prefix) for prefix in allowed_prefixes):
        raise ValueError(f"URL not allowed: {url!r}")
    session.goto(url)
    return f"Navigated to {url}"


def main() -> None:
    session = FakeBrowserSession()
    allowed = ("file:///sample_site/",)

    print(goto(session, "file:///sample_site/index.html", allowed))

    print("Reading the title:", session.get_text("#title"))

    try:
        session.get_text("#details")
    except ValueError as exc:
        print(f"Before clicking: {exc}")

    session.click("#details-btn")
    print("After clicking:", session.get_text("#details"))

    print("Disallowed navigation is rejected:")
    try:
        goto(session, "https://not-on-the-allowlist.example.com", allowed)
    except ValueError as exc:
        print(f"  {exc}")


if __name__ == "__main__":
    main()
