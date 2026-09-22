"""Checks every http(s) link in the repo's Markdown files actually resolves.

Run via `make check-links`. Exits non-zero (and prints the failing URLs and the
files that reference them) if any link returns an error status or fails to
connect. Skips localhost/example URLs. Network access required.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import httpx

LINK_RE = re.compile(r"\[[^\]]*\]\((https?://[^\s)]+)\)")
SKIP_HOSTS = (
    "localhost",
    "127.0.0.1",
    "example.com",
    "example.org",
    # Authenticated provider console pages: they redirect to a login page or
    # bot-block automated GET/HEAD requests (302/403) even when the link is
    # correct, so they aren't reliably checkable here. Verify these manually.
    "aistudio.google.com",
    "platform.openai.com",
    "console.anthropic.com",
)
REPO_ROOT = Path(__file__).resolve().parent.parent


def find_markdown_files() -> list[Path]:
    return [p for p in REPO_ROOT.rglob("*.md") if ".venv" not in p.parts and "site" not in p.parts]


def extract_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return [url for url in LINK_RE.findall(text) if not any(host in url for host in SKIP_HOSTS)]


def main() -> int:
    url_to_files: dict[str, list[Path]] = {}
    for path in find_markdown_files():
        for url in extract_links(path):
            url_to_files.setdefault(url, []).append(path)

    failures: list[tuple[str, str]] = []
    # A generic requests-style default User-Agent gets bot-blocked (403) by some
    # sites (Wikipedia among them) that otherwise serve normal browsers fine.
    headers = {"User-Agent": "Mozilla/5.0 (compatible; agentic-ai-mastery-link-check/1.0)"}
    with httpx.Client(follow_redirects=True, timeout=10.0, headers=headers) as client:
        for url in sorted(url_to_files):
            try:
                response = client.head(url)
                if response.status_code >= 400:
                    response = client.get(url)
                if response.status_code >= 400:
                    failures.append((url, f"HTTP {response.status_code}"))
            except httpx.HTTPError as exc:
                failures.append((url, str(exc)))

    print(f"Checked {len(url_to_files)} unique links across {len(find_markdown_files())} files.")
    if failures:
        print(f"\n{len(failures)} broken link(s):\n")
        for url, reason in failures:
            files = ", ".join(str(f.relative_to(REPO_ROOT)) for f in url_to_files[url])
            print(f"  {url}  ({reason})\n    referenced in: {files}")
        return 1
    print("All links OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
