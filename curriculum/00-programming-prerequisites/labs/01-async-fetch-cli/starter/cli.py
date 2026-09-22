"""Lab 00.01: async fetch + JSON CLI. See ../README.md for the full spec.

Fill in the four functions below. Run the tests against your work with:
    LAB_TARGET=starter uv run pytest \
        curriculum/00-programming-prerequisites/labs/01-async-fetch-cli/tests
"""

from __future__ import annotations

import sys

import httpx


async def fetch_json(client: httpx.AsyncClient, url: str) -> dict:
    """GET `url` with `client`, raise for non-2xx status, return the parsed JSON body.

    TODO: implement this.
    """
    raise NotImplementedError


def extract_field(data: dict, field_path: str) -> object:
    """Walk `data` following each dot-separated part of `field_path`.

    Example: extract_field({"a": {"b": 1}}, "a.b") == 1

    TODO: implement this. Raise KeyError naming the exact missing part if any
    step of the path isn't present.
    """
    raise NotImplementedError


async def run(url: str, field_path: str) -> str:
    """Fetch `url`, extract `field_path`, return the result as a string.

    TODO: open an httpx.AsyncClient as a context manager, call fetch_json and
    extract_field, and return str(value). Let exceptions propagate -- don't
    catch them here.
    """
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Parse argv as [url, field_path], run(), print the result, return an exit code.

    TODO: implement this. On httpx.HTTPStatusError or KeyError, print
    f"Error: {exc}" to sys.stderr and return 1. On success, print the result
    and return 0.
    """
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
