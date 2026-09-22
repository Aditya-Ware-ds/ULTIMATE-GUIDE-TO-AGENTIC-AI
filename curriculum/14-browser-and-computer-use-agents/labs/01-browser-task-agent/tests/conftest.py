"""Fixtures for the browser-task-agent lab: loads starter/ or solution/ (see
shared/testing/lab_loader.py) and provides a minimal fake browser session
purpose-built for this lab's one scripted scenario -- not a general DOM
simulator -- so the default offline tests never need a real browser.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from shared.llm import get_client
from shared.testing import load_lab_module

LAB_DIR = Path(__file__).resolve().parent.parent
SAMPLE_SITE_INDEX = (LAB_DIR / "sample_site" / "index.html").resolve().as_uri()


class FakeBrowserSession:
    """Mirrors sample_site/index.html's actual behavior: #title and #price
    are always present; #details is only created after #details-btn is
    clicked -- same as the real page's onclick handler.
    """

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
        if selector == "#price":
            return "$24.99"
        if selector == "#details":
            if "#details-btn" not in self.clicked:
                raise ValueError(f"No element matching {selector!r}")
            return "Battery life: 6 months. Color: black."
        raise ValueError(f"No element matching {selector!r}")


@pytest.fixture
def browser_agent():
    return load_lab_module(LAB_DIR, "browser_agent")


@pytest.fixture
def client():
    return get_client("mock")


@pytest.fixture
def session() -> FakeBrowserSession:
    return FakeBrowserSession()


@pytest.fixture
def sample_site_index() -> str:
    return SAMPLE_SITE_INDEX


@pytest.fixture
def allowed(sample_site_index: str) -> tuple[str, ...]:
    return (sample_site_index,)
